import asyncio
from datetime import datetime, timedelta, timezone
from models import SleepData
from sqlmodel import select
from collections import defaultdict
from sqlmodel import Session, select
from core.database import engine


# Variables globales para configuración del scheduler
BATTLE_INTERVAL_MINUTES = 120  # Intervalo por defecto: 2 horas
CHECK_INTERVAL_SECONDS = 60  # Cada cuánto segundos revisar si toca ejecutar una batalla

# Variable para rastrear la próxima batalla programada
_next_battle_time: datetime | None = None

# Cola de batallas programadas (en memoria)
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

# --- Matchmaking ---
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

    for i in range(0, len(entries) - 1) :
        available = [e for e in entries if counts[e] < battles_per_interval and e.username != entries[i].username]
        for j in range(0, len(available)) :
            if (available[j].username in today_battles[entries[i].username]) :
                continue
            counts[entries[i]] += 1
            counts[available[j]] += 1
            today_battles[entries[i].username].add(available[j].username)
            today_battles[available[j].username].add(entries[i].username)
            pairs.append((entries[i], available[j]))
            if (counts[entries[i]] >= 5) :
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

    for p1, p2 in pairs:
        print(f"🥊 {p1.username} vs {p2.username}")


def _update_next_battle_time():
    """Actualiza _next_battle_time buscando la próxima batalla no ejecutada"""
    global _next_battle_time, _battle_queue
    
    # Ordenar cola por tiempo
    _battle_queue.sort(key=lambda x: x.scheduled_time)
    
    # Buscar la primera no ejecutada
    for battle in _battle_queue:
        if not battle.executed:
            _next_battle_time = battle.scheduled_time
            return
    
    # Si no hay ninguna, usar la recurrencia por defecto
    _next_battle_time = datetime.now(timezone.utc) + timedelta(minutes=BATTLE_INTERVAL_MINUTES)


async def battle_scheduler():
    """
    Scheduler que se ejecuta en segundo plano (en lifespan).
    Verifica cada CHECK_INTERVAL_SECONDS si toca ejecutar una batalla.
    No bloquea la aplicación.
    """
    global _next_battle_time, _battle_queue
    
    # Inicializar con la primera batalla recurrente
    _next_battle_time = datetime.now(timezone.utc) + timedelta(minutes=BATTLE_INTERVAL_MINUTES)
    
    while True:
        try:
            await asyncio.sleep(CHECK_INTERVAL_SECONDS)
            
            now = datetime.now(timezone.utc)
            
            # Si llegó la hora de ejecutar una batalla
            if _next_battle_time and now >= _next_battle_time:
                # Buscar la batalla a ejecutar en la cola
                battle_to_execute = None
                for battle in _battle_queue:
                    if battle.scheduled_time <= now and not battle.executed:
                        battle_to_execute = battle
                        break
                
                # Si no hay en la cola, crear una implícita (recurrencia por defecto)
                if not battle_to_execute:
                    # Ejecutar batalla implícita
                    await start_battle()
                    # Próxima recurrencia
                    _next_battle_time = now + timedelta(minutes=BATTLE_INTERVAL_MINUTES)
                else:
                    # Marcar como ejecutada
                    battle_to_execute.executed = True
                    
                    # Ejecutar la batalla
                    await start_battle()
                    
                    # Si es recurrente, crear la próxima
                    if battle_to_execute.is_recurring and battle_to_execute.interval_minutes:
                        next_scheduled = now + timedelta(minutes=battle_to_execute.interval_minutes)
                        new_battle = BattleSchedule(
                            scheduled_time=next_scheduled,
                            is_recurring=True,
                            interval_minutes=battle_to_execute.interval_minutes
                        )
                        _battle_queue.append(new_battle)
                    
                    # Actualizar próxima batalla
                    _update_next_battle_time()
        
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"❌ Error en battle_scheduler: {e}")
            await asyncio.sleep(5)  # Esperar antes de reintentar


async def get_time_until_next_battle() -> dict:
    """
    Retorna el tiempo que falta hasta la siguiente batalla en ms.
    
    Returns:
        dict: {
            "milliseconds": int,  # Milisegundos hasta la siguiente batalla
            "seconds": int,       # Segundos
            "minutes": int,       # Minutos
            "hours": int,         # Horas
            "next_battle_time": str  # ISO format datetime
        }
    """
    global _next_battle_time
    
    if not _next_battle_time:
        _next_battle_time = datetime.now(timezone.utc) + timedelta(minutes=BATTLE_INTERVAL_MINUTES)
    
    now = datetime.now(timezone.utc)
    
    if _next_battle_time <= now:
        # Si la batalla ya debería haber ocurrido
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
    """
    Programa una batalla adicional para dentro de X minutos.
    Después de ejecutarse, el ciclo normal continúa.
    
    Args:
        minutes_from_now: Cuántos minutos desde ahora ejecutar la batalla
    
    Returns:
        dict: Información sobre la batalla programada
    """
    global _next_battle_time, _battle_queue
    
    now = datetime.now(timezone.utc)
    scheduled_time = now + timedelta(minutes=minutes_from_now)
    
    # Crear nueva batalla (no recurrente)
    new_battle = BattleSchedule(
        scheduled_time=scheduled_time,
        is_recurring=False,
        interval_minutes=None
    )
    _battle_queue.append(new_battle)
    
    # Si esta batalla adicional es anterior a la próxima, actualizar _next_battle_time
    if not _next_battle_time or scheduled_time < _next_battle_time:
        _next_battle_time = scheduled_time
    
    return {
        "id": new_battle.id,
        "scheduled_time": new_battle.scheduled_time.isoformat(),
        "minutes_from_now": minutes_from_now,
        "status": "battle_scheduled"
    }


async def set_battle_interval(interval_minutes: int) -> dict:
    """
    Actualiza el intervalo de batallas recurrentes.
    
    Args:
        interval_minutes: Nuevo intervalo en minutos
    
    Returns:
        dict: Información sobre la configuración actualizada
    """
    global BATTLE_INTERVAL_MINUTES, _next_battle_time, _battle_queue
    
    BATTLE_INTERVAL_MINUTES = interval_minutes
    
    now = datetime.now(timezone.utc)
    _next_battle_time = now + timedelta(minutes=interval_minutes)
    
    # Limpiar batallas recurrentes antiguas no ejecutadas
    _battle_queue = [b for b in _battle_queue if not (b.is_recurring and not b.executed)]
    
    # Crear nueva batalla recurrente
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
    """Retorna el intervalo actual de batallas en minutos."""
    return {
        "interval_minutes": BATTLE_INTERVAL_MINUTES,
        "check_interval_seconds": CHECK_INTERVAL_SECONDS
    }


def get_battle_queue_info() -> dict:
    """Retorna información sobre las batallas programadas (para debug)."""
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