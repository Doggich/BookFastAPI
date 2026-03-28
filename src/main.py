from fastapi import FastAPI
from fastapi.responses import FileResponse
import uvicorn
from src.routers.books import router as books_router 

app = FastAPI()

DEFAULT_ROUTS = "Домашняя страинца 🏠"

@app.get("/", summary="Выдать домашнюю страницу", tags=[DEFAULT_ROUTS])
def main():
    return FileResponse("src/public/index.html")

app.include_router(books_router)

if __name__ == "__main__":
    uvicorn.run("src.main:app", reload=True)