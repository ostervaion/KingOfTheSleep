from datetime import datetime, timedelta

from sqlmodel import select

from core.config import DAY_NAMES
from models import (
    SleepData,
)

def build_sleep_score(session, current_user_id: int, now: datetime):
    seven_days_ago = now - timedelta(days=7)
    records = session.exec(
        select(SleepData).where(
            SleepData.user_id == current_user_id,
            SleepData.created_at >= seven_days_ago,
        ).order_by(SleepData.created_at.asc())
    ).all()

    sleep_by_date = {}
    for record in records:
        sleep_by_date.setdefault(record.created_at.date(), []).append(record.performance)

    labels = []
    scores = []
    for days_back in range(6, -1, -1):
        target_date = now.date() - timedelta(days=days_back)
        labels.append(DAY_NAMES[target_date.weekday()])

        valid_scores = [s for s in sleep_by_date.get(target_date, []) if s is not None]
        if valid_scores:
            avg_score = int(sum(valid_scores) / len(valid_scores))
            scores.append(max(0, min(100, avg_score)))
        else:
            scores.append(0)

    return {"labels": labels, "scores": scores}