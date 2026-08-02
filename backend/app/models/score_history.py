from datetime import datetime

from sqlmodel import Field, SQLModel


# Historico de puntuaciones en bruto
# Pendiente el calculo de ELO (MUGI?? PASA LA FORMULA YA PLS)
# La tabla por arquitectura puede estar sin elo_score hasta que se actualice.
class ScoreHistory(SQLModel, table=True):
    __tablename__ = "score_history"
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="users.id", index=True)
    sleep_score: int | None = Field(default=None)
    elo_score: int | None = Field(nullable=False)  # El más reciente
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
