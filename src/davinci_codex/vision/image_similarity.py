"""
Image Similarity Engine

This module implements advanced computer vision techniques to find similar sketches
across different codices, creating connections between related drawings and
enabling a more comprehensive understanding of Leonardo da Vinci's work.
"""

from __future__ import annotations

import os
from typing import Dict, List, Optional

import numpy as np
import torch
from PIL import Image

# Configuration constants
DEFAULT_IMAGE_FORMATS = [".jpg", ".jpeg", ".png", ".tiff", ".bmp"]
FEATURE_EXTRACTOR_MODEL = "resnet50"
SIMILARITY_THRESHOLD = 0.7


class ImageSimilarityEngine:
    """
    Advanced image similarity engine for analyzing Leonardo da Vinci's sketches.

    This class provides comprehensive image similarity analysis including:
    - Feature extraction using deep learning models
    - Similarity calculation based on visual characteristics
    - Cross-codex matching of related sketches
    - Metadata tagging for historical context
    """

    def __init__(self):
        """
        Initialize the image similarity engine.
        """
        # Initialize model for feature extraction
        self.model = self._load_feature_extractor(FEATURE_EXTRACTOR_MODEL)
        self.model.eval()

        # Initialize database of known images
        self.image_database = []

    def _load_feature_extractor(self, model_name: str) -> torch.nn.Module:
        """
        Load a pre-trained feature extractor model.

        Args:
            model_name: Name of the model to load

        Returns:
            PyTorch model for feature extraction
        """
        # For demonstration purposes, we'll use a simple approach
        # In production, this would load a pre-trained model like ResNet50
        return None  # Placeholder for actual implementation

    def extract_features(self, image_path: str) -> Optional[np.ndarray]:
        """
        Extract features from an image for similarity comparison.

        Args:
            image_path: Path to the image file

        Returns:
            Array of features, or None if extraction failed
        """
        try:
            # Load image
            img = Image.open(image_path)

            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # Resize to standard size
            img = img.resize((224, 224))

            # Convert to numpy array
            img_array = np.array(img)

            # Normalize image (scale to 0-1)
            img_array = img_array.astype(np.float32) / 255.0

            # Create feature vector (simplified version)
            # In production, this would use the deep learning model
            feature_vector = np.mean(img_array, axis=(0, 1))  # Average color values

            return feature_vector

        except Exception:
            return None

    def calculate_similarity(self, features1: np.ndarray, features2: np.ndarray) -> float:
        """
        Calculate similarity between two sets of features.

        Uses cosine similarity for comparison.

        Args:
            features1: First set of features
            features2: Second set of features

        Returns:
            Similarity score (0.0 to 1.0)
        """
        # Calculate cosine similarity
        dot_product = np.dot(features1, features2)
        norm1 = np.linalg.norm(features1)
        norm2 = np.linalg.norm(features2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        similarity = dot_product / (norm1 * norm2)

        # Ensure similarity is in range [0, 1]
        similarity = max(0.0, min(1.0, similarity))

        return similarity

    def find_similar_images(self, target_image_path: str, database: List[Dict]) -> List[Dict]:
        """
        Find similar images in the database to the target image.

        Args:
            target_image_path: Path to the target image
            database: List of database entries with image information

        Returns:
            List of similar images with similarity scores
        """
        # Extract features from target image
        target_features = self.extract_features(target_image_path)
        if target_features is None:
            return []

        similar_images = []

        # Compare with each image in database
        for entry in database:
            # Extract features from database image
            db_features = self.extract_features(entry["image_path"])
            if db_features is None:
                continue

            # Calculate similarity
            similarity_score = self.calculate_similarity(target_features, db_features)

            # Add to results if above threshold
            if similarity_score >= SIMILARITY_THRESHOLD:
                similar_images.append({
                    "folio_id": entry.get("folio_id", "Unknown"),
                    "image_path": entry["image_path"],
                    "similarity_score": similarity_score,
                    "metadata": entry.get("metadata", {}),
                    "components_count": entry.get("components_count", 0)
                })

        # Sort by similarity score (descending)
        similar_images.sort(key=lambda x: x["similarity_score"], reverse=True)

        return similar_images

    def add_to_database(self, image_path: str, folio_id: str = "") -> bool:
        """
        Add an image to the database for future similarity comparisons.

        Args:
            image_path: Path to the image file
            folio_id: Identifier for the folio

        Returns:
            True if successfully added, False otherwise
        """
        try:
            # Extract features
            features = self.extract_features(image_path)
            if features is None:
                return False

            # Create database entry
            db_entry = {
                "folio_id": folio_id if folio_id else os.path.basename(image_path).split(".")[0],
                "image_path": image_path,
                "features": features.tolist(),
                "metadata": {
                    "source": "Codex Atlanticus",  # Default source
                    "date": "15th century",  # Default date
                    "location": "Milan",  # Default location
                    "category": "mechanical invention",  # Default category
                },
                "components_count": 0,  # To be updated later
            }

            # Add to database
            self.image_database.append(db_entry)

            return True

        except Exception:
            return False

    def get_database_size(self) -> int:
        """
        Get the current size of the image database.

        Returns:
            Number of images in the database
        """
        return len(self.image_database)

    def clear_database(self) -> None:
        """
        Clear all entries from the image database.
        """
        self.image_database = []

    def search_by_metadata(self, metadata: Dict) -> List[Dict]:
        """
        Search the database for images matching specified metadata.

        Args:
            metadata: Dictionary of metadata to match

        Returns:
            List of matching images
        """
        matching_images = []

        for entry in self.image_database:
            # Check if entry matches metadata
            match = True
            for key, value in metadata.items():
                if key not in entry["metadata"] or entry["metadata"][key] != value:
                    match = False
                    break

            if match:
                matching_images.append(entry)

        return matching_images

    def create_similarity_network(self, database: List[Dict]) -> Dict:
        """
        Create a network of similarities between images in the database.

        Args:
            database: List of database entries

        Returns:
            Dictionary representing the similarity network
        """
        # Initialize network
        network = {
            "nodes": [],
            "edges": [],
            "similarity_threshold": SIMILARITY_THRESHOLD,
        }

        # Add nodes
        for i, entry in enumerate(database):
            node = {
                "id": i,
                "folio_id": entry.get("folio_id", "Unknown"),
                "image_path": entry["image_path"],
                "metadata": entry.get("metadata", {}),
            }
            network["nodes"].append(node)

        # Add edges (connections between similar images)
        for i in range(len(database)):
            for j in range(i + 1, len(database)):
                # Extract features
                features1 = self.extract_features(database[i]["image_path"])
                features2 = self.extract_features(database[j]["image_path"])

                if features1 is not None and features2 is not None:
                    # Calculate similarity
                    similarity = self.calculate_similarity(features1, features2)

                    # Add edge if above threshold
                    if similarity >= SIMILARITY_THRESHOLD:
                        edge = {
                            "source": i,
                            "target": j,
                            "similarity": similarity,
                            "weight": similarity,
                        }
                        network["edges"].append(edge)

        return network


def find_similar_sketches(target_image_path: str, database: List[Dict]) -> List[Dict]:
    """
    Convenience function to find similar sketches to a target image.

    Args:
        target_image_path: Path to the target image
        database: List of database entries with image information

    Returns:
        List of similar images with similarity scores
    """
    # Initialize similarity engine
    engine = ImageSimilarityEngine()

    # Find similar images
    result = engine.find_similar_images(target_image_path, database)

    return result
