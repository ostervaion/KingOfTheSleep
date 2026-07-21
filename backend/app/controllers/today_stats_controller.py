from models import (
    CombatHistory
)
from database import get_session
from sqlalchemy import func, case, and_, or_
from sqlalchemy.orm import aliased
from sqlmodel import select
from datetime import date, datetime, timedelta, timezone
from data_transfer_objects import ProtocolImpactRead, TodayStatsRead, ResumedBattleRead
from models import (
    User,
    CombatHistory,
    SleepData,
    UserProfile
)
def _today_stats(session, actual_user_id: int, now: datetime) -> TodayStatsRead:

    today = now.date()
    winsLoses = session.exec(
        select(
            func.count(case((and_(CombatHistory.winner_user_id == actual_user_id, func.date(CombatHistory.created_at) == today,), 1,))).label("wins"),
            func.count(case((and_(CombatHistory.loser_user_id == actual_user_id, func.date(CombatHistory.created_at) == today,), 1,))).label("losses"),
        )
    ).one()


    stats = TodayStatsRead(
        wins = winsLoses.wins,
        losses = winsLoses.losses,
    )
    print("////////////TODAY_STATS//////////////")
    print(stats)
    return stats

def _today_battles(session, actual_user_id: int, now: datetime):

    today = now.date()

    me = session.exec(
    select(User.username, SleepData, UserProfile.user_avatar_path, UserProfile.game_avatar_path)
    .join(SleepData, SleepData.user_id == User.id)
    .outerjoin(UserProfile, UserProfile.user_id == User.id)
    .where(User.id == actual_user_id.id, func.date(SleepData.created_at) == today)
    ).first()

    enemy_user = aliased(User)
    enemy_profile = aliased(UserProfile)
    enemy_sleep = aliased(SleepData)

    enemy_id = case(
        (CombatHistory.winner_user_id == actual_user_id.id, CombatHistory.loser_user_id),
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
            enemy_sleep
        )
        .join(enemy_user, enemy_user.id == enemy_id)
        .join(enemy_profile, enemy_profile.user_id == enemy_id)
        .join(
            enemy_sleep,
            and_(enemy_sleep.user_id == enemy_id,
            func.date(enemy_sleep.created_at) == today)
        )
        .where(
            or_(
                CombatHistory.winner_user_id == actual_user_id.id,
                CombatHistory.loser_user_id == actual_user_id.id,
            ),
            func.date(CombatHistory.created_at) == today,
        )
        .order_by(CombatHistory.id.desc())
    ).all()
    print("////////////////////////////")
    if battles:
        print(battles[0]._mapping.keys())
    print("////////////////////////////")
    print(battles)
    result = {
        "me": {
            "username": me.username,
            "sleep": me.SleepData.dict() if me.SleepData else None,
            "user_avatar": me.user_avatar_path,
            "game_avatar": me.game_avatar_path,
        } if me else None,
        "battles": [
            {
                "combat_id": b.id,
                "won": b.winner_user_id == actual_user_id.id,
                "enemy_id": b.enemy_id,
                "enemy_username": b.enemy_username,
                "enemy_user_avatar": b.enemy_user_avatar,
                "enemy_game_avatar": b.enemy_game_avatar,
                "enemy_sleep": b.enemy_sleep.dict() if b.enemy_sleep else None,
            }
            for b in battles
        ],
    }
    """
        winner = aliased(User)
        loser = aliased(User)
        last_battles = session.exec(
            select(CombatHistory.id,
                    winner.username.label("winner"),
                    loser.username.label("loser"),)
            .join(winner, CombatHistory.winner_user_id == winner.id)
            .join(loser, CombatHistory.loser_user_id == loser.id)
            .where(
                or_(
                    CombatHistory.winner_user_id == actual_user_id,
                    CombatHistory.loser_user_id == actual_user_id,
                )
                , func.date(CombatHistory.created_at) == today
            )
            .order_by(CombatHistory.id.desc())
        ).all()
        battles = []
        for id, winner, loser in last_battles:
            battles.append(ResumedBattleRead(
                id = id,
                winner_name = winner,
                loser_name = loser,
            )
            )
    """
    return result