"""Pokemon TCG API client wrapper."""
import httpx
from typing import Optional, Dict, List

from config import settings


class PokemonTCGClient:
    """Wrapper around Pokemon TCG API for card lookups and pricing."""

    def __init__(self):
        """Initialize the Pokemon TCG API client."""
        self.base_url = settings.pokemon_tcg_api_url
        self.api_key = settings.pokemon_tcg_api_key
        self.headers = {}

        if self.api_key:
            self.headers["X-Api-Key"] = self.api_key

    async def search_card(
        self,
        name: str,
        set_name: Optional[str] = None,
        number: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Search for a Pokemon card by name, set, and number.

        Args:
            name: Card name (e.g., "Charizard")
            set_name: Set name (e.g., "Base Set")
            number: Card number (e.g., "4/102")

        Returns:
            Card data dict if found, None otherwise
        """
        # Build search query
        query_parts = [f'name:"{name}"']

        if set_name:
            query_parts.append(f'set.name:"{set_name}"')

        if number:
            query_parts.append(f'number:"{number}"')

        query = " ".join(query_parts)

        async with httpx.AsyncClient(timeout=settings.pricing_timeout_ms / 1000) as client:
            try:
                response = await client.get(
                    f"{self.base_url}/cards",
                    params={"q": query},
                    headers=self.headers
                )
                response.raise_for_status()
                data = response.json()

                if data.get("data") and len(data["data"]) > 0:
                    # Return first match
                    return data["data"][0]

                return None

            except httpx.TimeoutException:
                raise Exception("Pokemon TCG API request timed out")
            except httpx.HTTPStatusError as e:
                raise Exception(f"Pokemon TCG API error: {e.response.status_code}")
            except Exception as e:
                raise Exception(f"Failed to search Pokemon TCG API: {str(e)}")

    async def get_card_by_id(self, card_id: str) -> Optional[Dict]:
        """
        Get card details by ID.

        Args:
            card_id: Pokemon TCG API card ID

        Returns:
            Card data dict if found, None otherwise
        """
        async with httpx.AsyncClient(timeout=settings.pricing_timeout_ms / 1000) as client:
            try:
                response = await client.get(
                    f"{self.base_url}/cards/{card_id}",
                    headers=self.headers
                )
                response.raise_for_status()
                data = response.json()

                return data.get("data")

            except httpx.HTTPStatusError:
                return None
            except Exception as e:
                raise Exception(f"Failed to get card from Pokemon TCG API: {str(e)}")

    def extract_market_prices(self, card_data: Dict) -> Dict[str, float]:
        """
        Extract market prices from card data.

        Args:
            card_data: Card data from Pokemon TCG API

        Returns:
            Dict with price information
        """
        prices = {}

        if "tcgplayer" in card_data and "prices" in card_data["tcgplayer"]:
            tcg_prices = card_data["tcgplayer"]["prices"]

            # Try to get holofoil or normal price
            if "holofoil" in tcg_prices:
                prices["holofoil"] = tcg_prices["holofoil"].get("market", 0.0)
            elif "normal" in tcg_prices:
                prices["normal"] = tcg_prices["normal"].get("market", 0.0)
            elif "1stEditionHolofoil" in tcg_prices:
                prices["1stEditionHolofoil"] = tcg_prices["1stEditionHolofoil"].get("market", 0.0)

        if "cardmarket" in card_data and "prices" in card_data["cardmarket"]:
            cm_prices = card_data["cardmarket"]["prices"]
            prices["cardmarket"] = cm_prices.get("averageSellPrice", 0.0)

        return prices
