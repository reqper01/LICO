"""Utilities for creating QR and Code128 images."""
from __future__ import annotations

import io

import qrcode
from PIL import Image
from barcode import Code128
from barcode.writer import ImageWriter


def make_qr_png(url: str, box_size: int = 8, border: int = 2) -> Image.Image:
    """Create a QR code PNG image pointing to the given URL."""

    qr = qrcode.QRCode(box_size=box_size, border=border)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img.convert("RGB")


def make_code128_png(data: str) -> Image.Image:
    """Create a Code128 barcode as a PIL image."""

    buffer = io.BytesIO()
    Code128(data, writer=ImageWriter()).write(buffer)
    buffer.seek(0)
    return Image.open(buffer).convert("RGB")
