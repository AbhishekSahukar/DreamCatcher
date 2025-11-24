
# 1️⃣ FRONTEND BUILD (React)

FROM node:20 AS frontend-builder

WORKDIR /frontend

# Copy frontend source
COPY frontend/package*.json ./
RUN npm install

COPY frontend/ ./
RUN npm run build



# 2️⃣ BACKEND BUILD (FastAPI)

FROM python:3.11-slim AS backend-builder

WORKDIR /app

# Install backend dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY app/ ./app/



# 3️⃣ FINAL IMAGE (Serve React + FastAPI)

FROM python:3.11-slim

WORKDIR /app

# Copy installed dependencies from backend builder
COPY --from=backend-builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=backend-builder /usr/local/bin /usr/local/bin

# Copy backend source code
COPY app/ ./app/

# Create folders expected by FastAPI
RUN mkdir -p app/templates && mkdir -p app/static/assets

# Copy built React frontend into FastAPI
COPY --from=frontend-builder /frontend/dist/index.html app/templates/index.html
COPY --from=frontend-builder /frontend/dist/assets app/static/assets

# Expose port
EXPOSE 8000

# Start FastAPI with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
