from sqlmodel import Session, SQLModel, create_engine

from core.config import DATABASE_URL, LOG

if (LOG == "True"):
    engine = create_engine(DATABASE_URL, echo=True)
else:
    engine = create_engine(DATABASE_URL)



def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
