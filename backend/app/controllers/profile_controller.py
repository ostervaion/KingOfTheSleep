from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlmodel import select

from core.config import AVATAR_DIR
from core.database import get_session
from models import (
    User,
    UserProfile,
)
from schemas import (
    UserPublic,
    UserUpdate,
)
from utils.security import (
    get_current_active_user,
    hash_password,
    verify_password,
)

router = APIRouter()

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