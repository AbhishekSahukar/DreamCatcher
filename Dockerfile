# =========================
# 1️⃣ FRONTEND BUILD
# =========================
FROM node:20 AS frontend-builder

WORKDIR /frontend

COPY frontend/package*.json ./

RUN npm install

COPY frontend/ ./

ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

RUN npm run build


# =========================
# 2️⃣ BACKEND BUILD
# =========================
FROM python:3.11-slim AS backend-builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/


# =========================
# 3️⃣ FINAL IMAGE
# =========================
FROM python:3.11-slim

WORKDIR /app

# Copy installed python packages
COPY --from=backend-builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=backend-builder /usr/local/bin /usr/local/bin

# Copy backend
COPY app/ ./app/

# Create folders
RUN mkdir -p app/templates
RUN mkdir -p app/static/assets

# Copy frontend build
COPY --from=frontend-builder /frontend/dist/index.html app/templates/index.html
COPY --from=frontend-builder /frontend/dist/assets/ app/static/assets/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]