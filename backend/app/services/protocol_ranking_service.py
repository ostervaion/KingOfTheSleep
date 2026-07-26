from collections import defaultdict

from sqlalchemy import func
from sqlmodel import Session, select

from models import CombatHistory, Protocol, UserProtocol
from schemas import RankedProtocolData, RankedProtocolsRead


def protocol_stats(session) -> RankedProtocolsRead:
    top = session.exec(
        select(Protocol)
        .order_by(Protocol.global_win_rate.desc())
        .limit(7)
    ).all()
    bottom = session.exec(
        select(Protocol)
        .order_by(Protocol.global_win_rate.asc())
        .limit(7)
    ).all()

	# Map top protocols with rankings 1 to N
    winner_protocols = [
        RankedProtocolData(
            ranking=idx + 1,
            protocol=p.name,
            usage=p.global_usage,
            winrate=p.global_win_rate
        )
        for idx, p in enumerate(top)
    ]
    
    # Map bottom protocols with rankings 1 to N
    loser_protocols = [
        RankedProtocolData(
            ranking=idx + 1,
            protocol=p.name,
            usage=p.global_usage,
            winrate=p.global_win_rate
        )
        for idx, p in enumerate(bottom)
    ]
    
    return RankedProtocolsRead(
        winner_protocols=winner_protocols,
        loser_protocols=loser_protocols
    )

def	recalculate_protocol_stats(session: Session) -> None:

# Usos y victorias por protocolo, para los ganadores
    winner_stats = session.exec(
        select(
            UserProtocol.protocol_id,
            func.count().label("usage"),
        )
        .join(
            CombatHistory,
            (CombatHistory.winner_user_id == UserProtocol.user_id)
            & (func.date(CombatHistory.created_at) == func.date(UserProtocol.created_at)),
        )
        .group_by(UserProtocol.protocol_id)
    ).all()

    # Usos por protocolo, para los perdedores (no suman victorias)
    loser_stats = session.exec(
        select(
            UserProtocol.protocol_id,
            func.count().label("usage"),
        )
        .join(
            CombatHistory,
            (CombatHistory.loser_user_id == UserProtocol.user_id)
            & (func.date(CombatHistory.created_at) == func.date(UserProtocol.created_at)),
        )
        .group_by(UserProtocol.protocol_id)
    ).all()

    win_count: dict[int, int] = {row.protocol_id: row.usage for row in winner_stats}
    loser_count: dict[int, int] = {row.protocol_id: row.usage for row in loser_stats}

    usage_count: dict[int, int] = defaultdict(int)
    for pid, count in win_count.items():
        usage_count[pid] += count
    for pid, count in loser_count.items():
        usage_count[pid] += count

    protocols = session.exec(select(Protocol)).all()
    for protocol in protocols:
        total_usage = usage_count.get(protocol.id, 0)
        total_wins = win_count.get(protocol.id, 0)

        protocol.global_usage = total_usage
        protocol.global_win_rate = (total_wins / total_usage) if total_usage > 0 else 0.0
        session.add(protocol)

    session.commit()