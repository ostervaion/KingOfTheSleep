# app/schemas/protocol_impact.py
from pydantic import BaseModel


class ProtocolImpactRead(BaseModel):
    """
    DTO for the Protocol Impact widget.
    Not tied to any single table — computed by combining
    UserProtocol (usage dates) + ScoreHistory (sleep scores).
    """
    id: int          # protocol_id
    name: str        # protocol name
    percentage: float  # % impact vs baseline, computed server-side
    daysUsed: int      # count of days this protocol was used

class ResumedBattleRead(BaseModel):

    id: int
    winner_name: str
    loser_name: str
    

class TodayStatsRead(BaseModel):

    wins: int
    losses: int

class userSleepStatsRead(BaseModel):

    time_in_bed: float
    awake_time: float
    light_sleep: float
    slow_wave: float
    rem: float
    disturbance: int
    baseline: float
    debt: float
    strain: int
    respiratory_rate: int
    performance: int
    consistency: int
    efficiency: int