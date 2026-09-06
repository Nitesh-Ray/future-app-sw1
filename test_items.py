# tests/test_items.py
# Automated tests for the CRUD API using pytest and FastAPI TestClient.

from fastapi.testclient import TestClient
from main import app
from database import Base, engine

# Create a fresh test client
client = TestClient(app)

# Set up and tear down the database before each test
def setup_function():
    # Create tables
    Base.metadata.create_all(bind=engine)

def teardown_function():
    # Drop all tables to start clean next test
    Base.metadata.drop_all(bind=engine)

# ----------------------------
# Test creating an item
# ----------------------------
def test_create_item():
    response = client.post(
        "/items/",
        json={"name": "Test Item", "description": "A test", "price": 10.5}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["price"] == 10.5
    assert "id" in data

# ----------------------------
# Test reading all items (list)
# ----------------------------
def test_read_items():
    # Add two items first
    client.post("/items/", json={"name": "Item 1", "price": 5.0})
    client.post("/items/", json={"name": "Item 2", "price": 7.5})
    response = client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

# ----------------------------
# Test reading a single item
# ----------------------------
def test_read_item():
    # Create an item and get its id
    create_resp = client.post("/items/", json={"name": "Read Me", "price": 99.99})
    item_id = create_resp.json()["id"]
    # Fetch it
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Read Me"

# ----------------------------
# Test updating an item
# ----------------------------
def test_update_item():
    create_resp = client.post("/items/", json={"name": "Old Name", "price": 1.0})
    item_id = create_resp.json()["id"]
    update_resp = client.put(
        f"/items/{item_id}",
        json={"name": "New Name", "description": "Updated", "price": 2.0}
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["name"] == "New Name"
    assert update_resp.json()["price"] == 2.0

# ----------------------------
# Test deleting an item
# ----------------------------
def test_delete_item():
    create_resp = client.post("/items/", json={"name": "Delete Me", "price": 3.0})
    item_id = create_resp.json()["id"]
    delete_resp = client.delete(f"/items/{item_id}")
    assert delete_resp.status_code == 200
    # Verify it's gone
    get_resp = client.get(f"/items/{item_id}")
    assert get_resp.status_code == 404

# ----------------------------
# Test 404 for non-existent item
# ----------------------------
def test_read_item_not_found():
    response = client.get("/items/9999")
    assert response.status_code == 404