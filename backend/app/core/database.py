from sqlmodel import Session, SQLModel, create_engine, select

from core.config import DATABASE_URL, LOG

from models import Protocol

from core.config import PROTOCOL_NAMES

if (LOG == "True"):
    engine = create_engine(DATABASE_URL, echo=True)
else:
    engine = create_engine(DATABASE_URL)



def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        _seed_protocols(session)

def _seed_protocols(session: Session) -> None:
    existing = session.exec(select(Protocol.name)).all()
    existing_names = set(existing)

    for name in PROTOCOL_NAMES:
        if name not in existing_names:
            session.add(Protocol(name=name))

    session.commit()