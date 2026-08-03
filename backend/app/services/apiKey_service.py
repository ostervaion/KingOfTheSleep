
import hashlib
import hmac
import secrets
from datetime import datetime

from fastapi import Depends, Header, HTTPException, status
from sqlmodel import Session, select

from core.config import SECRET_KEY
from core.database import get_session
from models import APIKey, User

API_KEY_PREFIX = "kots_"

def _hash_key(raw_key: str) -> str:
    return hmac.new(SECRET_KEY.encode(), raw_key.encode(), hashlib.sha256).hexdigest()


def generate_api_key() -> tuple[str, str, str]:

    raw_key = f"{API_KEY_PREFIX}{secrets.token_urlsafe(32)}"
    visible_prefix = raw_key[:12]
    return raw_key, visible_prefix, _hash_key(raw_key)


def get_api_key_user(
    x_api_key: str = Header(..., alias="X-API-Key"),
    session: Session = Depends(get_session),
) -> User:
    if not x_api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="API key required")

    key_hash = _hash_key(x_api_key)
    api_key = session.exec(select(APIKey).where(APIKey.key_hash == key_hash)).first()

    if api_key is None or not api_key.active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="API key invalid")

    api_key.last_used_at = datetime.utcnow()
    session.add(api_key)
    session.commit()

    owner = session.get(User, api_key.owner_id)
    if owner is None or not owner.active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Propietario de la key no válido")

    return owner
