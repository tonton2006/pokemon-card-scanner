"""Pydantic models for request/response validation."""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class CardInfo(BaseModel):
    """Information about a Pokemon card extracted from OCR."""
    name: str = Field(..., description="Card name (e.g., 'Charizard')")
    set: Optional[str] = Field(None, description="Set name (e.g., 'Base Set')")
    number: Optional[str] = Field(None, description="Card number (e.g., '4/102')")
    rarity: Optional[str] = Field(None, description="Card rarity (e.g., 'Holo Rare')")


class PriceSource(BaseModel):
    """Price information from a single source."""
    name: str = Field(..., description="Source name (e.g., 'TCGPlayer')")
    price_usd: float = Field(..., description="Price in USD")
    condition: str = Field(default="Near Mint", description="Card condition")
    url: Optional[str] = Field(None, description="Link to listing")
    last_updated: datetime = Field(default_factory=datetime.utcnow, description="Last update time")


class PricingStatistics(BaseModel):
    """Statistical analysis of pricing data."""
    median: float = Field(..., description="Median price")
    average: float = Field(..., description="Average price")
    count: int = Field(..., description="Number of sources")
    recommendation: str = Field(default="median", description="Recommended price type")


class PricingData(BaseModel):
    """Aggregated pricing data."""
    sources: List[PriceSource] = Field(default_factory=list, description="Price sources")
    statistics: PricingStatistics = Field(..., description="Price statistics")


class ScanMetadata(BaseModel):
    """Metadata about the scan operation."""
    scan_time_ms: int = Field(..., description="Total scan time in milliseconds")
    confidence_score: float = Field(default=0.0, description="OCR confidence (0-1)")


class PricingResult(BaseModel):
    """Complete response for a card scan."""
    card: CardInfo = Field(..., description="Card information")
    pricing: PricingData = Field(..., description="Pricing data")
    metadata: ScanMetadata = Field(..., description="Scan metadata")


class ErrorDetail(BaseModel):
    """Error details."""
    code: str = Field(..., description="Error code")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[dict] = Field(None, description="Additional error context")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="Health status")
    version: str = Field(..., description="API version")
    dependencies: dict = Field(default_factory=dict, description="Dependency status")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Current time")
