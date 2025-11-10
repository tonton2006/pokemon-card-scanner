"""API v1 route handlers."""
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from datetime import datetime
import time

from models.schemas import HealthResponse, PricingResult, ErrorDetail, CardInfo, PricingData, ScanMetadata
from config import settings
from utils.error_handlers import (
    OCRFailedException,
    CardNotFoundException,
    PricingUnavailableException,
    InvalidImageException
)

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.

    Returns the status of the API and its dependencies.
    """
    # TODO: Add actual dependency checks (Google Vision, Pokemon TCG API)
    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        dependencies={
            "google_vision": "ok",  # Placeholder
            "pokemon_tcg_api": "ok"  # Placeholder
        },
        timestamp=datetime.utcnow()
    )


@router.post("/scan", response_model=PricingResult)
async def scan_card(image: UploadFile = File(...)):
    """
    Scan a Pokemon card and return pricing information.

    Args:
        image: Uploaded image file (JPEG/PNG)

    Returns:
        PricingResult with card info and pricing data

    Raises:
        400: Invalid image or OCR failed
        404: Card not found in database
        503: Pricing service unavailable
    """
    start_time = time.time()

    try:
        # TODO: Implement actual scanning logic
        # For now, return a stub response

        # Validate image
        if not image.content_type or not image.content_type.startswith("image/"):
            raise InvalidImageException(
                "Invalid image format. Please upload a JPEG or PNG image.",
                details={"content_type": image.content_type}
            )

        # Read image bytes
        image_bytes = await image.read()

        if len(image_bytes) > 5 * 1024 * 1024:  # 5MB limit
            raise InvalidImageException(
                "Image file too large. Maximum size is 5MB.",
                details={"size_bytes": len(image_bytes)}
            )

        # TODO: Call OCR service
        # TODO: Call pricing service

        # Stub response for now
        scan_time_ms = int((time.time() - start_time) * 1000)

        return PricingResult(
            card=CardInfo(
                name="Charizard",
                set="Base Set",
                number="4/102",
                rarity="Holo Rare"
            ),
            pricing=PricingData(
                sources=[],
                statistics={
                    "median": 0.0,
                    "average": 0.0,
                    "count": 0,
                    "recommendation": "median"
                }
            ),
            metadata=ScanMetadata(
                scan_time_ms=scan_time_ms,
                confidence_score=0.0
            )
        )

    except InvalidImageException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": {
                    "code": "INVALID_IMAGE",
                    "message": e.message,
                    "details": e.details
                }
            }
        )
    except OCRFailedException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": {
                    "code": "OCR_FAILED",
                    "message": e.message,
                    "details": e.details
                }
            }
        )
    except CardNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "code": "CARD_NOT_FOUND",
                    "message": e.message,
                    "details": e.details
                }
            }
        )
    except PricingUnavailableException as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error": {
                    "code": "PRICING_UNAVAILABLE",
                    "message": e.message,
                    "details": e.details
                }
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "An unexpected error occurred. Please try again.",
                    "details": {"error": str(e)}
                }
            }
        )
