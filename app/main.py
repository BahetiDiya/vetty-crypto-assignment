from fastapi import FastAPI

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
    #make external service dynamic after connecting to the CoinGecko API
    return{
        "app_status":"healthy",
        "app_version":"1.0.0",
        "external_service":{
            "status":"reachable",
            "version":"v3" 
        }
    }