from datetime import datetime

from sqlmodel import Field, SQLModel


# Tabla donde relacionamos los win rates con los protocolos. Por comodidad sol ose actualzia una vez al dia.
class Protocol(SQLModel, table=True):
    __tablename__ = "protocols"
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, nullable=False)
    global_win_rate: float = Field(default=0.0, nullable=False)  # se recalcula 1x al día
    global_usage: int = Field(default=0, nullable=False)  # se recalcula 1x al día

# En esta tabla por cada vinculo USER->PROTOCOLO se genera un row con la fecha(filtrado)
#  EJM: Paco123  hoy ha usado Magnesio, Luz roja, Ejercicio
#   Se generaran 3 filas con estos datos.
# Recordemos que cuando algo tenga id significa que hay una tabla que relaciona "string" con id , ejm Magnesio tendra un id unico en otra tabla.
class UserProtocol(SQLModel, table=True):
    __tablename__ = "user_protocols"
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="users.id", index=True)
    protocol_id: int | None = Field(default=None, foreign_key="protocols.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)