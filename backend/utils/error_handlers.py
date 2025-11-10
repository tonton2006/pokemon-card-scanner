"""Custom exception classes and error handlers."""


class BaseCardScannerException(Exception):
    """Base exception for all card scanner errors."""
    def __init__(self, message: str, details: dict = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class OCRFailedException(BaseCardScannerException):
    """Raised when OCR fails to extract card information."""
    pass


class CardNotFoundException(BaseCardScannerException):
    """Raised when card cannot be found in pricing database."""
    pass


class PricingUnavailableException(BaseCardScannerException):
    """Raised when pricing service is temporarily unavailable."""
    pass


class InvalidImageException(BaseCardScannerException):
    """Raised when uploaded image is invalid."""
    pass
