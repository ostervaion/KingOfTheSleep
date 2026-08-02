from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select

from core.database import get_session
from models import (
    Friend,
    User,
)
from utils.security import (
    get_current_active_user,
    get_user_by_username,
)

router = APIRouter()

@router.get("/friends", response_model=list[str])
def list_friends(
    current_user: User = Depends(get_current_active_user),
    session=Depends(get_session),
):
    friend_rows = session.exec(
        select(Friend).where(Friend.user_id == current_user.id)
    ).all()
 
    friend_ids = [row.friend_id for row in friend_rows]
    if not friend_ids:
        return []
 
    friends = session.exec(
        select(User).where(User.id.in_(friend_ids))
    ).all()
 
    return [friend.username for friend in friends]
 
 
@router.post("/friends/{username}", status_code=status.HTTP_201_CREATED)
def add_friend(
    username: str,
    current_user: User = Depends(get_current_active_user),
    session=Depends(get_session),
):
    if username == current_user.username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No puedes añadirte a ti mismo como amigo")
 
    friend_user = get_user_by_username(session, username)
    if friend_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
 
    existing = session.exec(
        select(Friend).where(
            Friend.user_id == current_user.id,
            Friend.friend_id == friend_user.id,
        )
    ).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ya sois amigos")
 
    session.add(Friend(user_id=current_user.id, friend_id=friend_user.id))
    session.add(Friend(user_id=friend_user.id, friend_id=current_user.id))
    session.commit()
 
    return {"message": f"{username} añadido como amigo"}

@router.delete("/friends/{username}", status_code=status.HTTP_200_OK)
def delete_friend(
    username: str,
    current_user: User = Depends(get_current_active_user),
    session=Depends(get_session),
):
    if username == current_user.username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes eliminarte a ti mismo",
        )

    friend_user = get_user_by_username(session, username)

    if friend_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    friendship = session.exec(
        select(Friend).where(
            Friend.user_id == current_user.id,
            Friend.friend_id == friend_user.id,
        )
    ).first()

    reverse_friendship = session.exec(
        select(Friend).where(
            Friend.user_id == friend_user.id,
            Friend.friend_id == current_user.id,
        )
    ).first()

    if friendship is None and reverse_friendship is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No sois amigos",
        )

    if friendship is not None:
        session.delete(friendship)

    if reverse_friendship is not None:
        session.delete(reverse_friendship)

    session.commit()

    return {"message": f"{username} eliminado de tus amigos"}