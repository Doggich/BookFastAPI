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

def test_add_new_book_1():
    payload = load_fixture("book_success_1", subdir="post")
    response = client.post("/books", json=payload)
    assert response == 200
    assert response.json() == { "status_code": "200", "detailed": "Книга успешно добавлена!"}

def test_add_new_book_2():
    payload = load_fixture("book_success_2", subdir="post")
    response = client.post("/books", json=payload)
    assert response == 200
    assert response.json() == { "status_code": "200", "detailed": "Книга успешно добавлена!"}


def test_add_new_book_3():
    payload = load_fixture("book_success_3", subdir="post")
    response = client.post("/books", json=payload)
    assert response == 200
    assert response.json() == { "status_code": "200", "detailed": "Книга успешно добавлена!"}
