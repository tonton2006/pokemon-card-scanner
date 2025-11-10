"""Google Cloud Vision API client wrapper."""
import os
from typing import List, Optional
from google.cloud import vision
from google.cloud.vision_v1 import types

from config import settings


class GoogleVisionClient:
    """Wrapper around Google Cloud Vision API for text detection."""

    def __init__(self):
        """Initialize the Vision API client."""
        # Set credentials if provided
        if settings.google_application_credentials:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.google_application_credentials

        self.client = vision.ImageAnnotatorClient()

    async def detect_text(self, image_bytes: bytes) -> List[str]:
        """
        Detect text in an image using Google Cloud Vision.

        Args:
            image_bytes: Image data as bytes

        Returns:
            List of detected text strings

        Raises:
            Exception: If Vision API call fails
        """
        # Create image object
        image = types.Image(content=image_bytes)

        # Perform text detection
        response = self.client.text_detection(image=image)

        if response.error.message:
            raise Exception(f"Google Vision API error: {response.error.message}")

        # Extract text annotations
        texts = []
        for text in response.text_annotations:
            texts.append(text.description)

        return texts

    def get_full_text(self, image_bytes: bytes) -> Optional[str]:
        """
        Get the full detected text from an image (synchronous version).

        Args:
            image_bytes: Image data as bytes

        Returns:
            Full text as a single string, or None if no text detected
        """
        image = types.Image(content=image_bytes)
        response = self.client.text_detection(image=image)

        if response.error.message:
            raise Exception(f"Google Vision API error: {response.error.message}")

        if response.text_annotations:
            # First annotation contains the full text
            return response.text_annotations[0].description

        return None
