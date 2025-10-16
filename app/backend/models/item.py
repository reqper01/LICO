"""SQLAlchemy models for inventory items."""
from __future__ import annotations

import uuid
from datetime import datetime, date

from sqlalchemy import Date, DateTime, ForeignKey, Text, event, select
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..utils.shortid import generate_short_id
from . import Base


class Item(Base):
    """Represents an asset that can be tagged with a QR/Barcode."""

    __tablename__ = "items"

    id: Mapped[uuid.UUID] = mapped_column(
        default=uuid.uuid4, primary_key=True, nullable=False
    )
    short_id: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(default="", nullable=False)
    description: Mapped[str] = mapped_column(Text, default="", nullable=False)
    tags: Mapped[list[str]] = mapped_column(JSONB, default=list, nullable=False)
    category: Mapped[str | None]
    brand: Mapped[str | None]
    model: Mapped[str | None]
    serial_no: Mapped[str | None]
    location: Mapped[str | None]
    status: Mapped[str] = mapped_column(default="active", nullable=False)
    purchase_date: Mapped[date | None] = mapped_column(Date)
    warranty_expiry: Mapped[date | None] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    images: Mapped[list["ItemImage"]] = relationship(
        back_populates="item", cascade="all, delete-orphan", lazy="joined"
    )


class ItemImage(Base):
    """Image metadata for an :class:`Item`."""

    __tablename__ = "item_images"

    id: Mapped[uuid.UUID] = mapped_column(
        default=uuid.uuid4, primary_key=True, nullable=False
    )
    item_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("items.id", ondelete="CASCADE"), nullable=False, index=True
    )
    path: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    item: Mapped[Item] = relationship(back_populates="images")


@event.listens_for(Item, "before_insert")
def ensure_short_id(mapper, connection, target: Item) -> None:  # pragma: no cover
    """Populate the short_id if it is missing, ensuring uniqueness."""

    if target.short_id:
        return

    while True:
        candidate = generate_short_id()
        exists = connection.execute(
            select(Item.short_id).where(Item.short_id == candidate)
        ).scalar_one_or_none()
        if not exists:
            target.short_id = candidate
            break
