
from datetime import datetime, timedelta

from sqlalchemy import func
from sqlmodel import select

from models import (
    SleepData,
)
from schedules.battle_scheduler import (
    get_time_until_next_battle,
)


async def build_battle_countdown(now: datetime, current_user_ranking, current_user_prev_pos):
    battle_info = await get_time_until_next_battle()

    tomorrow_midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    seconds_until_eod = int((tomorrow_midnight - now).total_seconds())

    delta_ranking = 0
    if current_user_prev_pos and current_user_ranking:
        delta_ranking = current_user_prev_pos - current_user_ranking

    return {
        "currentRanking": current_user_ranking or 0,
        "seconds": battle_info.get("seconds", 0),
        "endDay": seconds_until_eod,
        "deltaRanking": delta_ranking,
    }

def lobby_state(session, current_user_id: int, now: datetime) -> bool:
    today = now.date()

    today_data = session.exec(
        select(SleepData).where(
            SleepData.user_id == current_user_id,
            func.date(SleepData.created_at) == today,
        )
    ).first()

    return today_data is not None