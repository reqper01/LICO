# QR Label MVP

This repository contains a production-ready MVP for creating QR/Barcode labels with a Next.js PWA frontend and FastAPI backend.

## Project Structure

```
app/
  frontend/        # Next.js PWA
  backend/         # FastAPI app
  ops/             # Environment helpers (env sample, docker-compose)
```

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 16 running on port **5433** (see `app/ops/docker-compose.yml`)
- Redis 7+
- CUPS with `lp` command available for printing

## Backend Setup

```bash
cd app/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp ../ops/.env.sample ../ops/.env  # adjust values as needed
export $(cat ../ops/.env | xargs)  # or use a dotenv loader

# Prepare database
alembic upgrade head

# Run API
uvicorn backend.main:app --reload --port 8000
```

### Celery Worker

```bash
cd app/backend
source .venv/bin/activate
celery -A backend.tasks.celery_app.celery_app worker -l info
```

## Frontend Setup

```bash
cd app/frontend
npm install
npm run dev
```

The PWA will be available at `http://localhost:3000`.

### Environment Variables

Frontend expects these optional environment variables (create `.env.local`):

```
NEXT_PUBLIC_API_BASE=http://localhost:8000
NEXT_PUBLIC_PUBLIC_BASE=http://localhost:5434
```

## Printing

Set `LABEL_PRINTER` to your printer name (see `lpstat -p`). Test a print job:

```bash
export LABEL_PRINTER=MY_LABEL_PRINTER
curl -X POST http://localhost:8000/api/items/<item_id>/print -H 'Content-Type: application/json' \
  -d '{"size":"50x30","copies":1}'
```

## Running Tests

```bash
cd app/backend
pytest
```

## Features

- AI-assisted metadata suggestions (stubbed, deterministic)
- QR code generation and label PDF rendering
- Celery print worker for async label printing
- Responsive Next.js PWA with offline caching and install support
- Public sharing pages with delightful micro-animations
