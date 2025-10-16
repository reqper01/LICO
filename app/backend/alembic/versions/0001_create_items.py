"""create items tables"""
from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "items",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("short_id", sa.String(length=16), nullable=False, unique=True),
        sa.Column("title", sa.String(), nullable=False, server_default=""),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("tags", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="[]"),
        sa.Column("category", sa.String(), nullable=True),
        sa.Column("brand", sa.String(), nullable=True),
        sa.Column("model", sa.String(), nullable=True),
        sa.Column("serial_no", sa.String(), nullable=True),
        sa.Column("location", sa.String(), nullable=True),
        sa.Column("status", sa.String(), nullable=False, server_default="active"),
        sa.Column("purchase_date", sa.Date(), nullable=True),
        sa.Column("warranty_expiry", sa.Date(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index(op.f("ix_items_short_id"), "items", ["short_id"], unique=True)

    op.create_table(
        "item_images",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("item_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("items.id", ondelete="CASCADE"), nullable=False),
        sa.Column("path", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index(op.f("ix_item_images_item_id"), "item_images", ["item_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_item_images_item_id"), table_name="item_images")
    op.drop_table("item_images")
    op.drop_index(op.f("ix_items_short_id"), table_name="items")
    op.drop_table("items")
