"""Public read-only endpoints."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from ..core.config import get_settings
from ..core.db import SessionLocal
from ..models.item import Item
from ..schemas.item import ItemPublic

router = APIRouter(tags=["public"])
settings = get_settings()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/i/{short_id}", response_model=ItemPublic)
def get_public_item(short_id: str):
    with SessionLocal() as db:
        item = db.execute(select(Item).where(Item.short_id == short_id)).scalar_one_or_none()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        primary_image = None
        if item.images:
            primary_image = settings.public_base_url.rstrip("/") + "/media/" + item.images[0].path
        return ItemPublic(
            short_id=item.short_id,
            title=item.title,
            description=item.description,
            tags=item.tags,
            location=item.location,
            status=item.status,
            primary_image=primary_image,
        )
