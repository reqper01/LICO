# ---- Base Backend ----
FROM python:3.11-slim as backend
WORKDIR /app/backend
COPY app/backend /app/backend
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# ---- Base Frontend ----
FROM node:20-alpine as frontend
WORKDIR /app/frontend
COPY app/frontend /app/frontend
RUN npm install && npm run build

# ---- Final Image ----
FROM python:3.11-slim
WORKDIR /app
COPY --from=backend /app/backend /app/backend
COPY --from=frontend /app/frontend/out /app/frontend/out
WORKDIR /app/backend
ENV PORT=8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
