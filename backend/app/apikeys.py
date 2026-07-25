
import hashlib
import hmac
import secrets
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlmodel import Field, Session, SQLModel, select

from config import SECRET_KEY
from database import get_session
from models import User
from security import get_current_active_user

API_KEY_PREFIX = "kots_"


class APIKey(SQLModel, table=True):
    __tablename__ = "api_keys"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)  # etiqueta descriptiva, ej "bot de Telegram"
    key_prefix: str = Field(index=True, nullable=False)  # primeros chars, visibles en listados
    key_hash: str = Field(index=True, unique=True, nullable=False)
    owner_id: Optional[int] = Field(default=None, foreign_key="users.id", index=True)
    active: bool = Field(default=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    last_used_at: Optional[datetime] = Field(default=None)


class APIKeyCreate(SQLModel):
    name: str


class APIKeyCreated(SQLModel):
    id: int
    name: str
    api_key: str


class APIKeyPublic(SQLModel):
    id: int
    name: str
    key_prefix: str
    active: bool
    created_at: datetime
    last_used_at: Optional[datetime]


def _hash_key(raw_key: str) -> str:
    return hmac.new(SECRET_KEY.encode(), raw_key.encode(), hashlib.sha256).hexdigest()


def generate_api_key() -> tuple[str, str, str]:
    """Genera una key nueva. Devuelve (raw_key, prefix_visible, hash_para_guardar)."""
    raw_key = f"{API_KEY_PREFIX}{secrets.token_urlsafe(32)}"
    visible_prefix = raw_key[:12]
    return raw_key, visible_prefix, _hash_key(raw_key)


def get_api_key_user(
    x_api_key: str = Header(..., alias="X-API-Key"),
    session: Session = Depends(get_session),
) -> User:
    if not x_api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="API key requerida")

    key_hash = _hash_key(x_api_key)
    api_key = session.exec(select(APIKey).where(APIKey.key_hash == key_hash)).first()

    if api_key is None or not api_key.active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="API key inválida o revocada")

    api_key.last_used_at = datetime.utcnow()
    session.add(api_key)
    session.commit()

    owner = session.get(User, api_key.owner_id)
    if owner is None or not owner.active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Propietario de la key no válido")

    return owner

router = APIRouter(prefix="/admin/apikeys", tags=["API Keys"])


@router.post("", response_model=APIKeyCreated, status_code=status.HTTP_201_CREATED)
def create_api_key(
    payload: APIKeyCreate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    """Genera una API key nueva para el usuario logueado. Guarda `api_key`
    en tu cliente: no se puede volver a consultar en texto plano."""
    raw_key, prefix, key_hash = generate_api_key()

    new_key = APIKey(
        name=payload.name,
        key_prefix=prefix,
        key_hash=key_hash,
        owner_id=current_user.id,
    )
    session.add(new_key)
    session.commit()
    session.refresh(new_key)

    return APIKeyCreated(id=new_key.id, name=new_key.name, api_key=raw_key)


@router.get("", response_model=list[APIKeyPublic])
def list_api_keys(
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    """Lista tus API keys (nunca se devuelve la key en sí, solo el prefijo)."""
    return session.exec(select(APIKey).where(APIKey.owner_id == current_user.id)).all()


@router.delete("/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
def revoke_api_key(
    key_id: int,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    """Revoca (desactiva) una de tus API keys."""
    api_key = session.get(APIKey, key_id)
    if api_key is None or api_key.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="API key no encontrada")

    api_key.active = False
    session.add(api_key)
    session.commit()