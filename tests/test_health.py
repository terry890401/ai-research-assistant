from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import text
from app.database import engine

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status":"healthy"}

def test_database_connection():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        assert result.fetchone()[0] == 1