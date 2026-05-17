# EventFlow Project
ССылка на сайт: victoryops.ru
Система управления задачами и событиями с поддержкой реального времени.

## Стек технологий

### Backend
- **Framework:** FastAPI (Python 3.12)
- **Database:** PostgreSQL (SQLAlchemy + asyncpg)
- **Migrations:** Alembic
- **Task/Event Bus:** Redis & NATS
- **Validation:** Pydantic v2
- **Auth:** JWT, Passlib (bcrypt)

### Frontend
- **Framework:** Next.js / React
- **Environment:** Node.js

### Infrastructure
- **Containerization:** Docker & Docker Compose

---

## Быстрый запуск (через Docker Compose)

Это рекомендуемый способ запуска для разработки и тестирования.

### Предварительные требования
- Установленный [Docker](https://docs.docker.com/get-docker/)
- Установленный [Docker Compose](https://docs.docker.com/compose/install/)

### Шаги для запуска

1. **Клонируйте репозиторий:**
   ```bash
   git clone <url-репозитория>
   cd victory_group_unithack
   ```

2. **Запустите контейнеры:**
   ```bash
   docker compose up -d
   ```
   Эта команда соберет образы и запустит все необходимые сервисы:
   - **Backend:** http://localhost:8000 (Swagger: http://localhost:8000/docs)
   - **Frontend:** http://localhost:3000
   - **PostgreSQL:** localhost:5432
   - **Redis:** localhost:6379
   - **NATS:** localhost:4222

3. **Применение миграций:**
   Миграции выполняются автоматически при запуске backend-контейнера через `entrypoint.sh`.

4. **Проверка логов:**
   Если что-то не работает, проверьте логи:
   ```bash
   docker compose logs -f backend
   ```

---

## Локальная разработка (без Docker)

Если вы хотите запустить проект локально для отладки:

### Backend
1. Перейдите в папку backend: `cd backend`
2. Создайте виртуальное окружение: `python -m venv .venv`
3. Активируйте его: `source .venv/bin/activate` (или `.\.venv\Scripts\activate` на Windows)
4. Установите зависимости: `pip install -r requirements.txt`
5. Настройте переменные окружения в `.env` (см. `config.py` или параметры в `docker-compose.yml`)
6. Запустите сервер: `uvicorn main:app --reload`

### Frontend
1. Перейдите в папку frontend: `cd frontend`
2. Установите зависимости: `npm install`
3. Запустите в режиме разработки: `npm run dev`

---

## Основные эндпоинты API
- `POST /register` — Регистрация нового пользователя
- `POST /login` — Авторизация и получение токена
- `GET /identity/users/` — Список пользователей (требуется токен)
- `GET /docs` — Интерактивная документация Swagger

## Устранение неполадок
- **Permission Denied для entrypoint.sh:** Если контейнер backend не запускается, выполните `chmod +x backend/entrypoint.sh`.
- **Database Error:** Убедитесь, что контейнер `db` находится в статусе `healthy`.
