from sqlmodel import select

from models import UserProfile


def get_experience(session, current_user_id: int):
    user = session.exec(
            select(UserProfile).where(
                UserProfile.user_id == current_user_id
            )
        ).first()
    return user.exp if user else 0
