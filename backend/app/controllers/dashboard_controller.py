from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from core.database import get_session
from models import User, UserProfile
from services import (
    build_battle_countdown,
    build_protocol_impacts,
    build_ranking,
    build_sleep_score,
    get_experience,
    lobby_state,
    protocol_stats,
    today_stats,
)
from sockets.ws import broadcast_fetch
from utils.security import get_current_active_user

router = APIRouter()


@router.get("/")
def root():
    return {"message": "API running"}


@router.get("/dashboard/refresh")
async def trigger_dashboard_refresh():
    await broadcast_fetch()
    return {"status": "ok"}


@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    profile = session.exec(
        select(UserProfile).where(UserProfile.user_id == current_user.id)
    ).first()

    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role,
        "avatar_path": (
            f"/api{profile.user_avatar_path}"
            if profile and profile.user_avatar_path
            else None
        ),
    }


@router.get("/dashboard")
async def dashboard(
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    now = datetime.now(timezone.utc)
    user_id = current_user.id

    # Ejecuta juntas todas las operaciones síncronas de base de datos.
    ranking, current_user_ranking, current_user_prev_pos = build_ranking(
        session,
        user_id,
    )
    sleep_score = build_sleep_score(session, user_id, now)
    protocol_impact = build_protocol_impacts(session, user_id)
    lobby = lobby_state(session, user_id, now)
    experience = get_experience(session, user_id)
    today_stats_var = today_stats(session, user_id, now)
    protocols = protocol_stats(session)

    # Devuelve la conexión al pool antes de realizar cualquier await.
    session.close()

    next_battle = await build_battle_countdown(
        now,
        current_user_ranking,
        current_user_prev_pos,
    )

    return {
        "nextBattle": next_battle,
        "sleepScore": sleep_score,
        "ranking": ranking,
        "protocolImpacts": protocol_impact,
        "lobby": lobby,
        "todayStats": today_stats_var,
        "protocols": protocols,
        "experience": experience,
    }
