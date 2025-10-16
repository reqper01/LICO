"""Pydantic schemas for items."""
from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ItemImageRead(BaseModel):
    id: UUID
    path: str
    created_at: datetime

    class Config:
        orm_mode = True


class ItemBase(BaseModel):
    title: str = ""
    description: str = ""
    tags: List[str] = Field(default_factory=list)
    category: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    serial_no: Optional[str] = None
    location: Optional[str] = None
    status: str = "active"
    purchase_date: Optional[date] = None
    warranty_expiry: Optional[date] = None


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    serial_no: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = None
    purchase_date: Optional[date] = None
    warranty_expiry: Optional[date] = None


class ItemRead(ItemBase):
    id: UUID
    short_id: str
    created_at: datetime
    updated_at: datetime
    images: List[ItemImageRead] = Field(default_factory=list)

    class Config:
        orm_mode = True


class ItemPublic(BaseModel):
    short_id: str
    title: str
    description: str
    tags: List[str]
    location: Optional[str]
    status: str
    primary_image: Optional[str]


class ItemCreateResponse(BaseModel):
    item: ItemRead
    suggestions: dict


class QRResponse(BaseModel):
    url: str


class PrintRequest(BaseModel):
    size: str = Field("50x30", regex=r"^(50x30|40x30|62x30)$")
    copies: int = Field(1, ge=1, le=20)


class PrintResponse(BaseModel):
    status: str
    job_id: str
