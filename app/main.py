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