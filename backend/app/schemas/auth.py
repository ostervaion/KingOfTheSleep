
from pydantic import EmailStr
from sqlmodel import SQLModel


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

# Payload para el PATCH de /profile. Todos los campos son opcionales:
# el usuario puede mandar solo el email, solo el password, o ambos.
class UserUpdate(SQLModel):
    email: EmailStr | None = None
    current_password: str | None = None
    new_password: str | None = None

class Token(SQLModel):
    access_token: str
    token_type: str

class TokenData(SQLModel):
    username: str | None = None