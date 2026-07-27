from datetime import datetime, timezone

from core.database import engine

engine.echo = False

from models import User
from sqlmodel import Session, select
from utils.security import hash_password


def _next_admin_username(session: Session) -> str:
    existing = session.exec(select(User)).all()
    existing_usernames = {u.username for u in existing}

    n = 1
    while f"admin_{n}" in existing_usernames:
        n += 1

    return f"admin_{n}"


def create_admin_user():
    with Session(engine) as session:
        username = _next_admin_username(session)

        timestamp = int(datetime.now(timezone.utc).timestamp())
        plain_password = f"admin_{timestamp}"

        new_admin = User(
            username=username,
            password=hash_password(plain_password),
            email=f"{username}@example.com",
            role="admin",
            active=True,
        )

        session.add(new_admin)
        session.commit()
        session.refresh(new_admin)

        print("Admin user created successfully:")
        print(f"  username: {new_admin.username}")
        print(f"  password: {plain_password}")
        print(f"  id:       {new_admin.id}")

        return new_admin.username, plain_password


if __name__ == "__main__":
    create_admin_user()