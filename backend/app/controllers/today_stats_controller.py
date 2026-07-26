from collections import defaultdict
from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import and_, case, func, or_
from sqlalchemy.orm import aliased
from sqlmodel import select

from core.database import get_session
from models import CombatHistory, Protocol, SleepData, User, UserProfile, UserProtocol
from utils.security import (
    get_current_active_user,
)

router = APIRouter()



def _today_battles(session, actual_user_id: int, now: datetime):

    today = now.date()

    me = session.exec(
    select(User.username, SleepData, UserProfile.user_avatar_path, UserProfile.game_avatar_path)
    .join(SleepData, SleepData.user_id == User.id)
    .outerjoin(UserProfile, UserProfile.user_id == User.id)
    .where(User.id == actual_user_id, func.date(SleepData.created_at) == today)
    ).first()

    enemy_user = aliased(User, name="enemy_user_name")
    enemy_profile = aliased(UserProfile, name="enemy_avatar")
    enemy_sleep = aliased(SleepData, name="enemy_sleep")
    #enemy_Protocols = aliased(UserProtocol, name="enemy_Protocols")

    enemy_id = case(
        (CombatHistory.winner_user_id == actual_user_id, CombatHistory.loser_user_id),
        else_=CombatHistory.winner_user_id,
    )

    battles = session.exec(
        select(
            CombatHistory.id,
            CombatHistory.winner_user_id,
            CombatHistory.loser_user_id,
            enemy_id.label("enemy_id"),
            enemy_user.username.label("enemy_username"),
            enemy_profile.user_avatar_path.label("enemy_user_avatar"),
            enemy_profile.game_avatar_path.label("enemy_game_avatar"),
            enemy_sleep,
        )
        .join(enemy_user, enemy_user.id == enemy_id)
        .outerjoin(enemy_profile, enemy_profile.user_id == enemy_id)
        .outerjoin(
            enemy_sleep,
            and_(enemy_sleep.user_id == enemy_id,
            func.date(enemy_sleep.created_at) == today)
        )
        .where(
            or_(
                CombatHistory.winner_user_id == actual_user_id,
                CombatHistory.loser_user_id == actual_user_id,
            ),
            func.date(CombatHistory.created_at) == today,
        )
        .order_by(CombatHistory.id.desc())
    ).all()
     # --- NEW: fetch protocols used today by every enemy in this batch ---
    enemy_ids = {b.enemy_id for b in battles}

    protocols_by_user = defaultdict(list)
    if enemy_ids:
        protocol_rows = session.exec(
            select(UserProtocol.user_id, Protocol.name)
            .join(Protocol, Protocol.id == UserProtocol.protocol_id)
            .where(
                UserProtocol.user_id.in_(enemy_ids),
                func.date(UserProtocol.created_at) == today,
            )
        ).all()
        for user_id, protocol_name in protocol_rows:
            protocols_by_user[user_id].append(protocol_name)
    # ----------------------------------------------------------------
    result = {
        "me": {
            "name": me.username,
            "stats": me.SleepData.dict() if me.SleepData else None,
            "user_avatar": me.user_avatar_path,
            "game_avatar": me.game_avatar_path,
        } if me else None,
        "battles": [
            {
                "combat_id": b.id,
                "victory": b.winner_user_id == actual_user_id,
                "enemy_id": b.enemy_id,
                "enemy_username": b.enemy_username,
                "enemy_avatar": b.enemy_user_avatar,
                "enemy_stats": b.enemy_sleep.dict() if b.enemy_sleep else None,
                "enemy_protocol": protocols_by_user.get(b.enemy_id, []),
            }
            for b in battles
        ],
    }
    return result

@router.get("/battleData")
async def getBattleData(
    current_user: User = Depends(get_current_active_user),
    session=Depends(get_session)
):
    now = datetime.now(timezone.utc)
    return _today_battles(session, current_user.id, now)