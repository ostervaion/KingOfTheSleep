from itertools import groupby

from sqlmodel import select

from core.config import DEFAULT_SCORE
from models import (
    Protocol,
    ScoreHistory,
    UserProtocol,
)
from schemas import ProtocolImpactRead


def build_protocol_impacts(session, actual_user_id: int) -> list[ProtocolImpactRead]:
    
    statement = (
    select(Protocol.id, Protocol.name, ScoreHistory.sleep_score)
    .join(UserProtocol, UserProtocol.protocol_id == Protocol.id)
    .join(ScoreHistory, UserProtocol.user_id == ScoreHistory.user_id)
    .where(UserProtocol.user_id == actual_user_id)
    .order_by(UserProtocol.protocol_id)
    )
    protocol_user_history_list = session.exec(statement).all()

    results = []

    for (protocol_id, name), group in groupby(
        protocol_user_history_list, key=lambda row: (row.id, row.name)
    ):
        scores = [row.sleep_score for row in group]
        days_used = len(scores)
        avg_score = sum(scores) / days_used
        percentage = round(((avg_score / DEFAULT_SCORE) * 100) - 100, 2)

        results.append(
            ProtocolImpactRead(
                id=protocol_id,
                name=name,
                percentage=percentage,
                daysUsed=days_used,
            )
        )
    return results