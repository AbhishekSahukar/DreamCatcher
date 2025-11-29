# 1️⃣ FRONTEND BUILD (React)
FROM node:20 AS frontend-builder

WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build


# 2️⃣ BACKEND BUILD (FastAPI)
FROM python:3.11-slim AS backend-builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ ./app/


# 3️⃣ FINAL RUNTIME IMAGE
FROM python:3.11-slim

WORKDIR /app

# Copy backend packages + binaries
COPY --from=backend-builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=backend-builder /usr/local/bin /usr/local/bin

# Copy backend source
COPY app/ ./app/

# Ensure folders exist
RUN mkdir -p app/templates && mkdir -p app/static/assets

# Copy frontend build output
COPY --from=frontend-builder /frontend/dist/index.html app/templates/index.html
COPY --from=frontend-builder /frontend/dist/assets/ app/static/assets/

# Inject production env.js (Render)
RUN echo 'window.__ENV__ = { API_BASE: "" };' > app/static/assets/env.js

# Expose FastAPI port
EXPOSE 8000

# Start API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
