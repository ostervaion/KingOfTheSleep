from datetime import datetime

from sqlmodel import Field, SQLModel



class SleepData(SQLModel, table=True):
    __tablename__ = "sleep_data"

    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    user_id: int | None = Field(default=None, foreign_key="users.id", index=True) 
    username: str = Field(index=True, nullable=False)

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