"""Pricing service for aggregating card prices from multiple sources."""
from typing import List
from datetime import datetime
import statistics

from clients.pokemon_tcg import PokemonTCGClient
from models.schemas import CardInfo, PricingData, PriceSource, PricingStatistics
from utils.error_handlers import CardNotFoundException, PricingUnavailableException


class PriceService:
    """Service for aggregating Pokemon card pricing."""

    def __init__(self):
        """Initialize price service with Pokemon TCG API client."""
        self.tcg_client = PokemonTCGClient()

    async def get_pricing(self, card_info: CardInfo) -> PricingData:
        """
        Get pricing data for a Pokemon card.

        Args:
            card_info: Card information from OCR

        Returns:
            PricingData with aggregated prices

        Raises:
            CardNotFoundException: If card not found in database
            PricingUnavailableException: If pricing API is down
        """
        try:
            # Search for card in Pokemon TCG API
            card_data = await self.tcg_client.search_card(
                name=card_info.name,
                set_name=card_info.set,
                number=card_info.number
            )

            if not card_data:
                raise CardNotFoundException(
                    f"Could not find pricing for '{card_info.name}'. "
                    "This card may not be in our database yet.",
                    details={
                        "card_name": card_info.name,
                        "set": card_info.set,
                        "number": card_info.number
                    }
                )

            # Extract prices from card data
            market_prices = self.tcg_client.extract_market_prices(card_data)

            if not market_prices:
                raise PricingUnavailableException(
                    f"Found card '{card_info.name}' but pricing data is unavailable.",
                    details={
                        "card_id": card_data.get("id"),
                        "card_name": card_info.name
                    }
                )

            # Build price sources
            sources = self._build_price_sources(market_prices, card_data)

            # Calculate statistics
            statistics_data = self._calculate_statistics(sources)

            return PricingData(
                sources=sources,
                statistics=statistics_data
            )

        except (CardNotFoundException, PricingUnavailableException):
            raise
        except Exception as e:
            raise PricingUnavailableException(
                "Pricing service temporarily unavailable. Please try again.",
                details={"error": str(e)}
            )

    def _build_price_sources(self, market_prices: dict, card_data: dict) -> List[PriceSource]:
        """Build list of PriceSource objects from market prices."""
        sources = []

        # TCGPlayer prices
        if "holofoil" in market_prices and market_prices["holofoil"] > 0:
            sources.append(PriceSource(
                name="TCGPlayer (Holofoil)",
                price_usd=market_prices["holofoil"],
                condition="Near Mint",
                url=card_data.get("tcgplayer", {}).get("url"),
                last_updated=datetime.utcnow()
            ))

        if "normal" in market_prices and market_prices["normal"] > 0:
            sources.append(PriceSource(
                name="TCGPlayer (Normal)",
                price_usd=market_prices["normal"],
                condition="Near Mint",
                url=card_data.get("tcgplayer", {}).get("url"),
                last_updated=datetime.utcnow()
            ))

        if "1stEditionHolofoil" in market_prices and market_prices["1stEditionHolofoil"] > 0:
            sources.append(PriceSource(
                name="TCGPlayer (1st Ed Holofoil)",
                price_usd=market_prices["1stEditionHolofoil"],
                condition="Near Mint",
                url=card_data.get("tcgplayer", {}).get("url"),
                last_updated=datetime.utcnow()
            ))

        # CardMarket prices
        if "cardmarket" in market_prices and market_prices["cardmarket"] > 0:
            sources.append(PriceSource(
                name="CardMarket",
                price_usd=market_prices["cardmarket"],
                condition="Near Mint",
                url=card_data.get("cardmarket", {}).get("url"),
                last_updated=datetime.utcnow()
            ))

        return sources

    def _calculate_statistics(self, sources: List[PriceSource]) -> PricingStatistics:
        """Calculate pricing statistics from sources."""
        if not sources:
            return PricingStatistics(
                median=0.0,
                average=0.0,
                count=0,
                recommendation="median"
            )

        prices = [source.price_usd for source in sources]

        return PricingStatistics(
            median=statistics.median(prices),
            average=statistics.mean(prices),
            count=len(prices),
            recommendation="median"
        )


# Global price service instance
price_service = PriceService()
