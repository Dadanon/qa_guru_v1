import os

from dotenv import load_dotenv
from sqlmodel import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlmodel import Session

load_dotenv(".env")

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
if not SQLALCHEMY_DATABASE_URL:
    raise Exception("Missing DATABASE_URL environment variable")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session
)

Base = declarative_base()


def get_db():
    with SessionLocal() as session:
        yield session
