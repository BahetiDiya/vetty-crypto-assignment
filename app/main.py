from fastapi import FastAPI, Query, HTTPException, BackgroundTasks
from pydantic import BaseModel, HttpUrl
import httpx
from app.services.coingecko import ping_coingecko, get_all_coins, get_all_categories,get_market_data

webhooks_db = []

class WebhookRequest(BaseModel):
    url: HttpUrl
    coin_id: str
    target_price: float

#initialize fastAPI application
app = FastAPI(
    title="Crypto market data API",
    description="API to fetch cryptocurrency market data",
    version="1.0.0"
)

#server start
@app.get("/")
async def root():
    return{
        "message":"Welcome to Crypto API. Go to /docs for Swagger documentation"
    }

@app.get("/health", tags=["System"])
async def health_check():
    """
    check health status of application and external services 
    """
    external_status = await ping_coingecko()

    return{
        "app_status":"healthy",
        "app_version":"1.0.0",
        "external_service": external_status
    }

@app.get("/coins", tags=["Crypto"])
async def list_coins(
    page_num: int = Query(1, ge=1, description="Page number for pagination"),
    per_page: int = Query(10, ge=1, description="Number of items per page")
):
    """
    List all the avaiable cryptocurrency coins with pagination
    """

    all_coins = await get_all_coins()

    start_index = (page_num - 1)*per_page
    end_index = start_index + per_page
    paginated_coins = all_coins[start_index:end_index]
    
    return {
        "page_num": page_num,
        "per_page": per_page,
        "total_coins": len(all_coins),
        "data": paginated_coins
    }

@app.get("/categories", tags=["Crypto"])
async def list_categories(
    page_num: int = Query(1, ge=1, description="Page number for pagination"),
    per_page: int = Query(10, ge=1, description="Number of items per page")
):
    """
    List all available cryptocurrency categories with pagination.
    """
    all_categories = await get_all_categories()

    start_index = (page_num - 1) * per_page
    end_index = start_index + per_page
    paginated_categories = all_categories[start_index:end_index]

    return {
        "page_num": page_num,
        "per_page": per_page,
        "total_categories": len(all_categories),
        "data": paginated_categories
    }

@app.get("/market-data", tags=["Crypto"])
async def market_data(
    coin_id: str | None = Query(None, description="Filter by Coin ID (e.g., bitcoin)"),
    category: str | None = Query(None, description="Filter by Category (e.g., smart-contract-platform)"),
    page_num: int = Query(1, ge=1, description="Page number for pagination"),
    per_page: int = Query(10, ge=1, description="Number of items per page")
):
    """
    Retrieve cryptocurrency market information in CAD.
    Requires at least one of: coin_id or category.
    """
    #validation at least one parameter must be provided
    if not coin_id and not category:
        raise HTTPException(
            status_code=400, 
            detail="At least one parameter (coin_id or category) must be provided."
        )

    data = await get_market_data(
        coin_id=coin_id, 
        category=category, 
        page=page_num, 
        per_page=per_page
    )
    
    return {
        "page_num": page_num,
        "per_page": per_page,
        "data": data
    }

async def send_webhook_notification(url: str, payload: dict):
    """
    Background task that sends HTTP post request to the user's URL
    """

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, timeout=5.0)
            print(f"Webhook fired to {url} with status {response.status_code}")

        except httpx.RequestError as exc:
            print(f"Webhook failed to reach {url}: {exc}")

@app.post("/webhooks/register", tags=["Webhooks"])
async def register_webhook (webhook: WebhookRequest):
    """
    Register webhook URL to get notified when a coin gits a specific price
    """

    webhooks_db.append({
        "url": str(webhook.url),
        "coin_id": webhook.coin_id,
        "target_price":webhook.target_price
    })
    return {
        "message": "Webhook registered successfully", "total_webhooks":len(webhooks_db)
    }

@app.post("/webhooks/trigger", tags=["Webhooks"])
async def simulate_webhook_trigger(background_tasks: BackgroundTasks):
    """
    Simulate checking prices and triggering background webhooks for testing.
    """
    if not webhooks_db:
        return {"message": "No webhooks registered yet."}

    # Simulate logic: pretend all registered coins just hit their target prices
    for wh in webhooks_db:
        payload = {
            "coin_id": wh["coin_id"],
            "alert": "Target price reached!",
            "price": wh["target_price"]
        }
        # Add to background tasks (server responds to user instantly, sends webhook in background)
        background_tasks.add_task(send_webhook_notification, wh["url"], payload)
        
    return {"message": "Background webhooks triggered successfully!"}