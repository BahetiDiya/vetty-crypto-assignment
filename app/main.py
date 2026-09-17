from fastapi import FastAPI, Query
from app.services.coingecko import ping_coingecko, get_all_coins 

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

