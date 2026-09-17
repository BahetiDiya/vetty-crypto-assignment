import httpx
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"

async def ping_coingecko()->dict:
    """
    Pings the Coingecko API asynchronously to check if it is reachable
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{COINGECKO_BASE_URL}/ping", timeout=5.0)
            response.raise_for_status() 

            return {"status":"reachable", "version":"v3"}

        except httpx.RequestError as exc:
            logger.error(f"Failed to reach Coingecko {exc}")
            return {"status":"unreachable", "version":"unknown"}

async def get_all_coins()-> dict:
    """
    Fetches the list of all supported coins from CoinGecko
    """

    async with httpx.AsyncClient() as client:
        try:
            # Fetching all coins from CoinGecko
            response = await client.get(f"{COINGECKO_BASE_URL}/coins/list", timeout=10.0)
            response.raise_for_status()
            return response.json()

        except httpx.RequestError as exc:
            logger.error(f"Error fetching coins {exc}")
            return []
        
