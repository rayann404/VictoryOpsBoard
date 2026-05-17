# VictoryOpsBoard

**VictoryOpsBoard** — это интеллектуальная система управления проектами и задачами, разработанная командой **DurovTeam** для кейса **Victory Group** на хакатоне **ЮНИТХАК**.

Проект объединяет классический Kanban-интерфейс с мощью искусственного интеллекта (Google Gemini) и real-time обновлений для максимально эффективной командной работы.

---

## Оглавление
1. [Основные возможности](#-основные-возможности)
2. [Технологический стек](#-технологический-стек)
3. [Быстрый старт (Docker)](#-быстрый-старт-docker)
4. [Ручная установка и разработка](#-ручная-установка-и-разработка)
    - [Настройка бэкенда](#1-настройка-бэкенда)
    - [Настройка фронтенда](#2-настройка-фронтенда)
5. [Конфигурация (Environment)](#-конфигурация-environment)
6. [Структура проекта](#-структура-проекта)

---

## Основные возможности

- **AI CatchUp**: Интеллектуальная сводка по любой задаче. ИИ анализирует описание, комментарии и историю активности, выделяя суть, текущие блокеры и рекомендуемые следующие шаги.
- **Real-time Collaboration**: Мгновенное обновление доски у всех участников при создании, перемещении или изменении задач (WebSocket + Redis/NATS).
- **Гибкое управление**: Организации -> Проекты -> Доски -> Колонки -> Задачи.
- **Интеграция с Google Gemini**: Продвинутый анализ контекста задач.
- **Безопасность**: Авторизация на базе JWT (RS256) с использованием пары ключей (Public/Private).

---

## Технологический стек

### Backend
- **Язык**: Python 3.12
- **Фреймворк**: FastAPI (Asynchronous)
- **База данных**: PostgreSQL (SQLAlchemy + asyncpg)
- **Миграции**: Alembic
- **Real-time**: Redis (Pub/Sub) + NATS
- **AI**: Google Generative AI (Gemini API)
- **Безопасность**: PyJWT (RSA256)

### Frontend
- **Язык**: JavaScript (Vanilla / ES Modules)
- **Стили**: CSS3 (Modern features)
- **Сервер**: Node.js (Static file server + API Proxy)

---

## Быстрый старт (Docker)

Для запуска всей инфраструктуры и бэкенда одной командой:

1. Убедитесь, что у вас установлен Docker и Docker Compose.
2. Запустите сборку и старт:
   ```bash
   docker-compose up --build
   ```

**Доступные сервисы после запуска:**
- **Backend API**: [http://localhost:8000](http://localhost:8000)
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **PostgreSQL**: `localhost:5432` (User: `postgres`, Password: `password`, DB: `eventflow`)
- **Redis**: `localhost:6379`

> **Важно:** Фронтенд на текущем этапе требует ручного запуска (см. ниже).

---

## Ручная установка и разработка

### 1. Настройка бэкенда

Перейдите в директорию `backend`:
```bash
cd backend
```

**Шаг 1: Виртуальное окружение**
```bash
python -m venv .venv
source .venv/bin/activate # Linux/macOS
# .venv\Scripts\activate  # Windows
```

**Шаг 2: Установка зависимостей**
```bash
pip install -r requirements.txt
```

**Шаг 3: Генерация JWT ключей (ОБЯЗАТЕЛЬНО)**
Авторизация не будет работать без RSA-ключей. Сгенерируйте их:
```bash
mkdir -p core/security/certs
openssl genrsa -out core/security/certs/private_jwt_key.pem 2048
openssl rsa -in core/security/certs/private_jwt_key.pem -pubout -out core/security/certs/public_jwt_key.pem
```

**Шаг 4: Настройка переменных окружения**
Создайте файл `.env` в корне папки `backend/`:
```env
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/eventflow
REDIS_URL=redis://localhost:6379
NATS_URL=nats://localhost:4222
GEMINI_API_KEY=ваш_ключ_от_google_ai_studio
```

**Шаг 5: Миграции и запуск**
```bash
alembic upgrade head
uvicorn main:app --reload
```

---

### 2. Настройка фронтенда

Перейдите в директорию `frontend`:
```bash
cd frontend
```

**Шаг 1: Установка и запуск**
```bash
npm install
npm run dev
```

**Фронтенд будет доступен по адресу:** [http://localhost:5173](http://localhost:5173)

*Проксирование запросов к API настроено автоматически на `http://localhost:8000`.*

---

## Конфигурация (Environment)

| Переменная | Описание | Значение по умолчанию |
|------------|----------|-----------------------|
| `DATABASE_URL` | Строка подключения к БД | `postgresql+asyncpg://...` |
| `GEMINI_API_KEY` | Ключ для работы с ИИ | (Обязателен для AI функций) |
| `AI_MODEL` | Модель Gemini | `gemini-2.5-flash` |
| `REDIS_URL` | Адрес Redis | `redis://localhost:6379` |

---

## Структура проекта

```text
VictoryOpsBoard/
├── backend/                # Исходный код сервера
│   ├── alembic/           # Миграции БД
│   ├── core/              # Ядро (БД, JWT, Real-time инфраструктура)
│   ├── modules/           # Бизнес-логика (Identity, AI, Tasks, Projects)
│   └── main.py            # Точка входа FastAPI
├── frontend/               # Исходный код клиента
│   ├── src/               # Статические файлы (HTML, CSS, JS)
│   └── server.mjs         # Node.js сервер (Proxy + Static)
├── docker-compose.yml      # Оркестрация контейнеров
└── README.md               # Данная документация
```

---
