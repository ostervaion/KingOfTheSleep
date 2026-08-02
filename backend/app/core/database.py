from sqlmodel import Session, SQLModel, create_engine, select
from core.config import DATABASE_URL, LOG, PROTOCOL_NAMES
from models import Protocol

engine = create_engine(
    DATABASE_URL,
    echo=LOG == "True",
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_timeout=10,
    pool_recycle=1800,
)

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