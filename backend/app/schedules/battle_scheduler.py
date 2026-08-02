import asyncio
from datetime import datetime, timedelta, timezone
from models import SleepData
from sqlmodel import select
from collections import defaultdict
from sqlmodel import Session, select
from core.database import engine
from sockets import begin_battle

BATTLE_INTERVAL_MINUTES = 120
CHECK_INTERVAL_SECONDS = 60

_next_battle_time: datetime | None = None

class BattleSchedule:
    counter = 0
    
    def __init__(self, scheduled_time: datetime, is_recurring: bool, interval_minutes: int | None = None):
        BattleSchedule.counter += 1
        self.id = BattleSchedule.counter
        self.scheduled_time = scheduled_time
        self.is_recurring = is_recurring
        self.interval_minutes = interval_minutes
        self.executed = False
        self.created_at = datetime.now(timezone.utc)
    
    def __repr__(self):
        return f"Battle(id={self.id}, time={self.scheduled_time}, recurring={self.is_recurring})"

_battle_queue: list[BattleSchedule] = []

today_battles = defaultdict(set)
today = None
battles_per_interval = 5

def _make_pairs(entries: list[SleepData]) -> list[tuple[SleepData, SleepData]]:
    """
    Empareja entradas de dos en dos.
    """
    global today_battles

    counts = defaultdict(int)
    pairs: list[tuple[SleepData, SleepData]] = []

    for i in range(len(entries)):
        player = entries[i]

        available = [
            e for e in entries
            if (
                e.id != player.id
                and counts[e.id] < battles_per_interval
                and e.username not in today_battles[player.username]
            )
        ]

        for opponent in available:
            counts[player.id] += 1
            counts[opponent.id] += 1

            today_battles[player.username].add(opponent.username)
            today_battles[opponent.username].add(player.username)

            pairs.append((player, opponent))

            if counts[player.id] >= battles_per_interval:
                break

    return pairs


async def start_battle():
    global today

    now = datetime.now(timezone.utc)
    key = now.date()

    start_of_day = datetime.combine(
        key,
        datetime.min.time(),
        tzinfo=timezone.utc,
    )
    end_of_day = start_of_day + timedelta(days=1)

    if today is None or key != today:
        today_battles.clear()
        today = key

    with Session(engine) as session:
        sleepers = session.exec(
            select(SleepData).where(
                SleepData.created_at >= start_of_day,
                SleepData.created_at < end_of_day,
            )
        ).all()

    if len(sleepers) < 2:
        print(
            f"⚠️ Matchmaking {key}: "
            f"only {len(sleepers)} entries, not enough"
        )
        return

    pairs = _make_pairs(sleepers)

    from services import record_combat
    for p1, p2 in pairs:
        print(f"🥊 {p1.username} vs {p2.username}")
        record_combat(p1.user_id, p2.user_id)
        await begin_battle(p1.username, p2.username)


def _update_next_battle_time():
    global _next_battle_time, _battle_queue
    
    _battle_queue.sort(key=lambda x: x.scheduled_time)
    
    for battle in _battle_queue:
        if not battle.executed:
            _next_battle_time = battle.scheduled_time
            return
    
    _next_battle_time = datetime.now(timezone.utc) + timedelta(minutes=BATTLE_INTERVAL_MINUTES)


async def battle_scheduler():
    global _next_battle_time, _battle_queue
    
    _next_battle_time = datetime.now(timezone.utc) + timedelta(minutes=BATTLE_INTERVAL_MINUTES)
    
    while True:
        try:
            await asyncio.sleep(CHECK_INTERVAL_SECONDS)
            
            now = datetime.now(timezone.utc)
            
            if _next_battle_time and now >= _next_battle_time:
                battle_to_execute = None
                for battle in _battle_queue:
                    if battle.scheduled_time <= now and not battle.executed:
                        battle_to_execute = battle
                        break
                
                if not battle_to_execute:
                    await start_battle()
                    _next_battle_time = now + timedelta(minutes=BATTLE_INTERVAL_MINUTES)
                else:
                    battle_to_execute.executed = True
                    
                    await start_battle()
                    
                    if battle_to_execute.is_recurring and battle_to_execute.interval_minutes:
                        next_scheduled = now + timedelta(minutes=battle_to_execute.interval_minutes)
                        new_battle = BattleSchedule(
                            scheduled_time=next_scheduled,
                            is_recurring=True,
                            interval_minutes=battle_to_execute.interval_minutes
                        )
                        _battle_queue.append(new_battle)
                    
                    _update_next_battle_time()
        
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"❌ Error en battle_scheduler: {e}")
            await asyncio.sleep(5)


async def get_time_until_next_battle() -> dict:
    global _next_battle_time
    
    if not _next_battle_time:
        _next_battle_time = datetime.now(timezone.utc) + timedelta(minutes=BATTLE_INTERVAL_MINUTES)
    
    now = datetime.now(timezone.utc)
    
    if _next_battle_time <= now:
        return {
            "milliseconds": 0,
            "seconds": 0,
            "minutes": 0,
            "hours": 0,
            "next_battle_time": _next_battle_time.isoformat(),
            "status": "battle_should_be_running"
        }
    
    time_diff = _next_battle_time - now
    total_seconds = int(time_diff.total_seconds())
    total_milliseconds = int(time_diff.total_seconds() * 1000)
    
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    return {
        "milliseconds": total_milliseconds,
        "seconds": total_seconds,
        "minutes": minutes,
        "hours": hours,
        "next_battle_time": _next_battle_time.isoformat(),
        "status": "waiting"
    }


async def schedule_extra_battle(minutes_from_now: int) -> dict:
    global _next_battle_time, _battle_queue
    
    now = datetime.now(timezone.utc)
    scheduled_time = now + timedelta(minutes=minutes_from_now)
    
    new_battle = BattleSchedule(
        scheduled_time=scheduled_time,
        is_recurring=False,
        interval_minutes=None
    )
    _battle_queue.append(new_battle)
    
    if not _next_battle_time or scheduled_time < _next_battle_time:
        _next_battle_time = scheduled_time
    
    return {
        "id": new_battle.id,
        "scheduled_time": new_battle.scheduled_time.isoformat(),
        "minutes_from_now": minutes_from_now,
        "status": "battle_scheduled"
    }


async def set_battle_interval(interval_minutes: int) -> dict:

    global BATTLE_INTERVAL_MINUTES, _next_battle_time, _battle_queue
    
    BATTLE_INTERVAL_MINUTES = interval_minutes
    
    now = datetime.now(timezone.utc)
    _next_battle_time = now + timedelta(minutes=interval_minutes)
    
    _battle_queue = [b for b in _battle_queue if not (b.is_recurring and not b.executed)]
    
    new_battle = BattleSchedule(
        scheduled_time=_next_battle_time,
        is_recurring=True,
        interval_minutes=interval_minutes
    )
    _battle_queue.append(new_battle)
    
    return {
        "interval_minutes": interval_minutes,
        "next_battle_time": _next_battle_time.isoformat(),
        "status": "interval_updated"
    }


def get_battle_interval() -> dict:
    return {
        "interval_minutes": BATTLE_INTERVAL_MINUTES,
        "check_interval_seconds": CHECK_INTERVAL_SECONDS
    }


def get_battle_queue_info() -> dict:
    return {
        "queue_size": len(_battle_queue),
        "battles": [
            {
                "id": b.id,
                "scheduled_time": b.scheduled_time.isoformat(),
                "is_recurring": b.is_recurring,
                "interval_minutes": b.interval_minutes,
                "executed": b.executed,
                "created_at": b.created_at.isoformat()
            }
            for b in sorted(_battle_queue, key=lambda x: x.scheduled_time)
        ]
    }