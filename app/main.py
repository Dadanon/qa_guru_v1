import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from app.api.authors.routers import router as authors_router
from app.api.books.routers import router as books_router
from app.api.smoke.routers import router as smoke_router
from app.api.seed.routers import router as seed_router

app = FastAPI()
add_pagination(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authors_router)
app.include_router(books_router)
app.include_router(smoke_router)
app.include_router(seed_router)

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
