import asyncio
from datetime import datetime, timedelta

class BattleState:
    def __init__(self):
        self.next_battle_at: datetime = datetime.now() + timedelta(hours=2)
        self.battle_interval: timedelta = timedelta(hours=2)  # tiempo a sumar tras cada batalla
        self.lock = asyncio.Lock()

battle_state = BattleState()