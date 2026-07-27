from pydantic import BaseModel


class ScheduleExtraBattleRequest(BaseModel):
    minutes_from_now: int = 5


class SetBattleIntervalRequest(BaseModel):
    interval_minutes: int = 120

class ResumedBattleRead(BaseModel):

    id: int
    winner_name: str
    loser_name: str