from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_search_web():
    from app.agent import search_web
    result = search_web.invoke({"query": "Python FastAPI"})  # ← 改成 .invoke()
    assert isinstance(result, str)
    assert len(result) > 0

def test_run_research():
    from app.agent import run_research
    result = run_research("人工智慧發展趨勢")
    
    assert isinstance(result, dict)
    assert "title" in result
    assert "summary" in result
    assert "key_points" in result
    assert "conclusion" in result