from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.authors.routers import router as authors_router
from api.books.routers import router as books_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authors_router, prefix="/api/authors", tags=["Authors"])
app.include_router(books_router, prefix="/api/books", tags=["Books"])
