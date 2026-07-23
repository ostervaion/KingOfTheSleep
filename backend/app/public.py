
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from apikeys import get_api_key_user
from database import get_session
from models import SleepData, SleepDataCreate, SleepDataPublic, User

router = APIRouter(prefix="/publicAPI", tags=["Public API"])


@router.get(
    "/sleep-data",
    response_model=list[SleepDataPublic],
    summary="Listar registros de sueño",
)
def list_sleep_data(
    limit: int = 50,
    session: Session = Depends(get_session),
    api_user: User = Depends(get_api_key_user),
):
    """Devuelve los registros de sueño más recientes del dueño de la API key."""
    statement = (
        select(SleepData)
        .where(SleepData.user_id == api_user.id)
        .order_by(SleepData.created_at.desc())
        .limit(min(limit, 200))
    )
    return session.exec(statement).all()


@router.get(
    "/sleep-data/{sleep_data_id}",
    response_model=SleepDataPublic,
    summary="Obtener un registro de sueño",
)
def get_sleep_data(
    sleep_data_id: int,
    session: Session = Depends(get_session),
    api_user: User = Depends(get_api_key_user),
):
    record = session.get(SleepData, sleep_data_id)
    if record is None or record.user_id != api_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro no encontrado")
    return record


@router.post(
    "/sleep-data",
    response_model=SleepDataPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un registro de sueño",
)
def create_sleep_data(
    payload: SleepDataCreate,
    session: Session = Depends(get_session),
    api_user: User = Depends(get_api_key_user),
):
    new_record = SleepData(
        **payload.model_dump(),
        user_id=api_user.id,
        username=api_user.username,
    )
    session.add(new_record)
    session.commit()
    session.refresh(new_record)
    return new_record


@router.put(
    "/sleep-data/{sleep_data_id}",
    response_model=SleepDataPublic,
    summary="Reemplazar un registro de sueño",
)
def update_sleep_data(
    sleep_data_id: int,
    payload: SleepDataCreate,
    session: Session = Depends(get_session),
    api_user: User = Depends(get_api_key_user),
):
    record = session.get(SleepData, sleep_data_id)
    if record is None or record.user_id != api_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro no encontrado")

    for field, value in payload.model_dump().items():
        setattr(record, field, value)

    session.add(record)
    session.commit()
    session.refresh(record)
    return record


@router.delete(
    "/sleep-data/{sleep_data_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un registro de sueño",
)
def delete_sleep_data(
    sleep_data_id: int,
    session: Session = Depends(get_session),
    api_user: User = Depends(get_api_key_user),
):
    record = session.get(SleepData, sleep_data_id)
    if record is None or record.user_id != api_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro no encontrado")

    session.delete(record)
    session.commit()