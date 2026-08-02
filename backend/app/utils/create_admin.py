from datetime import datetime, timezone

from sqlmodel import Session, select

from core.database import engine
from models import User, UserProfile
from utils.security import hash_password


engine.echo = False


def _next_admin_username(session: Session) -> str:
    existing_users = session.exec(select(User)).all()
    existing_usernames = {
        user.username
        for user in existing_users
    }

    number = 1

    while f"admin_{number}" in existing_usernames:
        number += 1

    return f"admin_{number}"


def create_admin_user():
    with Session(engine) as session:
        try:
            username = _next_admin_username(session)

            timestamp = int(
                datetime.now(timezone.utc).timestamp()
            )

            plain_password = f"admin_{timestamp}"

            new_admin = User(
                username=username,
                password=hash_password(plain_password),
                email=f"{username}@example.com",
                role="admin",
                active=True,
            )

            session.add(new_admin)
            session.flush()

            admin_profile = UserProfile(
                user_id=new_admin.id,
                exp=0,
                public=True,
            )

            session.add(admin_profile)

            session.commit()

            session.refresh(new_admin)
            session.refresh(admin_profile)

            print("Admin user created successfully:")
            print(f"  username: {new_admin.username}")
            print(f"  password: {plain_password}")
            print(f"  id:       {new_admin.id}")
            print(f"  exp:      {admin_profile.exp}")

            return new_admin.username, plain_password

        except Exception:
            session.rollback()
            raise


if __name__ == "__main__":
    create_admin_user()