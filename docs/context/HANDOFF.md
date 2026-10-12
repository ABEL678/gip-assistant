# HANDOFF.md — эстафета между сессиями

> **Назначение:** файл-эстафета. Пишется по запросу человека — перед
> завершением сессии в чате с ИИ-ассистентом (DeepSeek, ChatGPT, Claude),
> или при приближении к лимиту контекста.
> Читается первым в новом чате. Позволяет продолжить работу без потери контекста.

**Дата:** 13.10.2026
**Сессия:** 5
**Статус:** закрыта (пауза до следующей сессии)

---

## 1. Что было в прошлой сессии (12.10.2026, сессия 4)

- Закрыт Уровень 1 (MVP): backend + frontend UI.
- Создано 12 файлов UI (entityApi, хуки, страницы, компоненты).
- Интеграция в ProjectPage.tsx (секция «Типы сущностей»).
- Обновлён AGENTS.md — правило авто-синхронизации контекста.
- Создан HANDOFF.md — механизм передачи между сессиями.

## 2. Что делаем сейчас

**Пауза.** Сессия 5 закрыта. Следующая — Сессия 5.1 (начнём позже).

**Задача на следующий раз:** Сессия 5.1 — Домен + SQLAlchemy-модели + миграция для ГОСТ-документов.

- **Файлы (новые):**
  - `backend/src/domain/entities/document.py`
  - `backend/src/domain/entities/document_version.py`
  - `backend/src/domain/entities/document_link.py`
  - `backend/src/domain/entities/document_type.py`
  - `backend/src/domain/value_objects/document.py` (4 Enum)
  - `backend/src/adapters/db/models/document_type.py`
  - `backend/src/adapters/db/models/document.py`
  - `backend/src/adapters/db/models/document_version.py`
  - `backend/src/adapters/db/models/document_link.py`
  - Обновить `backend/src/adapters/db/models/__init__.py`
  - Миграция Alembic (autogenerate) + сиды document_types

- **Прогресс:** 0% — ещё не начато.

- **Промпт для GigaCode:** в чате с DeepSeek (сохранён в истории, при необходимости — переформулировать по ТЗ 4.4, раздел 4.4).

## 3. Что дальше

1. **Сессия 5.1:** домен + модели + миграция (1 задача GigaCode).
2. **Сессия 5.2:** DTO + репозитории + сервисы.
3. **Сессия 5.3:** API + DI + тесты.
4. **Сессия 5.4:** UI (DocumentsPage) — позже.
5. **Потом:** Уровень 2 (шаблоны 6 типов), Auth, деплой.

## 4. Что уже в контексте (не надо пересказывать)

- `docs/Дорожная_карта_6.4.md` — стратегия.
- `docs/ТЗ_4.4.md` — ТЗ (включая раздел 16 — ГОСТ-совместимость).
- `docs/context/CONTEXT.md` — резюме проекта.
- `docs/context/TASKS.md` — статус.
- `docs/context/ARCHITECTURE.md` — структура.
- `docs/context/DATABASE.md` — схема БД (10 таблиц).
- `docs/context/API.md` — эндпоинты.
- `docs/context/RULES.md` — правила.
- `AGENTS.md` — правила для GigaCode (включая авто-синхронизацию контекста и HANDOFF).

## 5. Открытые вопросы / блокеры

- [ ] **GigaCode иногда выполняет задачу частично** — нужно проверять чек-лист по пунктам.
- [ ] **Первая проверка авто-синхронизации** — GigaCode должен сам обновить TASKS.md и CONTEXT.md после Сессии 5.1. Если не сделает — нужно поправить правило в AGENTS.md.
- [ ] **GitHub Actions** для авто-генерации DATABASE.md / API.md / RULES.md — не настроены (отложены).

## 6. Ключи / пути / команды

- **Проект:** `C:\Users\abelo\GIP-Assistant\gip-assistant`
- **Backend:** `cd backend && ..\.venv\Scripts\activate`
- **Backend (запуск):** `uvicorn backend.src.main:app --reload` (из корня)
- **Frontend:** `cd frontend && npm run dev`
- **Тесты:** `pytest backend/tests/ -v` (из корня)
- **Alembic:** `cd backend && ..\.venv\Scripts\activate && alembic current`
- **Ruff:** `.venv\Scripts\activate && ruff check backend/`
- **БД:** Docker `gip_db` на 5555
- **GitHub:** https://github.com/ABEL678/gip-assistant

## 7. Как продолжить в новом чате

**Первое сообщение в новом чате с DeepSeek (или другим ИИ):**

    Привет. Продолжаем проект «ГИП-Ассистент».

    Прочитай:
    1. docs/context/HANDOFF.md — что было и что дальше.
    2. docs/context/CONTEXT.md — что за продукт.
    3. docs/context/TASKS.md — что сделано.

    Дальше — продолжай с Сессии 5.1 (домен + модели для Document).
    Промпт для GigaCode — см. в HANDOFF.md, раздел 2.

    Правила работы — в AGENTS.md.

---

**Конец HANDOFF.md.**
