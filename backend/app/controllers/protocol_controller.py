from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select

from core.database import get_session
from models import (
    Protocol,
    User,
    UserProtocol,
)
from schemas import (
    ProtocolSelection,
    UserProtocolPublic,
)
from utils.security import (
    get_current_active_user,
)

router = APIRouter()


@router.post("/protocol", response_model=list[UserProtocolPublic], status_code=status.HTTP_201_CREATED)
def create_user_protocols(
    selection: ProtocolSelection,
    current_user: User = Depends(get_current_active_user),
    session=Depends(get_session),
):
    if not selection.protocol_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Protocols cant be empty",
        )

    # Deduplicamos por si el frontend envía ids repetidos
    protocol_ids = set(selection.protocol_ids)

    existing_protocols = session.exec(
        select(Protocol).where(Protocol.id.in_(protocol_ids))
    ).all()

    if len(existing_protocols) != len(protocol_ids):
        found_ids = {p.id for p in existing_protocols}
        missing = protocol_ids - found_ids
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Protocol not found: {sorted(missing)}",
        )

    new_user_protocols = [
        UserProtocol(user_id=current_user.id, protocol_id=protocol_id)
        for protocol_id in protocol_ids
    ]

    session.add_all(new_user_protocols)
    session.commit()

    for user_protocol in new_user_protocols:
        session.refresh(user_protocol)

    return new_user_protocols