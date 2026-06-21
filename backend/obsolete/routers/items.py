from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Column, String
from sqlalchemy.dialects.postgresql import UUID
from pydantic import BaseModel
import uuid

from database import get_db, Base


# ── Model ────────────────────────────────────────────────────
class Item(Base):
    __tablename__ = "items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)


# ── Schemas ──────────────────────────────────────────────────
class ItemCreate(BaseModel):
    name: str


class ItemRead(BaseModel):
    id: uuid.UUID
    name: str

    class Config:
        from_attributes = True


# ── Router ───────────────────────────────────────────────────
router = APIRouter()


@router.get("/", response_model=list[ItemRead])
async def list_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item))
    return result.scalars().all()


@router.post("/", response_model=ItemRead, status_code=201)
async def create_item(payload: ItemCreate, db: AsyncSession = Depends(get_db)):
    item = Item(name=payload.name)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


@router.get("/{item_id}", response_model=ItemRead)
async def get_item(item_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
