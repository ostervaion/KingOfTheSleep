from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import EmailStr
from datetime import datetime

# Tabla User basica almacenamos datos basico y contraseña Hasheada
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, nullable=False)
    password: str = Field(nullable=False)
    role: str = Field(default="user", nullable=False)
    active: bool = Field(default=True, nullable=False)
    email: EmailStr = Field(index=True, unique=True, nullable=False)


# Información RAW (sin tocar) del JSON (futura API woop). Actualmente un formulario.
# Faltaria implementar el prtocolo usado pero en principio usaremos otra tabla.
class SleepData(SQLModel, table=True):
    __tablename__ = "sleep_data"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    user_id: Optional[int] = Field(default=None, foreign_key="users.id", index=True) #FOREING KEY
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

# Historico de puntuaciones en bruto
# Pendiente el calculo de ELO (MUGI?? PASA LA FORMULA YA PLS)
# La tabla por arquitectura puede estar sin elo_score hasta que se actualice.
class ScoreHistory(SQLModel, table=True):
    __tablename__ = "score_history"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", index=True)
    sleep_score: Optional[int] = Field(default=None)
    elo_score: Optional[int] = Field(nullable=False)  # El más reciente
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

# Tabla donde relacionamos los win rates con los protocolos. Por comodidad sol ose actualzia una vez al dia.
class Protocol(SQLModel, table=True):
    __tablename__ = "protocols"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, nullable=False)
    global_win_rate: float = Field(default=0.0, nullable=False)  # se recalcula 1x al día
    global_usage: int = Field(default=0, nullable=False)  # se recalcula 1x al día

# En esta tabla por cada vinculo USER->PROTOCOLO se genera un row con la fecha(filtrado)
#  EJM: Paco123  hoy ha usado Magnesio, Luz roja, Ejercicio
#   Se generaran 3 filas con estos datos.
# Recordemos que cuando algo tenga id significa que hay una tabla que relaciona "string" con id , ejm Magnesio tendra un id unico en otra tabla.
class UserProtocol(SQLModel, table=True):
    __tablename__ = "user_protocols"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", index=True)
    protocol_id: Optional[int] = Field(default=None, foreign_key="protocols.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

# Asumimos que esto es lo que usara Mugi para gestionar avatares de juego.
class GameAvatar(SQLModel, table=True):
    __tablename__ = "game_avatars"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    path: str = Field(nullable=False)

# Creo que podemos cargarnos la tabla Game Avatar y juntarla con esto simplemente con path.
# La exp es un valor absoluto el front gestiona esto a niveles.
class UserProfile(SQLModel, table=True):
    __tablename__ = "user_profiles"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", index=True, unique=True)
    game_avatar_path: str = Field(nullable=False) #guardamos simplemente la ruta y lsito
    user_avatar_path: str = Field(nullable=False) #guardamos simplemente la ruta y lsito
    public: bool = Field(default=True, nullable=False)
    exp: Optional[int] = Field(default=0, primary_key=True)

# Tabla para gestionar el historico de batallas de forma sencilla e intuitiva.
class CombatHistory(SQLModel, table=True):
    __tablename__ = "combat_history"
    id: Optional[int] = Field(default=None, primary_key=True)
    winner_user_id: Optional[int] = Field(default=None, foreign_key="users.id", index=True)
    loser_user_id: Optional[int] = Field(default=None, foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


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
