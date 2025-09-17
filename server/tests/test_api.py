from fastapi.testclient import TestClient
from app.main import app

c = TestClient(app)

def test_health():
    r = c.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_trending_shape():
    r = c.get("/trending?k=3")
    assert r.status_code == 200
    items = r.json()["items"]
    assert isinstance(items, list) and len(items) <= 3
    if items:
        assert "item_id" in items[0] and "score" in items[0]
