"""FastAPI application entry point."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .core.config import get_settings
from .routers import items, public

settings = get_settings()

app = FastAPI(title="QR Label App", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items.router)
app.include_router(public.router)

app.mount("/media", StaticFiles(directory=settings.media_dir), name="media")


@app.get("/")
def read_root() -> dict:
    return {"message": "QR Label service is running"}
