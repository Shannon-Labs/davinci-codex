from __future__ import annotations

import os
from datetime import datetime
from typing import Dict, List, Optional

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./davinci_folios.db")
Base = declarative_base()


class Folio(Base):
    """
    Represents a folio (page) from Leonardo da Vinci's manuscripts.
    """
    __tablename__ = "folios"

    id = Column(Integer, primary_key=True, index=True)
    folio_id = Column(String, unique=True, index=True, nullable=False)
    image_path = Column(String, nullable=False)
    text_content = Column(Text)
    components_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Metadata fields
    source = Column(String, default="Codex Atlanticus")
    date_estimated = Column(String, default="15th century")
    location = Column(String, default="Milan")
    category = Column(String, default="mechanical invention")

    # Relationships
    components = relationship("Component", back_populates="folio", cascade="all, delete-orphan")
    linked_inventions = relationship("InventionLink", back_populates="folio", cascade="all, delete-orphan")


class Component(Base):
    """
    Represents a mechanical component identified in a folio.
    """
    __tablename__ = "components"

    id = Column(Integer, primary_key=True, index=True)
    folio_id = Column(Integer, ForeignKey("folios.id"), nullable=False)
    component_id = Column(String, nullable=False)
    bbox_x = Column(Integer)
    bbox_y = Column(Integer)
    bbox_width = Column(Integer)
    bbox_height = Column(Integer)
    area = Column(Float)
    aspect_ratio = Column(Float)
    circularity = Column(Float)
    classification = Column(String, default="unclassified")
    confidence_score = Column(Float, default=0.0)

    # Relationship to folio
    folio = relationship("Folio", back_populates="components")


class InventionLink(Base):
    """
    Represents a link between a folio and an invention.
    """
    __tablename__ = "invention_links"

    id = Column(Integer, primary_key=True, index=True)
    folio_id = Column(Integer, ForeignKey("folios.id"), nullable=False)
    invention_slug = Column(String, nullable=False)
    confidence_score = Column(Float, default=0.0)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    folio = relationship("Folio", back_populates="linked_inventions")


class FolioDatabase:
    """
    Database interface for managing folio data and invention links.
    """

    def __init__(self, db_url: str = DATABASE_URL):
        """
        Initialize the database connection.

        Args:
            db_url: Database connection URL
        """
        self.engine = create_engine(db_url)
        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self):
        """
        Get a database session.

        Returns:
            SQLAlchemy session object
        """
        return self.SessionLocal()

    def create_folio(self, folio_data: Dict) -> Folio:
        """
        Create a new folio entry in the database.

        Args:
            folio_data: Dictionary containing folio information

        Returns:
            Created Folio object
        """
        session = self.get_session()
        try:
            # Create folio record
            folio = Folio(
                folio_id=folio_data["folio_id"],
                image_path=folio_data["image_path"],
                text_content=folio_data.get("text_content", ""),
                components_count=folio_data.get("components_count", 0),
                source=folio_data.get("metadata", {}).get("source", "Codex Atlanticus"),
                date_estimated=folio_data.get("metadata", {}).get("date", "15th century"),
                location=folio_data.get("metadata", {}).get("location", "Milan"),
                category=folio_data.get("metadata", {}).get("category", "mechanical invention")
            )

            session.add(folio)
            session.commit()

            # Add components if they exist
            if "components" in folio_data:
                for component in folio_data["components"]:
                    comp = Component(
                        folio_id=folio.id,
                        component_id=str(component.get("component_id", "")),
                        bbox_x=component.get("bbox", [0, 0, 0, 0])[0],
                        bbox_y=component.get("bbox", [0, 0, 0, 0])[1],
                        bbox_width=component.get("bbox", [0, 0, 0, 0])[2],
                        bbox_height=component.get("bbox", [0, 0, 0, 0])[3],
                        area=component.get("area", 0.0),
                        aspect_ratio=component.get("aspect_ratio", 0.0),
                        circularity=component.get("circularity", 0.0),
                        classification=component.get("classification", "unclassified"),
                        confidence_score=component.get("confidence_score", 0.0)
                    )
                    session.add(comp)

            session.commit()
            return folio
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def update_folio(self, folio_id: str, updates: Dict) -> Optional[Folio]:
        """
        Update an existing folio entry.

        Args:
            folio_id: ID of the folio to update
            updates: Dictionary of fields to update

        Returns:
            Updated Folio object or None if not found
        """
        session = self.get_session()
        try:
            folio = session.query(Folio).filter(Folio.folio_id == folio_id).first()
            if not folio:
                return None

            # Update basic fields
            if "text_content" in updates:
                folio.text_content = updates["text_content"]
            if "components_count" in updates:
                folio.components_count = updates["components_count"]
            if "source" in updates:
                folio.source = updates["source"]
            if "date_estimated" in updates:
                folio.date_estimated = updates["date_estimated"]
            if "location" in updates:
                folio.location = updates["location"]
            if "category" in updates:
                folio.category = updates["category"]

            # Update components if provided
            if "components" in updates:
                # First, remove existing components
                session.query(Component).filter(Component.folio_id == folio.id).delete()

                # Add new components
                for component in updates["components"]:
                    comp = Component(
                        folio_id=folio.id,
                        component_id=str(component.get("component_id", "")),
                        bbox_x=component.get("bbox", [0, 0, 0, 0])[0],
                        bbox_y=component.get("bbox", [0, 0, 0, 0])[1],
                        bbox_width=component.get("bbox", [0, 0, 0, 0])[2],
                        bbox_height=component.get("bbox", [0, 0, 0, 0])[3],
                        area=component.get("area", 0.0),
                        aspect_ratio=component.get("aspect_ratio", 0.0),
                        circularity=component.get("circularity", 0.0),
                        classification=component.get("classification", "unclassified"),
                        confidence_score=component.get("confidence_score", 0.0)
                    )
                    session.add(comp)

            session.commit()
            return folio
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def add_invention_link(self, folio_id: str, invention_slug: str, confidence_score: float = 0.0, notes: str = "") -> Optional[InventionLink]:
        """
        Link a folio to an invention.

        Args:
            folio_id: ID of the folio
            invention_slug: Slug identifier for the invention
            confidence_score: Confidence score for the link (0.0-1.0)
            notes: Additional notes about the link

        Returns:
            Created InventionLink object or None if folio not found
        """
        session = self.get_session()
        try:
            folio = session.query(Folio).filter(Folio.folio_id == folio_id).first()
            if not folio:
                return None

            # Create invention link
            link = InventionLink(
                folio_id=folio.id,
                invention_slug=invention_slug,
                confidence_score=confidence_score,
                notes=notes
            )

            session.add(link)
            session.commit()
            return link
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_folio_by_id(self, folio_id: str) -> Optional[Folio]:
        """
        Get a folio by its ID.

        Args:
            folio_id: ID of the folio to retrieve

        Returns:
            Folio object or None if not found
        """
        session = self.get_session()
        try:
            folio = session.query(Folio).filter(Folio.folio_id == folio_id).first()
            return folio
        except Exception as e:
            raise e
        finally:
            session.close()

    def get_folios_by_invention(self, invention_slug: str) -> List[Folio]:
        """
        Get all folios linked to a specific invention.

        Args:
            invention_slug: Slug identifier for the invention

        Returns:
            List of Folio objects linked to the invention
        """
        session = self.get_session()
        try:
            folios = session.query(Folio).join(InventionLink).filter(InventionLink.invention_slug == invention_slug).all()
            return folios
        except Exception as e:
            raise e
        finally:
            session.close()

    def get_all_folios(self) -> List[Folio]:
        """
        Get all folios in the database.

        Returns:
            List of all Folio objects
        """
        session = self.get_session()
        try:
            folios = session.query(Folio).all()
            return folios
        except Exception as e:
            raise e
        finally:
            session.close()

    def search_folios(self, query: str, category: Optional[str] = None) -> List[Folio]:
        """
        Search for folios by text content and optionally by category.

        Args:
            query: Search term to match against text content
            category: Optional category filter

        Returns:
            List of matching Folio objects
        """
        session = self.get_session()
        try:
            folios = session.query(Folio)

            # Filter by text content
            if query:
                folios = folios.filter(Folio.text_content.contains(query))

            # Filter by category if provided
            if category:
                folios = folios.filter(Folio.category == category)

            return folios.all()
        except Exception as e:
            raise e
        finally:
            session.close()
