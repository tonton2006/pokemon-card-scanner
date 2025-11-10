"""OCR service for extracting card information from images."""
from typing import Optional

from clients.google_vision import GoogleVisionClient
from models.schemas import CardInfo
from services.card_parser import parse_full_card_info
from utils.error_handlers import OCRFailedException


class OCRService:
    """Service for orchestrating OCR and card info extraction."""

    def __init__(self):
        """Initialize OCR service with Google Vision client."""
        self.vision_client = GoogleVisionClient()

    async def extract_card_info(self, image_bytes: bytes) -> CardInfo:
        """
        Extract Pokemon card information from image.

        Args:
            image_bytes: Image data as bytes

        Returns:
            CardInfo object with extracted data

        Raises:
            OCRFailedException: If OCR fails or no card info found
        """
        try:
            # Get full text from image
            full_text = self.vision_client.get_full_text(image_bytes)

            if not full_text or len(full_text.strip()) < 10:
                raise OCRFailedException(
                    "Could not detect sufficient text in image. "
                    "Please ensure the card is clearly visible and well-lit.",
                    details={"detected_text_length": len(full_text) if full_text else 0}
                )

            # Parse card information from text
            card_data = parse_full_card_info(full_text)

            # Validate we got at least a card name
            if not card_data.get("name"):
                raise OCRFailedException(
                    "Could not identify card name from image. "
                    "Please ensure the card name is clearly visible.",
                    details={
                        "detected_text": full_text[:200],  # First 200 chars
                        "parsed_data": card_data
                    }
                )

            return CardInfo(
                name=card_data["name"],
                set=card_data.get("set"),
                number=card_data.get("number"),
                rarity=card_data.get("rarity")
            )

        except OCRFailedException:
            raise
        except Exception as e:
            raise OCRFailedException(
                f"OCR processing failed: {str(e)}",
                details={"error": str(e)}
            )


# Global OCR service instance
ocr_service = OCRService()
