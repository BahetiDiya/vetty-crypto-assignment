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
        
