from datetime import datetime, time, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select

from config import ACCESS_TOKEN_EXPIRE_MINUTES
from database import get_session
from models import Token, User, UserCreate, UserPublic
from security import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    get_user_by_username,
    hash_password,
)

router = APIRouter()


@router.get("/")
def root():
    return {"message": "API running"}

@router.get("/nextbattle")
def nextbattle(hora_destino=time(0, 0, 0)):
    # 1. Obtener el momento exacto actual
    ahora = datetime.now()
    
    # 2. Combinar la fecha de hoy con la hora objetivo
    meta = datetime.combine(ahora.date(), hora_destino)
    
    # 3. Si la hora ya pasó hoy, calcula para esa hora del día de mañana
    if ahora >= meta:
        from datetime import timedelta
        meta += timedelta(days=1)
        
    # 4. Restar los tiempos para obtener la diferencia
    diferencia = meta - ahora
    
    # 5. Retornar el total de segundos (incluye decimales de microsegundos)
    return {"nextbattle": diferencia}

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
