import os

from dotenv import load_dotenv
from sqlmodel import create_engine, Session
from sqlalchemy.orm import sessionmaker

load_dotenv(".env")

SQLMODEL_DATABASE_URL = os.getenv("DOCKER_DATABASE_URL")
if not SQLMODEL_DATABASE_URL:
    raise Exception("Missing DOCKER_DATABASE_URL environment variable")

engine = create_engine(SQLMODEL_DATABASE_URL, pool_size=int(os.getenv('DATABASE_POOL_SIZE', 10)))
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session
)


def get_db():
    with SessionLocal() as session:
        yield session
