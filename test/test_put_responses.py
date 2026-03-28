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

@pytest.mark.parametrize("book_id, update_data", [
    (2, load_fixture("update_book_1", "put")),
    (8, load_fixture("update_book_2", "put")),
    (10, load_fixture("update_book_3", "put"))])
def test_update_existing_book(book_id, update_data):
    response = client.put(f"/books/{book_id}", json=update_data)
    assert response.status_code == 200
    assert response.json() == {"status_code": "200", "detailed": f"Книга успешно обновлена (ID {book_id})!"}


@pytest.mark.parametrize("book_id, update_data", [
    (-1, load_fixture("update_book_1", "put")),
    (9999999, load_fixture("update_book_2", "put"))])
def test_update_existing_book(book_id, update_data):
    response = client.put(f"/books/{book_id}", json=update_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Книга для обновления не найдена"}