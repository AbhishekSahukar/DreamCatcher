# 1️⃣ FRONTEND BUILD (React + Vite)
FROM node:20 AS frontend-builder

WORKDIR /frontend

# Install deps
COPY frontend/package*.json ./
RUN npm install

# Build frontend
COPY frontend/ ./
RUN npm run build


# 2️⃣ BACKEND BUILD (FastAPI)
FROM python:3.11-slim AS backend-builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/


# 3️⃣ FINAL IMAGE (Serve React + API)
FROM python:3.11-slim

WORKDIR /app

# Copy backend dependencies installed in previous stage
COPY --from=backend-builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=backend-builder /usr/local/bin /usr/local/bin

# Copy backend source
COPY app/ ./app/

# Ensure required folders exist
RUN mkdir -p app/templates && mkdir -p app/static/assets

# Copy built frontend
COPY --from=frontend-builder /frontend/dist/index.html app/templates/index.html
COPY --from=frontend-builder /frontend/dist/assets/ app/static/assets/

# Copy env.js from Vite public → dist → container
COPY --from=frontend-builder /frontend/dist/env.js app/static/assets/env.js

# Expose port
EXPOSE 8000

# Start backend
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
