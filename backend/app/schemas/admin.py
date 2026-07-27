from pydantic import BaseModel


class AdminUserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None
    role: str | None = None
    active: bool | None = None
