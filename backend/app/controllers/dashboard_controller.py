from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlmodel import select

from core.database import get_session
from models import (
    User,
    UserProfile,
)
from services import (
    build_battle_countdown,
    build_protocol_impacts,
    build_ranking,
    build_sleep_score,
    lobby_state,
    protocol_stats,
    today_stats,
)
from sockets.ws import broadcast_fetch
from utils.security import (
    get_current_active_user,
)

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
    session=Depends(get_session),
):
    profile = session.exec(
        select(UserProfile).where(
            UserProfile.user_id == current_user.id
        )
    ).first()

    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role,
        "avatar_path": (
            f"/api{profile.user_avatar_path}"
            if profile
            else None
        ),
    }

@router.get("/dashboard")
async def dashboard_fake(
    current_user: User = Depends(get_current_active_user),
    session=Depends(get_session),
):
    now = datetime.now(timezone.utc)

    ranking, current_user_ranking, current_user_prev_pos = build_ranking(session, current_user.id)
    next_battle = await build_battle_countdown(now, current_user_ranking, current_user_prev_pos)
    sleep_score = build_sleep_score(session, current_user.id, now)
    protocol_impact = build_protocol_impacts(session, current_user.id)
    lobby = lobby_state(session, current_user.id, now)
    today_stats_var = today_stats(session, current_user.id, now)
    protocols = protocol_stats(session)
    return {
        "nextBattle": next_battle,
        "sleepScore": sleep_score,
        "ranking": ranking,
        "protocolImpacts": protocol_impact,
        "lobby": lobby,
        "todayStats": today_stats_var,
        "protocols": protocols
    }