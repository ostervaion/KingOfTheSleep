from datetime import datetime, time, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select
from pydantic import BaseModel

from config import ACCESS_TOKEN_EXPIRE_MINUTES
from database import get_session
from models import SleepData, SleepDataCreate, SleepDataPublic, Token, User, UserCreate, UserPublic
from security import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    get_user_by_username,
    hash_password,
)
from battle_scheduler import (
    get_time_until_next_battle,
    schedule_extra_battle,
    set_battle_interval,
    get_battle_interval,
    get_battle_queue_info,
)

router = APIRouter()


@router.get("/")
def root():
    return {"message": "API running"}


@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, session=Depends(get_session)):
    existing_username = session.exec(select(User).where(User.username == user_data.username)).first()
    if existing_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    existing_email = session.exec(select(User).where(User.email == user_data.email)).first()
    if existing_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    new_user = User(
        username=user_data.username,
        password=hash_password(user_data.password),
        email=user_data.email,
        role="admin",
        active=True,
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session=Depends(get_session)):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id, "role": user.role},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserPublic)
def read_me(current_user=Depends(get_current_active_user)):
    return current_user


@router.get("/all_users", response_model=list[UserPublic])
def list_users(current_user=Depends(get_current_active_user), session=Depends(get_session)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return session.exec(select(User)).all()


@router.get("/admin")
def admin_only(current_user=Depends(get_current_active_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return {"message": f"Welcome admin {current_user.username}"}


@router.delete("/users/{username}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(username: str, current_user=Depends(get_current_active_user), session=Depends(get_session)):
    if current_user.username != username and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
    user = get_user_by_username(session, username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    session.delete(user)
    session.commit()


@router.get("/dashboard")
def dashboard_fake():
    return {
        "nextBattle": {
            "currentRanking": 12,
            "seconds": 999999,
            "endDay": 1234,
            "deltaRanking": 34,
        },
        "sleepScore": {
            "labels": ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"],
            "scores": [75, 80, 70, 90, 73, 82, 80],
        },
    }

@router.post("/sleep-data", response_model=SleepDataPublic, status_code=status.HTTP_201_CREATED)
def create_sleep_data(
    sleep_data: SleepDataCreate,
    current_user: User = Depends(get_current_active_user),
    session=Depends(get_session),
):
    new_sleep_data = SleepData(
        time_in_bed=sleep_data.time_in_bed,
        awake_time=sleep_data.awake_time,
        light_sleep=sleep_data.light_sleep,
        slow_wave=sleep_data.slow_wave,
        rem=sleep_data.rem,

        disturbance=sleep_data.disturbance,
        baseline=sleep_data.baseline,
        debt=sleep_data.debt,
        strain=sleep_data.strain,
        nap=sleep_data.nap,

        respiratory_rate=sleep_data.respiratory_rate,
        performance=sleep_data.performance,
        consistency=sleep_data.consistency,
        efficiency=sleep_data.efficiency,

        user_id=current_user.id,
        username=current_user.username,
    )

    session.add(new_sleep_data)
    session.commit()
    session.refresh(new_sleep_data)

    return new_sleep_data


# ==================== MODELOS PYDANTIC PARA BATALLAS ====================

class ScheduleExtraBattleRequest(BaseModel):
    minutes_from_now: int = 5  # Cuántos minutos desde ahora


class SetBattleIntervalRequest(BaseModel):
    interval_minutes: int = 120  # Nuevo intervalo en minutos


# ==================== ENDPOINTS DE BATALLA ====================

@router.get("/battles/time-until-next")
async def get_next_battle_time():
    """
    Retorna el tiempo que falta para la próxima batalla en milisegundos y otros formatos.
    
    Returns:
        - milliseconds: Milisegundos hasta la siguiente batalla
        - seconds: Segundos totales
        - minutes: Minutos restantes (sin contar horas)
        - hours: Horas restantes
        - next_battle_time: Fecha y hora ISO de la próxima batalla
        - status: Estado ("waiting" o "battle_should_be_running")
    """
    return await get_time_until_next_battle()


@router.get("/battles/info")
def get_battles_info():
    """
    Retorna información de la configuración actual del scheduler de batallas.
    
    Returns:
        - interval_minutes: Intervalo entre batallas recurrentes (en minutos)
        - check_interval_seconds: Cada cuánto se verifica si toca ejecutar una batalla
    """
    return get_battle_interval()


@router.get("/battles/queue")
def get_battles_queue():
    """
    [DEBUG] Retorna la cola de batallas programadas en memoria.
    Útil para ver todas las batallas programadas y su estado.
    """
    return get_battle_queue_info()


@router.post("/admin/battles/schedule-extra")
async def schedule_extra_battle_endpoint(
    request: ScheduleExtraBattleRequest,
    current_user: User = Depends(get_current_active_user),
):
    """
    [REQUIERE ADMIN] Programa una batalla adicional para dentro de X minutos.
    Después de ejecutarse, el ciclo normal de batallas continúa.
    
    Ejemplo: Si normalmente hay batallas cada 2 horas, pero quieres una en 5 minutos,
    llama este endpoint con minutes_from_now=5. Después, la próxima batalla recurrente
    seguirá normalmente después de eso.
    
    Args:
        minutes_from_now: Cuántos minutos desde ahora ejecutar la batalla
    
    Returns:
        - id: ID de la batalla programada
        - scheduled_time: Cuándo se ejecutará (ISO format)
        - minutes_from_now: Confirmación de minutos solicitados
        - status: "battle_scheduled"
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    if request.minutes_from_now <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="minutes_from_now debe ser mayor a 0"
        )
    
    return await schedule_extra_battle(request.minutes_from_now)


@router.post("/admin/battles/set-interval")
async def set_battle_interval_endpoint(
    request: SetBattleIntervalRequest,
    current_user: User = Depends(get_current_active_user),
):
    """
    [REQUIERE ADMIN] Cambia el intervalo de batallas recurrentes.
    
    Ejemplo: Si quieres que las batallas sean cada 1 hora en lugar de cada 2 horas,
    llama este endpoint con interval_minutes=60.
    
    Args:
        interval_minutes: Nuevo intervalo en minutos
    
    Returns:
        - interval_minutes: Confirmación del nuevo intervalo
        - next_battle_time: Cuándo será la próxima batalla (ISO format)
        - status: "interval_updated"
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    if request.interval_minutes <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="interval_minutes debe ser mayor a 0"
        )
    
    return await set_battle_interval(request.interval_minutes)