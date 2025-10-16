"""Utility helpers to generate short base36 identifiers."""
from __future__ import annotations

import secrets
import string


ALPHABET = string.digits + string.ascii_lowercase


def generate_short_id(length: int = 7) -> str:
    """Return a random base36 string with the requested length."""

    return "".join(secrets.choice(ALPHABET) for _ in range(length))
