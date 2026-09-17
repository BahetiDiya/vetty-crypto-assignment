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
            #fetching all coins from CoinGecko
            response = await client.get(f"{COINGECKO_BASE_URL}/coins/list", timeout=10.0)
            response.raise_for_status()
            return response.json()

        except httpx.RequestError as exc:
            logger.error(f"Error fetching coins {exc}")
            return []

async def get_all_categories()->dict:
    """
    Fetches the list of all the cryptocurrency categories available
    """

    async with httpx.AsyncClient() as client:
        try:
            #fetching categories from CoinGecko
            response = await client.get(f"{COINGECKO_BASE_URL}/coins/categories/list", timeout=10.0)
            response.raise_for_status()
            return response.json()

        except httpx.RequestError as exc:
            logger.error(f"Error fetching categories {exc}")
            return[]
        

async def get_market_data(
        coin_id: str | None = None,
        category: str | None = None,
        page : int = 1,
        per_page : int = 10
)-> list:
    """
    Fetches cryptocurrency data in CAD
    """
    async with httpx.AsyncClient() as client:

        params ={
            "vs_currency": "cad",
            "per_page" : per_page,
            "page": page
        }
        if coin_id:
            params["ids"] = coin_id
        if category:
            params["category"] = category

        try:
            response = await client.get(
                    f"{COINGECKO_BASE_URL}/coins/markets", 
                    params=params, 
                    timeout=10.0
                )
            response.raise_for_status()
            return response.json()

        except httpx.RequestError as exc:
                logger.error(f"Error fetching market data: {exc}")
                return []
