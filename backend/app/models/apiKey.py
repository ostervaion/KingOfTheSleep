from datetime import datetime

from sqlmodel import Field, SQLModel


class APIKey(SQLModel, table=True):
    __tablename__ = "api_keys"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    key_prefix: str = Field(index=True, nullable=False)
    key_hash: str = Field(index=True, unique=True, nullable=False)
    owner_id: int | None = Field(default=None, foreign_key="users.id", index=True)
    active: bool = Field(default=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    last_used_at: datetime | None = Field(default=None)