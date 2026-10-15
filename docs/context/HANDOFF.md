# HANDOFF.md — эстафета между сессиями

> **Назначение:** файл-эстафета. Пишется по запросу человека — перед
> завершением сессии в чате с ИИ-ассистентом (DeepSeek, ChatGPT, Claude),
> или при приближении к лимиту контекста.
> Читается первым в новом чате. Позволяет продолжить работу без потери контекста.

**Дата:** 15.10.2026
**Сессия:** 5.2f (закрыта)
**Статус:** закрыта

---

## 1. Что было в прошлой сессии (15.10.2026, сессии 5.2f-1 и 5.2f-2)

Закрыты unit-тесты для сервисов ГОСТ-документов:

- **5.2f-1:** test_document_type_service.py (10 тестов) + test_document_service.py (13 тестов).
- **5.2f-2:** test_document_version_service.py (15 тестов) + test_document_link_service.py (11 тестов).

**Результат:** 14 таблиц, 11 портов, 11 репозиториев, 8 сервисов,
39 эндпоинтов, 122 теста pytest (все зелёные).
Уровень 1.5 backend закрыт полностью.

**HEAD:** `333325a` (docs(context): remove duplicate line in CONTEXT).

## 2. Что делаем сейчас

Следующая сессия: 5.4 (UI DocumentsPage + DocumentVersionsPage + DocumentLinksPage).
Источник: `docs/tasks/5.4_prompt.md` (создать по мере надобности).

## 3. Что дальше

1. Сессия 5.4: UI для ГОСТ-документов.
2. Неделя 3: Библиотека шаблонов + MinIO.
3. Неделя 4: Auth + Telegram + деплой на VPS.
4. MVP-1.5: XML-модуль.

## 4. Что уже в контексте (не надо пересказывать)

- `docs/Дорожная_карта_6.4.md` — стратегия.
- `docs/ТЗ_4.4.md` — ТЗ (включая раздел 16 — ГОСТ-совместимость).
- `docs/context/CONTEXT.md` — резюме проекта (последнее обновление: 5.2f-2).
- `docs/context/TASKS.md` — статус (5.2f-2 закрыт, 122 теста).
- `docs/context/ARCHITECTURE.md` — структура.
- `docs/context/DATABASE.md` — 14 таблиц.
- `docs/context/API.md` — 39 эндпоинтов.
- `docs/context/RULES.md` — правила.
- `docs/context/HANDOFF.md` — эта эстафета.
- `AGENTS.md` — правила для GigaCode.

## 5. Открытые вопросы / блокеры

- [ ] GitHub Actions для авто-генерации DATABASE.md / API.md — не настроены.
- [ ] B027 (TaskRepository.get_by_pair) — техдолг Этапа 1.
- [ ] GigaCode запускает pytest/python -c не из корня — нужно явно указывать.

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
- **Текущий HEAD:** `333325a` (docs(context): remove duplicate line in CONTEXT)

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
    - Уровень 1.5 закрыт полностью. Сессия 5.4: UI для ГОСТ-документов.
    - Стиль тестов: backend/tests/test_entity_type_service.py.
    - Твоя роль: дать GigaCode промпт, проверить diff, помочь с ошибками.

    Продолжай.

---

**Конец HANDOFF.md.**
