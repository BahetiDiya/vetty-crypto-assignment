from fastapi import FastAPI, Query, HTTPException
from app.services.coingecko import ping_coingecko, get_all_coins, get_all_categories,get_market_data

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