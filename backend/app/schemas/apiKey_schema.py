from datetime import datetime

from sqlmodel import SQLModel


class APIKeyCreate(SQLModel):
    name: str


class APIKeyCreated(SQLModel):
    id: int
    name: str
    api_key: str


class APIKeyPublic(SQLModel):
    id: int
    name: str
    key_prefix: str
    active: bool
    created_at: datetime
    last_used_at: datetime | None