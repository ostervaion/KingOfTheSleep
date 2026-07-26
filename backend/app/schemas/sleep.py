from datetime import datetime

from pydantic import BaseModel
from sqlmodel import SQLModel


class SleepDataCreate(SQLModel):
    time_in_bed: float
    awake_time: float
    light_sleep: float
    slow_wave: float
    rem: float

    disturbance: int
    baseline: float
    debt: float
    strain: int
    nap: float

    respiratory_rate: int
    performance: int
    consistency: int
    efficiency: int


class SleepDataPublic(SQLModel):
    id: int
    created_at: datetime
    user_id: int | None
    username: str

    time_in_bed: float
    awake_time: float
    light_sleep: float
    slow_wave: float
    rem: float

    disturbance: int
    baseline: float
    debt: float
    strain: int
    nap: float

    respiratory_rate: int
    performance: int
    consistency: int
    efficiency: int

class UserSleepStatsRead(BaseModel):

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