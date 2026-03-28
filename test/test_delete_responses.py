import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

@pytest.mark.parametrize("del_id", [2, 8, 10])
def test_delete_book_by_id(del_id: int):
    response = client.delete(f"/books/{del_id}")
    assert response.status_code == 200
    assert response.json() == {"status_code": "200", "detailed": "Книга успешно удалена!"}

@pytest.mark.parametrize("not_exist_id", [99999, -1])
def test_delete_nonexistent_book(not_exist_id: int):
    response = client.delete("/books/99999")
    assert response.status_code == 404
    assert response.json() ==  {"detail": "Нет такой книги!"}



