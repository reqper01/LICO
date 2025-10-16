"""Item management API endpoints."""
from __future__ import annotations

import io
import json
import uuid
from datetime import date
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy import String, or_, select
from sqlalchemy.orm import Session

from ..core.config import get_settings
from ..core.db import SessionLocal
from ..models.item import Item, ItemImage
from ..schemas.item import (
    ItemCreateResponse,
    ItemImageRead,
    ItemRead,
    ItemUpdate,
    PrintRequest,
    PrintResponse,
)
from ..services.ai import describe_item
from ..services.labels import SIZE_PRESETS
from ..services.qrcode_utils import make_qr_png
from ..tasks.print_tasks import print_label

router = APIRouter(prefix="/api/items", tags=["items"])
settings = get_settings()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _parse_tags(raw: Optional[str]) -> list[str]:
    if not raw:
        return []
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, list):
            return [str(tag) for tag in parsed]
    except json.JSONDecodeError:
        pass
    return [tag.strip() for tag in raw.split(",") if tag.strip()]


def _save_upload(item_id: uuid.UUID, upload: UploadFile) -> Path:
    media_dir = settings.media_dir / "items" / str(item_id)
    media_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid.uuid4()}{Path(upload.filename or 'upload').suffix}"
    destination = media_dir / filename
    with destination.open("wb") as buffer:
        buffer.write(upload.file.read())
    return destination


@router.get("/", response_model=list[ItemRead])
def list_items(search: Optional[str] = None, db: Session = Depends(get_db)) -> list[ItemImageRead]:
    query = select(Item)
    if search:
        term = f"%{search.lower()}%"
        query = query.where(
            or_(
                Item.title.ilike(term),
                Item.description.ilike(term),
                Item.tags.cast(String).ilike(term),
            )
        )
    items = db.execute(query.order_by(Item.created_at.desc())).scalars().unique().all()
    return items


@router.post("/", response_model=ItemCreateResponse)
async def create_item(
    title: str = Form(""),
    description: str = Form(""),
    tags: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    brand: Optional[str] = Form(None),
    model: Optional[str] = Form(None),
    serial_no: Optional[str] = Form(None),
    location: Optional[str] = Form(None),
    status: str = Form("active"),
    purchase_date: Optional[str] = Form(None),
    warranty_expiry: Optional[str] = Form(None),
    text_hint: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
) -> ItemCreateResponse:
    data = Item(
        title=title,
        description=description,
        tags=_parse_tags(tags),
        category=category,
        brand=brand,
        model=model,
        serial_no=serial_no,
        location=location,
        status=status,
    )
    if purchase_date:
        try:
            data.purchase_date = date.fromisoformat(purchase_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid purchase_date")
    if warranty_expiry:
        try:
            data.warranty_expiry = date.fromisoformat(warranty_expiry)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid warranty_expiry")

    db.add(data)
    db.flush()

    saved_path = None
    if image:
        saved = _save_upload(data.id, image)
        saved_path = saved
        db.add(ItemImage(item_id=data.id, path=str(saved.relative_to(settings.media_dir))))
        db.flush()

    suggestions = describe_item(
        image_path=str(saved_path) if saved_path else None,
        text_hint=text_hint,
    )

    db.commit()
    db.refresh(data)
    return ItemCreateResponse(item=data, suggestions=suggestions)


@router.patch("/{item_id}", response_model=ItemRead)
def update_item(item_id: uuid.UUID, payload: ItemUpdate, db: Session = Depends(get_db)) -> ItemRead:
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(item, field, value)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.post("/{item_id}/images", response_model=list[ItemImageRead])
async def upload_item_image(
    item_id: uuid.UUID,
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> list[ItemImageRead]:
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    saved = _save_upload(item.id, image)
    db.add(ItemImage(item_id=item.id, path=str(saved.relative_to(settings.media_dir))))
    db.commit()
    db.refresh(item)
    return item.images


@router.get("/{item_id}/qr.png")
def get_item_qr(item_id: uuid.UUID, db: Session = Depends(get_db)) -> StreamingResponse:
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    url = settings.public_base_url.rstrip("/") + f"/i/{item.short_id}"
    qr_img = make_qr_png(url)
    buffer = io.BytesIO()
    qr_img.save(buffer, format="PNG")
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="image/png")


@router.post("/{item_id}/print", response_model=PrintResponse)
def print_item_label(
    item_id: uuid.UUID,
    request: PrintRequest,
    db: Session = Depends(get_db),
) -> PrintResponse:
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    size = request.size if request.size in SIZE_PRESETS else "50x30"
    task = print_label.delay(str(item.id), size=size, copies=request.copies)
    return PrintResponse(status="queued", job_id=str(task.id))
