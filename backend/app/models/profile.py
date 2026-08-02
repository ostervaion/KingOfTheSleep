
from sqlmodel import Field, SQLModel


# Asumimos que esto es lo que usara Mugi para gestionar avatares de juego.
class GameAvatar(SQLModel, table=True):
    __tablename__ = "game_avatars"
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    path: str = Field(nullable=False)

# Creo que podemos cargarnos la tabla Game Avatar y juntarla con esto simplemente con path.
# La exp es un valor absoluto el front gestiona esto a niveles.
class UserProfile(SQLModel, table=True):
    __tablename__ = "user_profiles"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="users.id", unique=True, index=True)
    game_avatar_path: str | None = Field(default=None)
    user_avatar_path: str | None = Field(default=None)
    public: bool = Field(default=True)
    exp: int = Field(default=0)