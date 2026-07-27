from fastapi import APIRouter

from schedules.battle_scheduler import (
    get_battle_interval,
    get_battle_queue_info,
    get_time_until_next_battle,
)

router = APIRouter()


@router.get("/battles/info")
def get_battles_info():
    return get_battle_interval()


@router.get("/battles/queue")
def get_battles_queue():
    return get_battle_queue_info()

@router.get("/battles/time-until-next")
async def get_next_battle_time():
    return await get_time_until_next_battle()

