from datetime import datetime

from sqlmodel import Field, SQLModel


# Tabla para gestionar el historico de batallas de forma sencilla e intuitiva.
class CombatHistory(SQLModel, table=True):
    __tablename__ = "combat_history"
    id: int | None = Field(default=None, primary_key=True)
    winner_user_id: int | None = Field(default=None, foreign_key="users.id", index=True)
    loser_user_id: int | None = Field(default=None, foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)