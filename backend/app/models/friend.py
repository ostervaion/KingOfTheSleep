from datetime import datetime

from sqlmodel import Field, SQLModel, UniqueConstraint


# Tabla de amistades. Al añadir un amigo se crean las dos filas (user_id->friend_id
# y friend_id->user_id) para que la relación sea simétrica desde el primer momento
# (sin flujo de solicitud/aceptación).
class Friend(SQLModel, table=True):
    __tablename__ = "friends"
    __table_args__ = (UniqueConstraint("user_id", "friend_id", name="uq_friend_pair"),)
 
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="users.id", index=True)
    friend_id: int | None = Field(default=None, foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)