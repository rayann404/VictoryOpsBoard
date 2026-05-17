FROM python:3.12-slim

WORKDIR /app

# Устанавливаем системные зависимости для psycopg2 (libpq-dev) и для других пакетов
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости
COPY backend/requirements.txt .

# Устанавливаем Python-пакеты
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код
COPY backend/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]