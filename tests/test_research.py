from fastapi.testclient import TestClient
from app.main import app
import pytest

@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client

def get_token(client):
    client.post("/auth/register", json={
        "email": "research_test@test.com",
        "password": "testpassword123"
    })
    response = client.post("/auth/login", json={
        "email": "research_test@test.com",
        "password": "testpassword123"
    })
    return response.json()["access_token"]

def test_create_research(test_client):
    token = get_token(test_client)
    response = test_client.post("/research/", json={"topic": "test topic"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    assert response.json()["status"] == "pending"
    assert response.json()["topic"] == "test topic"

def test_get_research(test_client):
    token = get_token(test_client)
    create = test_client.post("/research/", json={"topic": "test topic"},
        headers={"Authorization": f"Bearer {token}"}
    )
    research_id = create.json()["id"]
    response = test_client.get(f"/research/{research_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

def test_get_all_research(test_client):
    token = get_token(test_client)
    response = test_client.get("/research/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_research_unauthorized(test_client):
    response = test_client.get("/research/")
    assert response.status_code == 401