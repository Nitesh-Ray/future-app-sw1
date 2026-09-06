# tests/test_auth.py
# Tests for authentication flow.

from fastapi.testclient import TestClient
from main import app
from database import Base, engine

client = TestClient(app)

def setup_function():
    Base.metadata.create_all(bind=engine)

def teardown_function():
    Base.metadata.drop_all(bind=engine)

def test_register_and_login():
    # Register a new user
    reg_resp = client.post("/register", json={"username": "testuser", "password": "secret"})
    assert reg_resp.status_code == 200
    assert reg_resp.json()["username"] == "testuser"

    # Login with correct credentials
    login_resp = client.post("/login", data={"username": "testuser", "password": "secret"})
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]
    assert token is not None

    # Try to access protected endpoint without token
    no_auth = client.get("/items/")
    assert no_auth.status_code == 401

    # Access with token
    headers = {"Authorization": f"Bearer {token}"}
    auth_resp = client.get("/items/", headers=headers)
    assert auth_resp.status_code == 200

def test_login_wrong_password():
    client.post("/register", json={"username": "user2", "password": "right"})
    resp = client.post("/login", data={"username": "user2", "password": "wrong"})
    assert resp.status_code == 401