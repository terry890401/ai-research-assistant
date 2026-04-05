def test_search_web():
    from app.agent import search_web
    result = search_web("Python FastAPI")
    assert isinstance(result, str)
    assert len(result) > 0