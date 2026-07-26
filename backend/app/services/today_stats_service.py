from datetime import datetime

from sqlalchemy import and_, case, func
from sqlmodel import select

from models import CombatHistory
from schemas import TodayStatsRead


def today_stats(session, actual_user_id: int, now: datetime) -> TodayStatsRead:

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
    return stats