"""Celery application bootstrap."""
from __future__ import annotations

import os

from celery import Celery

from ..core.config import get_settings

settings = get_settings()
os.environ.setdefault("CELERY_TIMEZONE", "UTC")

celery_app = Celery(
    "label_printer",
    broker=settings.redis_url,
    backend=settings.redis_url,
)
celery_app.conf.update(task_serializer="json", result_serializer="json", accept_content=["json"])

celery_app.autodiscover_tasks(["backend.tasks"])
