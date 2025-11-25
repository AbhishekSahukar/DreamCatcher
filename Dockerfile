
FROM node:20 AS frontend-builder

WORKDIR /app/frontend


COPY frontend/package*.json ./
RUN npm install


COPY frontend/ ./


RUN rm -rf dist
RUN npm run build



FROM python:3.11-slim AS backend-builder

WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY app/ ./app/



FROM python:3.11-slim

WORKDIR /app


COPY --from=backend-builder /usr/local/lib/python3.11/site-packages \
                            /usr/local/lib/python3.11/site-packages
COPY --from=backend-builder /usr/local/bin /usr/local/bin


COPY app/ ./app/


RUN mkdir -p app/templates && mkdir -p app/static/assets


RUN rm -rf app/static/assets/* app/templates/*


COPY --from=frontend-builder /app/frontend/dist/index.html ./app/templates/index.html
COPY --from=frontend-builder /app/frontend/dist/assets ./app/static/assets


EXPOSE 8000


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
