from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test the health endpoint to ensure it returns 200 and correct keys."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "app_status" in data
    assert data["app_status"] == "healthy"

def test_list_coins():
    """Test the coins list endpoint with pagination."""
    response = client.get("/coins?page_num=1&per_page=5")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "total_coins" in data

def test_list_categories():
    """Test the categories list endpoint with pagination."""
    response = client.get("/categories?page_num=1&per_page=5")
    assert response.status_code == 200
    assert "data" in response.json()

def test_market_data_valid():
    """Test market data with a valid coin_id."""
    response = client.get("/market-data?coin_id=bitcoin")
    assert response.status_code == 200
    assert "data" in response.json()

def test_market_data_invalid():
    """Test market data without any parameters to ensure it throws a 400 error."""
    response = client.get("/market-data")
    assert response.status_code == 400
    assert "detail" in response.json()

def test_webhooks_flow():
    """Test registering a webhook and then triggering it."""
    #test registration
    payload = {
        "url": "https://webhook.site/test-url",
        "coin_id": "bitcoin",
        "target_price": 100000.0
    }
    register_response = client.post("/webhooks/register", json=payload)
    assert register_response.status_code == 200
    assert "successfully" in register_response.json()["message"]

    #test triggering
    trigger_response = client.post("/webhooks/trigger")
    assert trigger_response.status_code == 200
    assert "successfully" in trigger_response.json()["message"]
