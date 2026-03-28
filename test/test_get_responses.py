import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from fastapi.testclient import TestClient
from src.main import app
import json

client = TestClient(app)

def load_fixture(name, subdir="get"):
    path = Path(__file__).parent / "fixtures" / subdir / f"{name}.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def test_get_root():
    response = client.get("/")
    assert response.status_code == 200

def test_get_books():
    expected = load_fixture("expected_books")
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json() == expected

def test_get_book_id2():
    expected = load_fixture("expected_book_ID2")
    response = client.get("/books/2")
    assert response.status_code == 200
    assert response.json() == expected

def test_get_book_id5():
    expected = load_fixture("expected_book_ID5")
    response = client.get("/books/5")
    assert response.status_code == 200
    assert response.json() == expected

@pytest.mark.parametrize("not_exist_id", [99999, -1])
def test_get_nonexistent_book(not_exist_id: int):
    response = client.delete(f"/books/{not_exist_id}")
    assert response.status_code == 404
    assert response.json() ==  {"detail": "Нет такой книги!"}
