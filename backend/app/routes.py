from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4
from sqlalchemy import func

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select
from pydantic import BaseModel
from ws import broadcast_fetch
from config import ACCESS_TOKEN_EXPIRE_MINUTES
from database import get_session
from models import (
    ScoreHistory,
    SleepData,
    SleepDataCreate,
    SleepDataPublic,
    Token,
    User,
    UserCreate,
    UserPublic,
    UserProfile,
    UserUpdate,
    Friend
)
from security import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    get_user_by_username,
    hash_password,
    verify_password,
)
from battle_scheduler import (
    get_time_until_next_battle,
    schedule_extra_battle,
    set_battle_interval,
    get_battle_interval,
    get_battle_queue_info,
)

router = APIRouter()

DAY_NAMES = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
UPLOAD_BASE_DIR = Path(__file__).resolve().parent / "uploads"
AVATAR_DIR = UPLOAD_BASE_DIR / "avatars"
AVATAR_DIR.mkdir(parents=True, exist_ok=True)


@router.get("/")
def root():
    return {"message": "API running"}

@router.get("/friends", response_model=list[str])
def list_friends(
    current_user: User = Depends(get_current_active_user),
    session=Depends(get_session),
):
    friend_rows = session.exec(
        select(Friend).where(Friend.user_id == current_user.id)
    ).all()
 
    friend_ids = [row.friend_id for row in friend_rows]
    if not friend_ids:
        return []
 
    friends = session.exec(
        select(User).where(User.id.in_(friend_ids))
    ).all()
 
    return [friend.username for friend in friends]
 
 
@router.post("/friends/{username}", status_code=status.HTTP_201_CREATED)
def add_friend(
    username: str,
    current_user: User = Depends(get_current_active_user),
    session=Depends(get_session),
):
    if username == current_user.username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No puedes añadirte a ti mismo como amigo")
 
    friend_user = get_user_by_username(session, username)
    if friend_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
 
    existing = session.exec(
        select(Friend).where(
            Friend.user_id == current_user.id,
            Friend.friend_id == friend_user.id,
        )
    ).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ya sois amigos")
 
    # Creamos la relación en los dos sentidos para que sea simétrica de inmediato
    session.add(Friend(user_id=current_user.id, friend_id=friend_user.id))
    session.add(Friend(user_id=friend_user.id, friend_id=current_user.id))
    session.commit()
 
    return {"message": f"{username} añadido como amigo"}

@router.delete("/friends/{username}", status_code=status.HTTP_200_OK)
def delete_friend(
    username: str,
    current_user: User = Depends(get_current_active_user),
    session=Depends(get_session),
):
    if username == current_user.username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes eliminarte a ti mismo",
        )

    friend_user = get_user_by_username(session, username)

    if friend_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    # Relación: usuario actual -> amigo
    friendship = session.exec(
        select(Friend).where(
            Friend.user_id == current_user.id,
            Friend.friend_id == friend_user.id,
        )
    ).first()

    # Relación inversa: amigo -> usuario actual
    reverse_friendship = session.exec(
        select(Friend).where(
            Friend.user_id == friend_user.id,
            Friend.friend_id == current_user.id,
        )
    ).first()

    if friendship is None and reverse_friendship is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No sois amigos",
        )

    if friendship is not None:
        session.delete(friendship)

    if reverse_friendship is not None:
        session.delete(reverse_friendship)

    session.commit()

    return {"message": f"{username} eliminado de tus amigos"}

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

    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id, "role": user.role},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/all_users", response_model=list[UserPublic])
def list_users(current_user=Depends(get_current_active_user), session=Depends(get_session)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return session.exec(select(User)).all()


@router.delete("/users/{username}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(username: str, current_user=Depends(get_current_active_user), session=Depends(get_session)):
    if current_user.username != username and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
    user = get_user_by_username(session, username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    session.delete(user)
    session.commit()


@router.post("/profile/avatar")
async def upload_profile_avatar(
    current_user: User = Depends(get_current_active_user),
    session=Depends(get_session),
    file: UploadFile = File(...),
):
    if not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No file selected")

    extension = Path(file.filename).suffix.lower()
    if extension not in {".jpg", ".jpeg", ".png", ".webp", ".gif"}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only image files are allowed")

    file_name = f"{current_user.id}_{uuid4().hex}{extension}"
    file_path = AVATAR_DIR / file_name
    contents = await file.read()
    file_path.write_bytes(contents)

    profile = session.exec(select(UserProfile).where(UserProfile.user_id == current_user.id)).first()
    if profile is None:
        profile = UserProfile(user_id=current_user.id)
        session.add(profile)

    profile.user_avatar_path = f"/uploads/avatars/{file_name}"
    session.add(profile)
    session.commit()
    session.refresh(profile)

    return {"avatar_url": f"/api{profile.user_avatar_path}"}


@router.patch("/profile", response_model=UserPublic)
def update_profile(
    payload: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    session=Depends(get_session),
):
    # Email: solo tocamos si viene y es distinto al actual
    if payload.email and payload.email != current_user.email:
        existing_email = session.exec(select(User).where(User.email == payload.email)).first()
        if existing_email and existing_email.id != current_user.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        current_user.email = payload.email

    # Password: si viene new_password, exigimos current_password y la validamos
    if payload.new_password:
        if not payload.current_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is required to set a new password",
            )
        if not verify_password(payload.current_password, current_user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect")
        current_user.password = hash_password(payload.new_password)

    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return current_user

@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_active_user),
    session=Depends(get_session),
):
    profile = session.exec(
        select(UserProfile).where(
            UserProfile.user_id == current_user.id
        )
    ).first()

    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "avatar_path": (
            f"/api{profile.user_avatar_path}"
            if profile
            else None
        ),
    }

@router.get("/dashboard/refresh")
async def trigger_dashboard_refresh():
    await broadcast_fetch()
    return {"status": "ok"}

def _build_ranking(session, current_user_id: int):
    all_scores = session.exec(
        select(ScoreHistory)
        .order_by(ScoreHistory.created_at.desc())
    ).all()

    latest_by_user = {}
    previous_by_user = {}

    for score in all_scores:
        if score.user_id is None:
            continue

        if score.user_id not in latest_by_user:
            latest_by_user[score.user_id] = score

        elif score.user_id not in previous_by_user:
            previous_by_user[score.user_id] = score

    users = session.exec(
        select(User)
    ).all()

    profiles = session.exec(
        select(UserProfile)
    ).all()


    profiles_by_user = {
        profile.user_id: profile
        for profile in profiles
    }

    ranking_data = [
        {
            "user_id": user.id,
            "name": user.username,

            "avatar_path": (
                profiles_by_user[user.id].user_avatar_path
                if user.id in profiles_by_user
                else None
            ),

            "current_points": (
                latest_by_user[user.id].elo_score
                if user.id in latest_by_user
                else 0
            ),

            "previous_points": (
                previous_by_user[user.id].elo_score
                if user.id in previous_by_user
                else 0
            ),
        }
        for user in users
    ]

    ranking_data.sort(
        key=lambda entry: entry["current_points"],
        reverse=True,
    )

    previous_ranking = sorted(
        ranking_data,
        key=lambda entry: entry["previous_points"],
        reverse=True,
    )

    previous_positions = {
        item["user_id"]: index + 1
        for index, item in enumerate(previous_ranking)
    }

    ranking = []
    current_user_ranking = None
    current_user_prev_pos = None

    for index, entry in enumerate(ranking_data):
        current_pos = index + 1

        previous_pos = previous_positions.get(
            entry["user_id"],
            current_pos,
        )

        pos_delta = previous_pos - current_pos

        ranking.append({
            "ranking": str(current_pos),
            "user_id": entry["user_id"],
            "name": entry["name"],
            "avatar_path": (
                f"/api{entry['avatar_path']}"
                if entry["avatar_path"]
                else None
            ),
            "points": str(entry["current_points"]),
            "posChange": str(abs(pos_delta)),
            "trend": (
                "up"
                if pos_delta > 0
                else "down"
                if pos_delta < 0
                else "same"
            ),
        })

        if entry["user_id"] == current_user_id:
            current_user_ranking = current_pos
            current_user_prev_pos = previous_pos

    return (
        ranking,
        current_user_ranking,
        current_user_prev_pos,
    )

async def _build_battle_countdown(now: datetime, current_user_ranking, current_user_prev_pos):
    battle_info = await get_time_until_next_battle()

    tomorrow_midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    seconds_until_eod = int((tomorrow_midnight - now).total_seconds())

    delta_ranking = 0
    if current_user_prev_pos and current_user_ranking:
        delta_ranking = current_user_prev_pos - current_user_ranking

    return {
        "currentRanking": current_user_ranking or 0,
        "seconds": battle_info.get("seconds", 0),
        "endDay": seconds_until_eod,
        "deltaRanking": delta_ranking,
    }


def _build_sleep_score(session, current_user_id: int, now: datetime):
    seven_days_ago = now - timedelta(days=7)
    records = session.exec(
        select(ScoreHistory).where(
            ScoreHistory.user_id == current_user_id,
            ScoreHistory.created_at >= seven_days_ago,
        ).order_by(ScoreHistory.created_at.asc())
    ).all()

    sleep_by_date = {}
    for record in records:
        sleep_by_date.setdefault(record.created_at.date(), []).append(record.sleep_score)

    labels = []
    scores = []
    for days_back in range(6, -1, -1):
        target_date = now.date() - timedelta(days=days_back)
        labels.append(DAY_NAMES[target_date.weekday()])

        valid_scores = [s for s in sleep_by_date.get(target_date, []) if s is not None]
        if valid_scores:
            avg_score = int(sum(valid_scores) / len(valid_scores))
            scores.append(max(0, min(100, avg_score)))
        else:
            scores.append(0)

    return {"labels": labels, "scores": scores}


def _lobby_state(session, current_user_id: int, now: datetime) -> bool:
    today = now.date()

    today_data = session.exec(
        select(SleepData).where(
            SleepData.user_id == current_user_id,
            func.date(SleepData.created_at) == today,
        )
    ).first()

    return today_data is not None

@router.get("/dashboard")
async def dashboard_fake(
    current_user: User = Depends(get_current_active_user),
    session=Depends(get_session),
):
    now = datetime.now(timezone.utc)

    ranking, current_user_ranking, current_user_prev_pos = _build_ranking(session, current_user.id)
    next_battle = await _build_battle_countdown(now, current_user_ranking, current_user_prev_pos)
    sleep_score = _build_sleep_score(session, current_user.id, now)
    lobby = _lobby_state(session, current_user.id, now)

    return {
        "nextBattle": next_battle,
        "sleepScore": sleep_score,
        "ranking": ranking,
        "lobby": lobby,
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


class ScheduleExtraBattleRequest(BaseModel):
    minutes_from_now: int = 5


class SetBattleIntervalRequest(BaseModel):
    interval_minutes: int = 120


@router.get("/battles/time-until-next")
async def get_next_battle_time():
    return await get_time_until_next_battle()


@router.get("/battles/info")
def get_battles_info():
    return get_battle_interval()


@router.get("/battles/queue")
def get_battles_queue():
    return get_battle_queue_info()


def _require_admin(current_user: User):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")


@router.post("/admin/battles/schedule-extra")
async def schedule_extra_battle_endpoint(
    request: ScheduleExtraBattleRequest,
    current_user: User = Depends(get_current_active_user),
):
    _require_admin(current_user)

    if request.minutes_from_now <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="minutes_from_now debe ser mayor a 0")

    return await schedule_extra_battle(request.minutes_from_now)


@router.post("/admin/battles/set-interval")
async def set_battle_interval_endpoint(
    request: SetBattleIntervalRequest,
    current_user: User = Depends(get_current_active_user),
):
    _require_admin(current_user)

    if request.interval_minutes <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="interval_minutes debe ser mayor a 0")

    return await set_battle_interval(request.interval_minutes)