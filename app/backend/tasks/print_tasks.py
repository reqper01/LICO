"""Celery tasks for label printing."""
from __future__ import annotations

import subprocess
import uuid

from celery import shared_task

from ..core.config import get_settings
from ..core.db import session_scope
from ..models.item import Item
from ..services.labels import SIZE_PRESETS, render_label_pdf

settings = get_settings()


@shared_task(bind=True, name="print_label")
def print_label(self, item_id: str, size: str = "50x30", copies: int = 1) -> dict:
    """Render a label and send it to the configured printer."""

    with session_scope() as session:
        item = session.get(Item, uuid.UUID(item_id))
        if not item:
            raise ValueError(f"Item {item_id} not found")
        size_mm = SIZE_PRESETS.get(size, SIZE_PRESETS["50x30"])
        pdf_path = render_label_pdf(item, size_mm=size_mm, public_base_url=settings.public_base_url)

    media_option = f"Custom.{size_mm[0]}x{size_mm[1]}mm"
    command = [
        "lp",
        "-d",
        settings.label_printer,
        "-n",
        str(copies),
        "-o",
        f"media={media_option}",
        "-o",
        "fit-to-page",
        str(pdf_path),
    ]
    process = subprocess.run(command, capture_output=True, text=True, check=False)
    result = {
        "command": command,
        "returncode": process.returncode,
        "stdout": process.stdout,
        "stderr": process.stderr,
    }
    if process.returncode != 0:
        raise RuntimeError(f"Printing failed: {result}")
    return result
