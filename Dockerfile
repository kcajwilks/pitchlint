FROM node:20-slim AS frontend

WORKDIR /frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY core/requirements.txt /app/core/requirements.txt
RUN pip install --no-cache-dir -r /app/core/requirements.txt

COPY core /app/core
COPY --from=frontend /core/static/spa /app/core/static/spa

# Build-time collectstatic (safe defaults for build)
ENV DJANGO_DEBUG=0 \
    DJANGO_SECRET_KEY=build-secret-key \
    DJANGO_ALLOWED_HOSTS=localhost
RUN python /app/core/manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "core.wsgi:application", "--chdir", "core", "--bind", "0.0.0.0:8000", "--workers", "2", "--threads", "4", "--timeout", "60"]
