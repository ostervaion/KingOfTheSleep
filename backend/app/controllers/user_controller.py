from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select

from core.database import get_session
from models import (
    CombatHistory,
    Friend,
    ScoreHistory,
    SleepData,
    User,
    UserProfile,
    UserProtocol,
)
from schemas import (
    UserPublic,
)
from utils.security import (
    get_current_active_user,
    get_user_by_username,
)

router = APIRouter()

@router.get("/all_users", response_model=list[UserPublic])
def list_users(current_user=Depends(get_current_active_user), session=Depends(get_session)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return session.exec(select(User)).all()


@router.delete("/users/{username}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(username: str, current_user=Depends(get_current_active_user), session=Depends(get_session)):
    if current_user.username != username and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
    user = get_user_by_username(session, username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    profile = session.exec(select(UserProfile).where(UserProfile.user_id == user.id)).first()
    if profile is not None:
        session.delete(profile)

    friend_rows = session.exec(
        select(Friend).where(
            (Friend.user_id == user.id) | (Friend.friend_id == user.id)
        )
    ).all()
    for row in friend_rows:
        session.delete(row)

    sleep_rows = session.exec(select(SleepData).where(SleepData.user_id == user.id)).all()
    for row in sleep_rows:
        session.delete(row)

    score_rows = session.exec(select(ScoreHistory).where(ScoreHistory.user_id == user.id)).all()
    for row in score_rows:
        session.delete(row)

    protocol_rows = session.exec(select(UserProtocol).where(UserProtocol.user_id == user.id)).all()
    for row in protocol_rows:
        session.delete(row)

    combat_rows = session.exec(
        select(CombatHistory).where(
            (CombatHistory.winner_user_id == user.id) | (CombatHistory.loser_user_id == user.id)
        )
    ).all()
    for row in combat_rows:
        session.delete(row)

    session.delete(user)

    try:
        session.commit()
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Cant delete this user.",
        )