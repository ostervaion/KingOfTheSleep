from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select

from core.database import get_session
from models import (
    User,
)
from schedules.battle_scheduler import (
    schedule_extra_battle,
    set_battle_interval,
)
from schemas import (
    AdminUserUpdate,
    ScheduleExtraBattleRequest,
    SetBattleIntervalRequest,
    UserPublic,
)
from utils.security import (
    get_current_active_user,
    get_user_by_username,
    hash_password,
)

router = APIRouter()

@router.patch("/admin/users/{username}", response_model=UserPublic)
def admin_update_user(
    username: str,
    payload: AdminUserUpdate,
    current_user: User = Depends(get_current_active_user),
    session=Depends(get_session),
):
    _require_admin(current_user)

    user = get_user_by_username(session, username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    if payload.username and payload.username != user.username:
        existing_username = session.exec(select(User).where(User.username == payload.username)).first()
        if existing_username:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
        user.username = payload.username

    if payload.email and payload.email != user.email:
        existing_email = session.exec(select(User).where(User.email == payload.email)).first()
        if existing_email and existing_email.id != user.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        user.email = payload.email

    if payload.password:
        user.password = hash_password(payload.password)

    if payload.role is not None:
        user.role = payload.role

    if payload.active is not None:
        user.active = payload.active

    session.add(user)
    session.commit()
    session.refresh(user)

    return user

def _require_admin(current_user: User):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")

@router.post("/admin/battles/schedule-extra")
async def schedule_extra_battle_endpoint(
    request: ScheduleExtraBattleRequest,
    current_user: User = Depends(get_current_active_user),
):
    _require_admin(current_user)

    if request.minutes_from_now <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="minutes_from_now debe ser mayor a 0")

    return await schedule_extra_battle(request.minutes_from_now)


@router.post("/admin/battles/set-interval")
async def set_battle_interval_endpoint(
    request: SetBattleIntervalRequest,
    current_user: User = Depends(get_current_active_user),
):
    _require_admin(current_user)

    if request.interval_minutes <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="interval_minutes debe ser mayor a 0")

    return await set_battle_interval(request.interval_minutes)