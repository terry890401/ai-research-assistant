from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_token():
    client.post("/auth/register", json={
        "email": "research_test@test.com",
        "password": "testpassword123"
    })
    response = client.post("/auth/login", json={
        "email": "research_test@test.com",
        "password": "testpassword123"
    })
    return response.json()["access_token"]

def test_create_research():
    token = get_token()
    response = client.post("/research/", json={"topic": "test topic"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    assert response.json()["status"] == "pending"
    assert response.json()["topic"] == "test topic"

def test_get_research():
    token = get_token()
    create = client.post("/research/", json={"topic": "test topic"},
        headers={"Authorization": f"Bearer {token}"}
    )
    research_id = create.json()["id"]
    response = client.get(f"/research/{research_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

def test_get_all_research():
    token = get_token()
    response = client.get("/research/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_research_unauthorized():
    response = client.get("/research/")
    assert response.status_code == 401