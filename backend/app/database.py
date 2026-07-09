from sqlalchemy import inspect, text
from sqlmodel import Session, SQLModel, create_engine
from config import DATABASE_URL
import models  # ensures all table classes are registered before create_all runs

engine = create_engine(DATABASE_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
