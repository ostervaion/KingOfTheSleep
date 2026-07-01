import asyncio
from datetime import datetime
from battle_state import battle_state

def run_battle():
    print(f"[BATTLE] Ejecutando batalla a las {datetime.now()}")

async def battle_scheduler(check_interval: int = 5):
    while True:
        async with battle_state.lock:
            now = datetime.now()
            if now >= battle_state.next_battle_at:
                run_battle()
                battle_state.next_battle_at += battle_state.battle_interval
        await asyncio.sleep(check_interval)