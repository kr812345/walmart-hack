import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

# --- Inventory CRUD Tests ---
def test_inventory_crud():
    # Create
    item = {
        "item_id": "test123",
        "item_name": "Test Item",
        "category": "TestCat",
        "department": "TestDept",
        "shelf_life_days": 10,
        "days_remaining": 10,
        "initial_stock": 100,
        "current_stock": 100,
        "base_price": 10.0,
        "dynamic_price": 10.0,
        "daily_sales": 0,
        "elasticity": 0.1,
        "restock_frequency_days": 7,
        "last_restock_date": "2023-01-01",
        "next_restock_date": "2023-01-08",
        "carbon_score": 5,
        "predicted_monthly_sales": 100,
        "predicted_daily_sales": 3.3,
        "days_until_restock": 7,
        "days_stock_lasts": 30
    }
    resp = client.post("/inventory", json=item)
    assert resp.status_code == 200
    # Read
    resp = client.get(f"/inventory/{item['item_id']}")
    assert resp.status_code == 200
    # Update
    update = {"item_name": "Updated Item"}
    resp = client.put(f"/inventory/{item['item_id']}", json=update)
    assert resp.status_code == 200
    assert resp.json()["item_name"] == "Updated Item"
    # Delete
    resp = client.delete(f"/inventory/{item['item_id']}")
    assert resp.status_code == 200

# --- Simulation Endpoints ---
def test_simulation_status():
    resp = client.get("/simulation/status")
    assert resp.status_code == 200
    assert "status" in resp.json()

def test_simulation_start_stop():
    resp = client.post("/simulation/start", json={"days": 1})
    assert resp.status_code in (200, 400)  # 400 if already running
    resp = client.post("/simulation/stop")
    assert resp.status_code in (200, 400)  # 400 if not running

# --- Recommendation Endpoints ---
def test_recommendation():
    resp = client.post("/recommend")
    assert resp.status_code == 200
    assert "recommendations" in resp.json() or resp.json() == {} 