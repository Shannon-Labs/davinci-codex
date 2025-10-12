"""
Manuscript Image Analysis Module

This module implements computer vision capabilities for analyzing Leonardo da Vinci's
original manuscripts, including OCR, handwriting recognition, and image segmentation
to identify mechanical components in drawings.
"""

from __future__ import annotations

import os
from typing import Dict, List

import cv2
import numpy as np
import pytesseract

# Configuration constants
DEFAULT_IMAGE_FORMATS = [".jpg", ".jpeg", ".png", ".tiff", ".bmp"]
OCR_CONFIG = "--psm 6 --oem 3"


class ManuscriptAnalyzer:
    """
    Advanced manuscript analysis system for Leonardo da Vinci's sketches and notes.

    This class provides comprehensive image analysis capabilities including:
    - Text extraction (OCR) from mirror-script handwriting
    - Component segmentation in mechanical drawings
    - Metadata tagging based on historical context
    - Database linking of folio images to specific inventions
    """

    def __init__(self, data_directory: str = ""):
        """
        Initialize the manuscript analyzer.

        Args:
            data_directory: Directory containing manuscript images
        """
        self.data_directory = data_directory
        self.current_image = None
        self.current_image_path = ""

    def load_image(self, image_path: str) -> bool:
        """
        Load an image for analysis.

        Args:
            image_path: Path to the image file

        Returns:
            True if image loaded successfully, False otherwise
        """
        try:
            # Check if file exists
            if not os.path.exists(image_path):
                return False

            # Load image using OpenCV
            self.current_image = cv2.imread(image_path)
            if self.current_image is None:
                return False

            self.current_image_path = image_path
            return True

        except Exception:
            return False

    def extract_text(self, preprocess: bool = True) -> str:
        """
        Extract text from the current image using OCR.

        Args:
            preprocess: Whether to preprocess the image for better OCR results

        Returns:
            Extracted text as a string
        """
        if self.current_image is None:
            return ""

        # Preprocess image for better OCR results
        if preprocess:
            processed_image = self._preprocess_for_ocr(self.current_image)
        else:
            processed_image = self.current_image

        # Convert to grayscale
        gray = cv2.cvtColor(processed_image, cv2.COLOR_BGR2GRAY)

        # Use Pytesseract for OCR
        text = pytesseract.image_to_string(gray, config=OCR_CONFIG)

        return text.strip()

    def _preprocess_for_ocr(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image for optimal OCR results.

        Args:
            image: Input image array

        Returns:
            Preprocessed image array
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )

        # Invert colors (white text on black background)
        inverted = cv2.bitwise_not(thresh)

        return inverted

    def segment_components(self) -> List[Dict]:
        """
        Segment mechanical components in the manuscript drawing.

        Uses contour detection to identify potential mechanical elements.

        Returns:
            List of dictionaries containing component information
        """
        if self.current_image is None:
            return []

        # Create a copy of the image
        img_copy = self.current_image.copy()

        # Convert to grayscale
        gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)

        # Apply Canny edge detection
        edges = cv2.Canny(gray, 50, 150)

        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        components = []

        for i, contour in enumerate(contours):
            # Calculate area and perimeter
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)

            # Filter out very small or very large contours
            if area < 100 or area > 100000:
                continue

            # Get bounding box
            x, y, w, h = cv2.boundingRect(contour)

            # Calculate aspect ratio
            aspect_ratio = float(w) / h if h > 0 else 0

            # Calculate circularity
            circularity = (4 * np.pi * area) / (perimeter * perimeter) if perimeter > 0 else 0

            # Create component dictionary
            component = {
                "id": i,
                "area": area,
                "perimeter": perimeter,
                "bbox": (x, y, w, h),
                "aspect_ratio": aspect_ratio,
                "circularity": circularity,
                "center": (x + w//2, y + h//2),
                "contour": contour
            }

            components.append(component)

        return components

    def get_component_visualization(self, components: List[Dict]) -> np.ndarray:
        """
        Create a visualization of the segmented components.

        Args:
            components: List of component dictionaries

        Returns:
            Image array with components highlighted
        """
        if self.current_image is None:
            return np.array([])

        # Create a copy of the original image
        vis_img = self.current_image.copy()

        # Draw rectangles around components
        for component in components:
            x, y, w, h = component["bbox"]
            cv2.rectangle(vis_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Add component ID as text
            cv2.putText(
                vis_img,
                f"{component['id']}",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )

        return vis_img

    def analyze_folio(self, folio_id: str, image_path: str) -> Dict:
        """
        Comprehensive analysis of a manuscript folio.

        Args:
            folio_id: Identifier for the folio
            image_path: Path to the folio image

        Returns:
            Dictionary containing analysis results
        """
        # Load the image
        if not self.load_image(image_path):
            return {"error": "Failed to load image"}

        # Extract text
        text = self.extract_text()

        # Segment components
        components = self.segment_components()

        # Create visualization
        visualization = self.get_component_visualization(components)

        # Return analysis results
        return {
            "folio_id": folio_id,
            "image_path": image_path,
            "text_content": text,
            "components_count": len(components),
            "components": components,
            "visualization": visualization,
            "analysis_timestamp": "TODO: Add timestamp",
        }

    def create_database_entry(self, folio_analysis: Dict) -> Dict:
        """
        Create a database entry for the analyzed folio.

        Args:
            folio_analysis: Results from folio analysis

        Returns:
            Dictionary representing the database entry
        """
        if "error" in folio_analysis:
            return folio_analysis

        # Extract relevant information
        folio_id = folio_analysis["folio_id"]
        image_path = folio_analysis["image_path"]
        text_content = folio_analysis["text_content"]
        components_count = folio_analysis["components_count"]

        # Create database entry
        db_entry = {
            "folio_id": folio_id,
            "image_path": image_path,
            "text_content": text_content,
            "components_count": components_count,
            "components": [],
            "metadata": {
                "source": "Codex Atlanticus",  # Default source
                "date": "15th century",  # Default date
                "location": "Milan",  # Default location
                "category": "mechanical invention",  # Default category
            },
            "linked_inventions": [],
            "confidence_score": 0.0,
        }

        # Add component metadata
        for component in folio_analysis["components"]:
            component_metadata = {
                "component_id": component["id"],
                "bbox": component["bbox"],
                "area": component["area"],
                "aspect_ratio": component["aspect_ratio"],
                "circularity": component["circularity"],
                "classification": "unclassified",  # To be classified later
                "confidence_score": 0.0,
            }
            db_entry["components"].append(component_metadata)

        return db_entry

    def find_similar_folios(self, target_folio: Dict, database: List[Dict]) -> List[Dict]:
        """
        Find similar folios in the database based on visual characteristics.

        Args:
            target_folio: Target folio for comparison
            database: List of database entries

        Returns:
            List of similar folios with similarity scores
        """
        similar_folios = []

        # Compare with each folio in database
        for folio in database:
            # Calculate similarity score (simplified version)
            similarity_score = self._calculate_similarity(target_folio, folio)

            if similarity_score > 0.5:  # Threshold for similarity
                similar_folios.append({
                    "folio_id": folio["folio_id"],
                    "similarity_score": similarity_score,
                    "metadata": folio["metadata"],
                    "components_count": folio["components_count"]
                })

        # Sort by similarity score (descending)
        similar_folios.sort(key=lambda x: x["similarity_score"], reverse=True)

        return similar_folios

    def _calculate_similarity(self, folio1: Dict, folio2: Dict) -> float:
        """
        Calculate similarity between two folios.

        Args:
            folio1: First folio
            folio2: Second folio

        Returns:
            Similarity score (0.0 to 1.0)
        """
        # Simple similarity calculation based on component count and text length
        # This would be replaced with more sophisticated algorithms in production

        component_similarity = min(folio1["components_count"], folio2["components_count"]) / max(folio1["components_count"], folio2["components_count"]) if folio1["components_count"] > 0 and folio2["components_count"] > 0 else 0.0

        text1_length = len(folio1.get("text_content", ""))
        text2_length = len(folio2.get("text_content", ""))

        text_similarity = min(text1_length, text2_length) / max(text1_length, text2_length) if text1_length > 0 and text2_length > 0 else 0.0

        # Weighted average
        similarity = 0.7 * component_similarity + 0.3 * text_similarity

        return similarity


def analyze_manuscript(image_path: str, folio_id: str = "") -> Dict:
    """
    Convenience function to analyze a manuscript image.

    Args:
        image_path: Path to the manuscript image
        folio_id: Identifier for the folio

    Returns:
        Dictionary containing analysis results
    """
    # Initialize analyzer
    analyzer = ManuscriptAnalyzer()

    # Set default folio ID if not provided
    if not folio_id:
        folio_id = os.path.basename(image_path).split(".")[0]

    # Analyze the folio
    result = analyzer.analyze_folio(folio_id, image_path)

    return result
