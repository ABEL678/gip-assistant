# ГИП-Ассистент

> SaaS-система управления проектной разработкой для микро-студий, частных ГИПов и проектных институтов.

**Ключевая идея:** мы не заставляем менять рабочий процесс. Мы встраиваемся в существующий Excel ГИПа, превращаем его в удобный интерфейс с универсальными сущностями и на выходе отдаём документы в XML-формате, требуемом государственной экспертизой.

---

## Что решает

| Боль ГИПа | Частота (из 12 интервью) | Решение |
|-----------|--------------------------|---------|
| Координация смежников | 10/12 | Матрица смежников + задачи пары |
| Контроль просрочек | 9/12 | Telegram-сводка в 09:00 |
| Потеря задач | 8/12 | Универсальные сущности (EntityType + Entity) |
| Согласования | 7/12 | MVP-2 |
| Изменения / РВИ | 6/12 | MVP-2 |

---

## Стек

| Слой | Технология |
|------|-----------|
| Backend | FastAPI + SQLAlchemy 2.0 async + PostgreSQL 15 + Alembic |
| Frontend (app) | React 18 + TypeScript + Vite + shadcn/ui + TanStack Query |
| Website | Next.js 14 + TypeScript |
| Bot | aiogram 3.x (Telegram) |
| Storage (MVP-1.5) | MinIO AIStor Free (S3-совместимое) |
| LLM (MVP-3) | Qwen 2.5 7B (локально, VPS 16 GB RAM) |
| XML (MVP-1.5) | lxml + xmlschema (валидация по XSD Минстроя) |
| AI-инструменты (разработка) | GigaCode + самописный агент на GigaChat API |
| Инфра | Docker Compose + Nginx + GitHub Actions |
| Python | 3.14+ |
| Node.js | 24+ |

---

## Архитектура

**Гексагональная** (порты и адаптеры):

    backend/src/
    ├── domain/       # чистая логика, не зависит от FastAPI/SQLAlchemy
    │   ├── entities/     # сущности (Project, Task, EntityType, Entity)
    │   ├── value_objects/# Enum'ы
    │   ├── ports/        # ABC-интерфейсы репозиториев
    │   └── services/     # доменные сервисы
    ├── application/  # use cases, DTO
    │   ├── dto/          # Pydantic-схемы
    │   └── use_cases/    # оркестрация
    ├── adapters/     # инфраструктура
    │   ├── db/           # SQLAlchemy, репозитории
    │   ├── api/          # FastAPI роуты, DI
    │   ├── notifications/# Telegram
    │   ├── import_export/# Excel
    │   ├── storage/      # MinIO (MVP-1.5)
    │   ├── xml/          # XML (MVP-1.5)
    │   └── llm/          # Qwen (MVP-3)
    ├── config/       # настройки
    └── bootstrap.py  # composition root

**Правило:** зависимости идут **внутрь** (adapters → application → domain). Домен **не знает** про FastAPI, SQLAlchemy, HTTP.

---

## Статус

| Этап | Что | Статус |
|------|-----|--------|
| 0 | Подготовка (ИП, домен, интервью) | ✅ |
| 1 | Прототип (импорт Excel, матрица, TaskList, бот) | ✅ |
| 2 | MVP (Уровень 1 backend) | ✅ |
| 2 | MVP (Уровень 1 UI) | 🔄 в работе |
| 2 | MVP (нед. 3-5: шаблоны, MinIO, Auth, деплой, лендинг) | ⏳ |
| 2.5 | MVP-1.5 (XML-формат ПД) | ⏳ |
| 3 | MVP-2 (согласования, тома, финансы) | ⏳ |
| 4 | MVP-3 (LLM-ассистент) | ⏳ |

**Тесты:** 65 passed (pytest).
**Таблиц в БД:** 10.
**Эндпоинтов API:** 17.

---

## Быстрый старт

### С Docker (рекомендуется)

    git clone https://github.com/ABEL678/gip-assistant.git
    cd gip-assistant
    copy .env.example .env
    docker compose -f docker/docker-compose.yml up -d --build
    curl http://localhost/api/health

| URL | Назначение |
|-----|-----------|
| http://localhost/ | Лендинг (Next.js) — MVP-1.5 |
| http://localhost/app | Приложение (React) |
| http://localhost/api | Backend (FastAPI) |
| http://localhost/api/docs | Swagger UI |
| http://localhost/storage | MinIO Console (MVP-1.5) |

### Локально (без Docker)

**Backend:**

    python -m venv .venv
    .venv\Scripts\activate
    pip install -e "backend[dev]"
    uvicorn backend.src.main:app --reload

**Frontend:**

    cd frontend
    npm install
    npm run dev

**Тесты:**

    cd /d C:\Users\abelo\GIP-Assistant\gip-assistant
    .venv\Scripts\activate
    pytest backend/tests/ -v

**Alembic:**

    cd backend
    alembic current
    alembic upgrade head

---

## Документация

Карта документации — **[`docs/README.md`](docs/README.md)**: что читать
и в каком порядке (Закон → Спеки → Статус → Рабочее).

- `docs/context/DOMAIN.md` — онтология ядра, главный документ.
- `docs/context/CONTEXT.md` — резюме продукта (2 страницы).
- `docs/context/TASKS.md` — статус и журнал.
- `docs/specs/` — спеки вех.
- `AGENTS.md` — правила для ИИ-агентов.

---

## Структура репозитория

    gip-assistant/
    ├── backend/          # FastAPI + SQLAlchemy
    │   ├── src/
    │   │   ├── domain/
    │   │   ├── application/
    │   │   ├── adapters/
    │   │   ├── config/
    │   │   └── main.py
    │   ├── alembic/
    │   ├── tests/
    │   └── scripts/      # ai_agent/, generate_ai_context.py
    ├── frontend/         # React + Vite
    ├── website/          # Next.js (лендинг, MVP-1.5)
    ├── docker/           # Dockerfile'ы, docker-compose.yml, nginx.conf
    ├── docs/             # документация — карта docs/README.md
    ├── .github/workflows/# CI
    ├── AGENTS.md         # правила для ИИ-агентов
    └── README.md         # этот файл

---

## Технологические запреты (MVP)

**НЕ используем:**

- Celery, Redis, RabbitMQ
- Webhooks
- Публичные облачные LLM
- MinIO Community Edition (архивирован)
- Claude Code (недоступен без VPN)
- Cursor Composer (требует иностранных карт)

**Используем:**

- Синхронные запросы
- BackgroundTasks FastAPI + отдельный воркер
- Docker Compose с первого дня
- MinIO AIStor Free
- Qwen 2.5 7B локально (MVP-3)
- GigaCode (PyCharm) + самописный агент на GigaChat API

---

## Контакты

- **GitHub:** https://github.com/ABEL678/gip-assistant
- **Домен (план):** gip-assistant.ru
- **Автор:** ИП, ГИП-руководитель

**Статус:** MVP v0.2 — Уровень 1 backend готов, UI в работе.