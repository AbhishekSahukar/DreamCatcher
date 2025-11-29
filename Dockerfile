# 1️⃣ FRONTEND BUILD (React)
FROM node:20 AS frontend-builder

WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# 2️⃣ BACKEND STAGE
FROM python:3.11-slim AS backend-builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ ./app/

# 3️⃣ FINAL IMAGE
FROM python:3.11-slim

WORKDIR /app

# Backend dependencies
COPY --from=backend-builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=backend-builder /usr/local/bin /usr/local/bin

# Backend source
COPY app/ ./app/

# Create required dirs INSIDE app/app/
RUN mkdir -p app/templates && mkdir -p app/static/assets

# Copy frontend build → MUST GO INSIDE app/app/*
COPY --from=frontend-builder /frontend/dist/index.html app/templates/index.html
COPY --from=frontend-builder /frontend/dist/assets app/static/assets

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
