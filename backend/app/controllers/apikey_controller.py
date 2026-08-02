from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from core.database import get_session
from models import APIKey, User
from schemas import APIKeyCreate, APIKeyCreated, APIKeyPublic
from services import generate_api_key
from utils.security import get_current_active_user

router = APIRouter(prefix="/admin/apikeys", tags=["API Keys"])


@router.post("", response_model=APIKeyCreated, status_code=status.HTTP_201_CREATED)
def create_api_key(
    payload: APIKeyCreate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
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
    return session.exec(select(APIKey).where(APIKey.owner_id == current_user.id)).all()


@router.delete("/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
def revoke_api_key(
    key_id: int,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    api_key = session.get(APIKey, key_id)
    if api_key is None or api_key.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="API key no encontrada")

    api_key.active = False
    session.add(api_key)
    session.commit()