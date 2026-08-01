from fastapi.testclient import TestClient
from src.main import app
from src.storage import store

client = TestClient(app)


def setup_function():
    """Reset the store before every test so tests don't affect each other."""
    store._expenses.clear()


def test_add_expense_returns_201_and_id():
    resp = client.post("/expenses", json={
        "title": "Groceries", "amount": 45.5, "category": "food", "date": "2026-08-01"
    })
    assert resp.status_code == 201
    body = resp.json()
    assert body["title"] == "Groceries"
    assert "id" in body


def test_negative_amount_rejected():
    resp = client.post("/expenses", json={
        "title": "Bad", "amount": -5, "category": "food", "date": "2026-08-01"
    })
    assert resp.status_code == 422


def test_list_all_expenses():
    client.post("/expenses", json={"title": "A", "amount": 10, "category": "food", "date": "2026-08-01"})
    client.post("/expenses", json={"title": "B", "amount": 20, "category": "transport", "date": "2026-08-01"})
    resp = client.get("/expenses")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_filter_by_category():
    client.post("/expenses", json={"title": "A", "amount": 10, "category": "food", "date": "2026-08-01"})
    client.post("/expenses", json={"title": "B", "amount": 20, "category": "transport", "date": "2026-08-01"})
    resp = client.get("/expenses", params={"category": "food"})
    body = resp.json()
    assert len(body) == 1
    assert body[0]["category"] == "food"


def test_total_overall_and_by_category():
    client.post("/expenses", json={"title": "A", "amount": 10, "category": "food", "date": "2026-08-01"})
    client.post("/expenses", json={"title": "B", "amount": 20, "category": "transport", "date": "2026-08-01"})

    total = client.get("/expenses/total").json()
    assert total["total"] == 30

    food_total = client.get("/expenses/total", params={"category": "food"}).json()
    assert food_total["total"] == 10


def test_delete_expense():
    added = client.post("/expenses", json={
        "title": "ToDelete", "amount": 5, "category": "misc", "date": "2026-08-01"
    }).json()

    delete_resp = client.delete(f"/expenses/{added['id']}")
    assert delete_resp.status_code == 204

    # deleting again should now 404
    second_delete = client.delete(f"/expenses/{added['id']}")
    assert second_delete.status_code == 404
