
from pydantic import EmailStr,Field, field_validator
from sqlmodel import SQLModel


class UserCreate(SQLModel):
    username: str = Field(min_length=5, max_length=30)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        value = value.strip()

        if len(value) < 5:
            raise ValueError("Username must be at least 5 characters long")

        if not value.replace("_", "").isalnum():
            raise ValueError(
                "Username can only contain letters, numbers, and underscores"
            )

        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")

        return value

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