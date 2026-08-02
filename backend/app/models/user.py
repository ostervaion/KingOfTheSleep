
from pydantic import EmailStr
from sqlmodel import Field, SQLModel


# Tabla User basica almacenamos datos basico y contraseña Hasheada
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, nullable=False)
    password: str = Field(nullable=False)
    role: str = Field(default="user", nullable=False)
    active: bool = Field(default=True, nullable=False)
    email: EmailStr = Field(index=True, unique=True, nullable=False)