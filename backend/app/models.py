from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import EmailStr
from datetime import datetime




class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, nullable=False)
    password: str = Field(nullable=False)
    role: str = Field(default="user", nullable=False)
    active: bool = Field(default=True, nullable=False)
    email: EmailStr = Field(index=True, unique=True, nullable=False)


class UserCreate(SQLModel):
    username: str
    password: str
    email: EmailStr


class UserPublic(SQLModel):
    id: int
    username: str
    role: str
    active: bool
    email: EmailStr


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: Optional[str] = None

class SleepData(SQLModel, table=True):
    __tablename__ = "sleep_data"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    user_id: Optional[int] = Field(default=None, foreign_key="users.id", index=True)
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
    user_id: Optional[int]
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
