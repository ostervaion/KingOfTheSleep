from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import EmailStr


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, nullable=False)
    password: str = Field(nullable=False)
    role: str = Field(default="user", nullable=False)
    active: bool = Field(default=True, nullable=False)
    email: EmailStr = Field(index=True, unique=True, nullable=False)


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
