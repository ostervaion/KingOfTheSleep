from datetime import datetime, timedelta

from sqlalchemy import func
from sqlmodel import select, Session
from math import exp, ceil
from fastapi import HTTPException, Depends
from core.database import get_session
from datetime import timezone
from core.database import engine

from schedules.battle_scheduler import (
    get_time_until_next_battle,
)

from models import CombatHistory, SleepData, ScoreHistory, UserProfile

from math import exp, ceil


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


def getStats(id: int):
    today = datetime.now(timezone.utc).date()
    start_of_day = datetime.combine(
        today,
        datetime.min.time(),
        tzinfo=timezone.utc,
    )
    end_of_day = start_of_day + timedelta(days=1)

    with Session(engine) as session :
        user = session.exec(select(SleepData).where(
            SleepData.user_id == id,
            SleepData.created_at >= start_of_day,
            SleepData.created_at < end_of_day
        )).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Sleep data not found")

    total_sleep = user.light_sleep + user.slow_wave + user.rem
    sleep_needed = user.baseline + user.debt + user.strain + user.nap

    fullfillment = total_sleep / sleep_needed
    fullfillment = 100 - 200 * abs(fullfillment - 1)

    sw = 100 * user.slow_wave / total_sleep
    sw = 100 - 4 * abs(sw - 18)

    rem = 100 * user.rem / total_sleep
    rem = 100 - 3 * abs(rem - 22.5)

    disturbances = 10 / (1 + exp(-0.25 * (user.disturbance - 15)))
    time_awake = user.awake_time / 60000
    time_awake = 10 / (1 + exp(-0.12 * (time_awake - 35)))

    vitality = fullfillment * user.performance / 100
    vitality += sw * 0.25
    vitality += rem * 0.25
    vitality*=10

    defense = sw * 0.1
    defense -= disturbances

    attack = rem * (user.consistency / 100) / 2

    speed = user.efficiency * 0.1
    speed -= time_awake
    speed*=0.5
    return {"vitality": vitality, "defense": defense, "attack": attack, "speed": speed}


def getElo(id: int, session: Session) :
    user = session.exec(select(ScoreHistory).where(
        ScoreHistory.user_id == id
    ).order_by(
        ScoreHistory.created_at.desc(),
        ScoreHistory.id.desc(),
    )).first()

    if user is None :
        return 400

    return(user.elo_score)

def gainExperience(id: int, session: Session) :
    user = session.exec(select(UserProfile).where(
        UserProfile.user_id == id
    )).first()
    if user is None :
        return
    print(user)
    user.exp += 10
    session.add(user)
    session.commit()
    session.refresh(user)

def editElo(id: int, raiting: int, session: Session) :
    elo = ScoreHistory(
        user_id = id, 
        elo_score = raiting
	)

    session.add(elo)
    session.commit()
    session.refresh(elo)

def record_combat(
    idA: int,
    idB: int,
):
    userA = getStats(idA)
    userB = getStats(idB)

    effectiveAttackA = max(userA["attack"] - userB["defense"], 1)
    effectiveAttackB = max(userB["attack"] - userA["defense"], 1)

    hitsA = ceil(userB["vitality"] / effectiveAttackA)
    hitsB = ceil(userA["vitality"] / effectiveAttackB)

    speedA = max(userA["speed"], 1)
    speedB = max(userB["speed"], 1)

    timeA = hitsA / speedA
    timeB = hitsB / speedB

    if timeA > timeB:
        winner, loser = idB, idA
    else:
        winner, loser = idA, idB

    with Session(engine) as session :
        combat = CombatHistory(
            winner_user_id=winner,
            loser_user_id=loser,
        )

        session.add(combat)
        session.commit()
        session.refresh(combat)

        ratingA = getElo(idA, session)
        ratingB = getElo(idB, session)

        expectedA = 1 / (1 + pow(10, (ratingB - ratingA) / 400))
        expectedB = 1 / (1 + pow(10, (ratingA - ratingB) / 400))

        if winner == idA :
            sA, sB = 1, 0
        else :
            sA, sB = 0, 1

        newRaitingA = ratingA + 10 * (sA - expectedA)
        newRaitingB = ratingB + 10 * (sB - expectedB)

        editElo(idA, newRaitingA, session)
        editElo(idB, newRaitingB, session)

        gainExperience(idA, session)
        gainExperience(idB, session)

