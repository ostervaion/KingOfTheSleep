from datetime import datetime

from sqlmodel import Field, SQLModel



class ScoreHistory(SQLModel, table=True):
    __tablename__ = "score_history"
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="users.id", index=True)
    sleep_score: int | None = Field(default=None)
    elo_score: int | None = Field(nullable=False)  
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
