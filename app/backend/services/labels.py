"""Label rendering helpers."""
from __future__ import annotations

from pathlib import Path
from typing import Tuple

from PIL import Image, ImageDraw, ImageFont

from ..core.config import get_settings
from ..models.item import Item
from .qrcode_utils import make_qr_png

settings = get_settings()


def _load_font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    """Load a system font with graceful fallback."""

    try:
        if bold:
            return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
    except Exception:  # pragma: no cover - fallback path
        return ImageFont.load_default()


def _truncate(text: str, max_chars: int) -> str:
    return text if len(text) <= max_chars else text[: max_chars - 1] + "…"


SIZE_PRESETS = {
    "50x30": (50, 30),
    "40x30": (40, 30),
    "62x30": (62, 30),
}


def render_label_pdf(item: Item, size_mm: Tuple[int, int] | None = None, public_base_url: str | None = None) -> Path:
    """Render the label into a PDF and return the path."""

    if size_mm is None:
        size_mm = SIZE_PRESETS["50x30"]
    width_mm, height_mm = size_mm
    dpi = 300
    width_px = int(width_mm / 25.4 * dpi)
    height_px = int(height_mm / 25.4 * dpi)

    canvas = Image.new("RGB", (width_px, height_px), "white")
    draw = ImageDraw.Draw(canvas)

    public_url = (public_base_url or settings.public_base_url).rstrip("/") + f"/i/{item.short_id}"
    qr_img = make_qr_png(public_url, box_size=max(2, width_px // 120))
    qr_size = min(height_px - 20, width_px // 2)
    qr_img = qr_img.resize((qr_size, qr_size))
    qr_x = 10
    qr_y = (height_px - qr_size) // 2
    canvas.paste(qr_img, (qr_x, qr_y))

    padding = 20
    text_x = qr_x + qr_size + padding

    title_font = _load_font(48, bold=True)
    body_font = _load_font(28)
    small_font = _load_font(24)

    title = _truncate(item.title or "Untitled Item", 60)
    draw.text((text_x, qr_y), title, fill="black", font=title_font)

    meta_text = f"#{item.short_id} • Loc: {item.location or '-'}"
    draw.text((text_x, qr_y + 60), meta_text, fill="black", font=body_font)

    short_url = public_url.replace("http://", "").replace("https://", "")
    draw.text((text_x, height_px - 40), short_url, fill="black", font=small_font)

    # Optional: wrap description
    desc = _truncate(item.description or "", 140)
    draw.multiline_text(
        (text_x, qr_y + 110),
        desc,
        fill="black",
        font=body_font,
        spacing=4,
    )

    labels_dir = settings.media_dir / "labels"
    labels_dir.mkdir(parents=True, exist_ok=True)
    filename = f"label_{item.id}_{width_mm}x{height_mm}.pdf"
    pdf_path = labels_dir / filename
    canvas.save(pdf_path, "PDF", resolution=dpi)
    return pdf_path
