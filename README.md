# Crypto Market Data API (Vetty Assignment)

A production-ready RESTful API built with FastAPI that aggregates cryptocurrency data from the CoinGecko API. This project implements mandatory technical requirements including in-memory caching, background webhooks, and comprehensive unit testing.

##  Features

* **RESTful Endpoints:** Fetch list of coins, categories, and live market data (in CAD).
* **Smart Caching:** Integrated `cachetools` (TTLCache) with a 5-minute TTL for `/coins` and `/categories` to optimize performance and prevent rate-limiting.
* **Background Webhooks:** Register endpoints and simulate background event triggers using FastAPI's `BackgroundTasks`.
* **High Reliability:** Automated unit tests written with `pytest`, achieving **>80% code coverage**.

##  Tech Stack

* **Framework:** FastAPI
* **HTTP Client:** HTTPX (Async)
* **Caching:** Cachetools
* **Testing:** Pytest, Pytest-cov
* **Data Validation:** Pydantic

##  Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/BahetiDiya/vetty-crypto-assignment.git
   cd vetty-assignment
Create and activate a virtual environment:

Bash
python -m venv crypto_venv
# For Windows:
crypto_venv\Scripts\activate
# For Mac/Linux:
source crypto_venv/bin/activate
Install the dependencies:

Bash
pip install -r requirements.txt
Running the Server
Start the FastAPI application using Uvicorn:

Bash
uvicorn app.main:app --reload
Once the server is running, you can access the interactive API documentation (Swagger UI) at:
http://127.0.0.1:8000/docs

Running Tests
To verify the test coverage (>80%), run the following command:

Bash
pytest --cov=app tests/