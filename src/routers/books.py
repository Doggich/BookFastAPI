from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_404_NOT_FOUND
from src.db import books
from src.modules.schemes import BookScheme

router = APIRouter(prefix="/books", tags=["Книги 📚"])

@router.get("/", summary="Выдать все книги")
def get_all_books():
    """
        Получить список всех книг.

        **Возвращает:** массив объектов книг. Каждый объект содержит:
        - `id` (int) – идентификатор
        - `title` (str) – название
        - `author` (str) – автор
        - `year` (int) – год издания
        - `genre` (List[str]) – жанры
        - `is_available` (bool) – доступность
        - `metadata` (dict) – доп. данные

        **Статус:** `200 OK`
        **Примечание:** если книг нет, возвращается пустой массив `[]`.
    """
    return books

@router.get("/{book_id}", summary="Выдать книгу по id")
def get_book_by_id(book_id: int):
    """
        Получить книгу по её идентификатору.

        **Параметры:**
        - `book_id` (int) – уникальный номер книги

        **Возвращает:** объект книги (поля: id, title, author, year, genre, is_available, metadata)

        **Статус-коды:**
        - `200 OK` – книга найдена
        - `404 Not Found` – книга отсутствует (тело: `{"detail": "Нет такой книги!"}`)

        **Пример запроса:** `/books/2`

        **Пример ответа (200):**
        ```json
        {
        "id": 2,
        "title": "Автостопом по галактике",
        "author": "Дуглас Адамс",
        "year": 1979,
        "genre": ["Фантастика", "Юмор"],
        "is_available": false,
        "metadata": { "pages": 224, "format": "E-book" }
        }
        ```
    """
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Нет такой книги!")

@router.post("/", summary="Добавить книгу")
def post_book(new_book: BookScheme):
    """
        Добавить новую книгу.

        **Параметры (JSON):** поля согласно схеме BookScheme (title, author, year, genre, is_available, metadata).

        **Пример запроса:** POST `/books/`
        
        ```json
        {
        "title": "Война и мир",
        "author": "Лев Толстой",
        "year": 1869,
        "genre": ["Классика", "Роман"],
        "is_available": true,
        "metadata": { "pages": 1225, "format": "Hardcover" }
        }
        ```
        Возвращает: подтверждение добавления.

        Статус-коды:

        `200 OK` – книга добавлена

        `422 Unprocessable Entity` – ошибка валидации

        Примечание: ID генерируется автоматически (текущая длина списка + 1).
    """
    books.append({
        "id": len(books) + 1,
        "title": new_book.title,
        "author": new_book.author,
        "year": new_book.year,
        "genre": new_book.genre,
        "is_available": new_book.is_available,
        "metadata": new_book.metadata
    })
    return {"status_code": "200", "detailed": "Книга успешно добавлена!"}

@router.delete("/{book_id}", summary="Удалить книгу по id")
def del_book_by_id(book_id: int):
    """
        Удалить книгу по идентификатору.

        **Параметры:**
        - `book_id` (int) – id книги для удаления

        **Пример запроса:** `/books/5`

        **Возвращает:** подтверждение удаления.

        **Статус-коды:**
        - `200 OK` – книга удалена
        - `404 Not Found` – книга не найдена

        **Пример ответа (200):**
        ```json
        {
        "status_code": "200",
        "detailed": "Книга успешно удалена!"
        }
        Примечание: после удаления ID оставшихся книг пересчитываются (начиная с 1).
    """
    book_to_remove = next((b for b in books if b["id"] == book_id), None)
    if book_to_remove is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Нет такой книги!")
    books.remove(book_to_remove)
    
    for index, book in enumerate(books, start=1):
        book["id"] = index
    return {"status_code": "200", "detailed": "Книга успешно удалена!"}

@router.put("/{book_id}", summary="Обновить книгу по id")
def put_book(book_id: int, update_book: BookScheme):
    """
        Полностью обновить информацию о книге.

        **Параметры пути:**
        - `book_id` (int) – id книги для обновления

        **Параметры тела (JSON):** поля согласно схеме BookScheme

        **Пример запроса:** PUT `/books/3`
        ```json
        {
        "title": "Новое название",
        "author": "Новый автор",
        "year": 2024,
        "genre": ["Жанр"],
        "is_available": true,
        "metadata": { "pages": 300 }
        }
        ```
        Возвращает: подтверждение обновления.

        Статус-коды:

        `200 OK` – книга обновлена

        `404 Not Found` – книга не найдена

        `422 Unprocessable Entity` – ошибка валидации

        Пример ответа (200):

        ```json
        {
        "status_code": "200",
        "detailed": "Книга успешно обновлена (ID 3)!"
        }
        ```

        Примечание: выполняется полная замена всех полей книги.
    """
    for book in books:
        if book["id"] == book_id:
            book["title"] = update_book.title
            book["author"] = update_book.author
            book["year"] = update_book.year
            book["genre"] = update_book.genre
            book["is_available"] = update_book.is_available
            book["metadata"] = update_book.metadata
            return {"status_code": "200", "detailed": f"Книга успешно обновлена (ID {book_id})!"}
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Книга для обновления не найдена")