FROM python:3.12-alpine
WORKDIR /app

RUN apk update && \
    apk add --virtual .tmp build-base python3-dev \
    libpq postgresql-dev gcc jpeg-dev zlib-dev libffi-dev

COPY . .
RUN pip install -r requirements.txt && \
    apk del .tmp && apk add postgresql-dev jpeg-dev

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

CMD ["gunicorn", "--reload", "--workers=2", "--worker-tmp-dir", "/dev/shm", "--bind=0.0.0.0:80", "--chdir", "/app/crypto_assets", "crypto_assets.wsgi"]
