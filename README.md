# ГИП-Ассистент

SaaS-система управления проектной разработкой для микро-студий и проектных институтов.

**MVP:** матрица смежников + импорт Excel + Telegram-сводка в 09:00.

## Стек

| Слой | Технология |
|---|---|
| Backend | FastAPI + SQLAlchemy 2.0 + PostgreSQL 15 + Alembic |
| Frontend (app) | React 18 + TypeScript + Vite + shadcn/ui + TanStack Query |
| Website | Next.js 14 + TypeScript |
| Bot | aiogram 3.x |
| Infra | Docker Compose + Nginx + GitHub Actions |
| Python | 3.14 (локально) / 3.12 (в Docker) |

## Архитектура

Гексагональная (порты и адаптеры):

```
backend/src/
├── domain/       # чистая логика, не зависит от FastAPI/SQLAlchemy
├── application/  # use cases, оркестрация
├── adapters/     # db, api, notifications, import_export
├── config/       # настройки
└── bootstrap.py  # composition root
```

## Быстрый старт

```bash
# 1. Клонировать
git clone https://github.com/ABEL678/gip-assistant.git
cd gip-assistant

# 2. Подготовить окружение
copy .env.example .env

# 3. Запустить
docker compose -f docker/docker-compose.yml up -d --build

# 4. Проверить
curl http://localhost/api/health
```

| URL | Назначение |
|---|---|
| http://localhost/ | Лендинг (Next.js) |
| http://localhost/app | Приложение (React) |
| http://localhost/api | Backend (FastAPI) |
| http://localhost/api/docs | Swagger |

## Локальная разработка (без Docker)

```bash
# Backend
python -m venv .venv
.venv\Scripts\activate
pip install -e "backend[dev]"
uvicorn backend.src.main:app --reload

# Frontend
cd frontend
npm install
npm run dev

# Website
cd website
npm install
npm run dev
```

## Документы проекта

- `docs/ТЗ_ГИП-Ассистент_вер.3.0.md`
- `docs/Дорожная_карта_ГИП-Ассистент_вер.5.0.md`

## Статус

**MVP v0.1** — Этап 1.1 (технический скелет).