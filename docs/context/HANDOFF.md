# HANDOFF.md — эстафета между сессиями

> **Назначение:** файл-эстафета. Пишется по запросу человека — перед
> завершением сессии в чате с ИИ-ассистентом (DeepSeek, ChatGPT, Claude),
> или при приближении к лимиту контекста.
> Читается первым в новом чате. Позволяет продолжить работу без потери контекста.

**Дата:** 14.10.2026
**Сессия:** 5.2f (пауза до 15.10.2026)
**Статус:** закрыта (пауза до завтра)

---

## 1. Что было в прошлой сессии (14.10.2026, сессия 5.2e)

Закрыт Уровень 1.5 (backend) — 8 подсессий:

- **5.1:** домен + модели + миграция (4 таблицы, 8 сидов).
- **5.2a:** 4 порта репозиториев.
- **5.2b:** 4 DTO-файла (13 Pydantic-классов).
- **5.2c-1:** 4 SQLAlchemy-репозитория (Enum-маппинг).
- **5.2c-2:** 8 smoke-тестов маппинга.
- **5.2d:** 4 доменных сервиса (валидации, set_current, delete).
- **5.2e-1:** DI (2 __init__.py + dependencies.py).
- **5.2e-2/3:** 4 роутера (22 эндпоинта) + main.py + API.md.

**Результат:** 14 таблиц, 11 портов, 11 репозиториев, 8 сервисов,
39 эндпоинтов, 73 теста pytest (все зелёные).

**HEAD:** `b0de1f7` (feat(api): add document routes + context sync).

## 2. Что делаем сейчас

**Сессия 5.2f-1 — Unit-тесты сервисов: DocumentTypeService + DocumentService.**

- **Прогресс:** 0% — начинаем с нуля.
- **Источник истины:** `docs/tasks/5.2f-1_prompt.md` (создать).
- **Критерии готовности:**
  - `backend/tests/test_document_type_service.py` — ~7 тестов.
  - `backend/tests/test_document_service.py` — ~9 тестов.
  - Стиль: AsyncMock, @pytest.mark.asyncio, фикстуры (см. test_entity_type_service.py).
  - Покрытие: create (успех + ValueError), get_by_id, list, update (частично), delete.
  - 73 старых теста зелёные, итого — ~89 тестов.
  - TASKS.md и CONTEXT.md обновлены.
- **НЕ делать:** тесты DocumentVersion + DocumentLink (это 5.2f-2).

## 3. Что дальше

1. **Сессия 5.2f-1** (завтра): тесты DocumentType + Document.
2. **Сессия 5.2f-2:** тесты DocumentVersion + DocumentLink.
   Цель: ~100 тестов pytest. Backend 1.5 закрыт.
3. **Сессия 5.4:** UI DocumentsPage + DocumentVersionsPage + DocumentLinksPage.
4. **Потом:** Auth (JWT), Telegram-сводка, деплой на VPS.
5. **MVP-1.5:** XML-модуль.

## 4. Что уже в контексте (не надо пересказывать)

- `docs/Дорожная_карта_6.4.md` — стратегия.
- `docs/ТЗ_4.4.md` — ТЗ (включая раздел 16 — ГОСТ-совместимость).
- `docs/context/CONTEXT.md` — резюме проекта (последнее обновление: 5.2e).
- `docs/context/TASKS.md` — статус (5.2e закрыт).
- `docs/context/ARCHITECTURE.md` — структура.
- `docs/context/DATABASE.md` — 14 таблиц.
- `docs/context/API.md` — 39 эндпоинтов.
- `docs/context/RULES.md` — правила.
- `docs/context/HANDOFF.md` — эта эстафета.
- `AGENTS.md` — правила для GigaCode.

## 5. Открытые вопросы / блокеры

- [ ] GigaCode запускает `python -c` без активации .venv → ImportError.
      Решение: обновить AGENTS.md — правило «Для python -c: .venv\Scripts\activate && python -c ...».
- [ ] GigaCode делает отдельный коммит вместо amend. Решение: явно указывать «amend» в промпте.
- [ ] Проверять импорты DTO при планировании роутов (сегодня: DocumentTypeUpdate забыт в 5.2b).
- [ ] GitHub Actions для авто-генерации DATABASE.md / API.md — не настроены.
- [ ] Промпт для 5.2f-1 — создать `docs/tasks/5.2f-1_prompt.md` (завтра).

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
- **Текущий HEAD:** `b0de1f7` (feat(api): add document routes + context sync)

## 7. Как продолжить в новом чате

**Первое сообщение в новом чате с DeepSeek (или другим ИИ):**

    Привет. Продолжаем проект «ГИП-Ассистент».

    Прочитай (по порядку):
    1. docs/context/HANDOFF.md — что было и что дальше.
    2. docs/context/CONTEXT.md — что за продукт.
    3. docs/context/TASKS.md — что сделано.
    4. docs/context/ARCHITECTURE.md — структура.
    5. AGENTS.md — правила для GigaCode.

    Дальше:
    - Уровень 1.5, Сессия 5.2f-1 (тесты DocumentType + Document).
    - Стиль тестов: backend/tests/test_entity_type_service.py.
    - Твоя роль: дать GigaCode промпт, проверить diff, помочь с ошибками.

    Продолжай.

---

**Конец HANDOFF.md.**
