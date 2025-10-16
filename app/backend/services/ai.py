"""Deterministic AI suggestion stub (replace with DeepSeek later)."""
from __future__ import annotations

import hashlib
from typing import Optional


_BASE_RESPONSE = {
    "title": "Stainless Steel Watering Can",
    "description": "A durable 1.5L can suitable for indoor/outdoor plants. Fingerprint-resistant finish.",
    "tags": ["gardening", "watering", "stainless", "1.5L"],
}


def _rotate(values: list[str], offset: int) -> list[str]:
    return values[offset:] + values[:offset]


def describe_item(image_path: Optional[str] = None, text_hint: Optional[str] = None) -> dict:
    """Return deterministic mock suggestions based on inputs.

    The goal is to emulate an AI assistant without external dependencies.
    The output is stable for the same combination of inputs.
    """

    seed_input = (image_path or "") + "::" + (text_hint or "")
    digest = hashlib.sha1(seed_input.encode("utf-8")).digest()
    offset = digest[0] % len(_BASE_RESPONSE["tags"])
    response = dict(_BASE_RESPONSE)
    response["title"] = f"{response['title']} #{digest[1] % 9 + 1}"
    response["tags"] = _rotate(response["tags"], offset)
    return response
