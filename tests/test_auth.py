from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_success():
    response = client.post("/auth/register", json={
        "email": "research_test@test.com",
        "password": "testpassword123"
    })
    assert response.status_code in [201, 409]

def test_login_success():
    client.post("/auth/register", json={
        "email": "research_test@test.com",
        "password": "testpassword123"
    })
    response = client.post("/auth/login", json={
        "email": "research_test@test.com",
        "password": "testpassword123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password():
    client.post("/auth/register", json={
        "email": "research_test@test.com",
        "password": "testpassword123"
    })
    response = client.post("/auth/login", json={
        "email": "research_test@test.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

def test_get_me():
    client.post("/auth/register", json={
        "email": "research_test@test.com",
        "password": "testpassword123"
    })
    login = client.post("/auth/login", json={
        "email": "research_test@test.com",
        "password": "testpassword123"
    })
    token = login.json()["access_token"]
    response = client.get("/auth/me", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "research_test@test.com"