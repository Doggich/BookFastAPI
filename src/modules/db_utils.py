import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.data_schemes import Book, BookScheme
from typing import Final
import json

BASE_DIR: Final[Path] = Path(__file__).parent.parent
DB_PATH: Final[Path] = BASE_DIR / "database" / "DataBase.json"
 

class JsonDataBase():
    def __init__(self, path: str = None):
        if path is None:
            self.path = str(DB_PATH)
        else:
            self.path = path
    
    def read_all(self) -> Book:
      with open(self.path, "r", encoding="utf-8") as f:
        data = json.load(f)
        f.close()
      
      return data
    
    def read_by_id(self, id_: int) -> Book:
      with open(self.path, "r", encoding="utf-8") as f:
        data = json.load(f)
        f.close()

      if id_ <= 0 or id_ > len(data):
         raise IndexError(f"Invalid identifier! The identifier is out of range! It must be {1} or {len(data)}") 
      
      return data[id_ - 1]
    
    def add_book(self, book: BookScheme) -> None:
      data = self.read_all()
      new_id = max([item["id"] for item in data], default=0) + 1
      data.append({
          "id": new_id,
          "title": book.title,
          "author": book.author,
          "year": book.year,
          "genre": book.genre,
          "is_available": book.is_available,
          "metadata": book.metadata.model_dump() if hasattr(book.metadata, 'model_dump') else dict(book.metadata)
      })
      with open(self.path, "w", encoding="utf-8") as f:
          json.dump(data, f, ensure_ascii=False, indent=4)

    def delete_by_id(self, id_: int) -> None:
        data = self.read_all()
        new_data = [item for item in data if item["id"] != id_]
        if len(new_data) == len(data):
            raise IndexError(f"ID {id_} not found")
        for new_id, item in enumerate(new_data, start=1):
            item["id"] = new_id
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(new_data, f, ensure_ascii=False, indent=4)

    def update_by_id(self, id_: int, book: BookScheme) -> None:
        data = self.read_all()
        found = False
        for item in data:
            if item["id"] == id_:
                item["title"] = book.title
                item["author"] = book.author
                item["year"] = book.year
                item["genre"] = book.genre
                item["is_available"] = book.is_available
                item["metadata"] = book.metadata.model_dump() if hasattr(book.metadata, 'model_dump') else dict(book.metadata)
                found = True
                break
        if not found:
            raise IndexError(f"ID {id_} not found")
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)



db  = JsonDataBase()
print(type(db.read_all()))


# print(data[0])      
