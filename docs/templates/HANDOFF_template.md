# HANDOFF.md — эстафета между сессиями

> **Назначение:** файл-эстафета. Пишется по запросу человека — перед
> завершением сессии в чате с ИИ-ассистентом (DeepSeek, ChatGPT, Claude),
> или при приближении к лимиту контекста.
> Читается первым в новом чате. Позволяет продолжить работу без потери контекста.

**Дата:** [DD.MM.YYYY]
**Сессия:** [номер]
**Статус:** [в работе / закрыта]

---

## 1. Что было в прошлой сессии

[краткое описание — 3-5 пунктов]

## 2. Что делаем сейчас

**Сессия [N.M] — [название].**

- **Прогресс:** [% или статус]
- **Промпт для GigaCode:** `docs/tasks/[N.M]_prompt.md`.
- **Источник истины:** [ТЗ 4.4, раздел X / другой].
- **Критерии готовности:** [список].

## 3. Что дальше

[следующие шаги — 3-5 пунктов]

## 4. Что уже в контексте (не надо пересказывать)

- `docs/Дорожная_карта_6.4.md` — стратегия.
- `docs/ТЗ_4.4.md` — ТЗ.
- `docs/context/CONTEXT.md` — резюме.
- `docs/context/TASKS.md` — статус.
- `docs/context/ARCHITECTURE.md` — структура.
- `docs/context/DATABASE.md` — схема БД.
- `docs/context/API.md` — эндпоинты.
- `docs/context/RULES.md` — правила.
- `AGENTS.md` — правила для GigaCode.

## 5. Открытые вопросы / блокеры

- [ ] [вопрос 1]

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

**Первое сообщение:**

    Привет. Продолжаем проект «ГИП-Ассистент».

    Прочитай (по порядку):
    1. docs/context/HANDOFF.md
    2. docs/context/CONTEXT.md
    3. docs/context/TASKS.md
    4. docs/context/ARCHITECTURE.md
    5. AGENTS.md

    Дальше:
    - Мы на сессии [N.M].
    - Задача: [название].
    - Полный промпт для GigaCode — в docs/tasks/[N.M]_prompt.md.
    - Твоя роль: дать GigaCode промпт, проверить diff, помочь с ошибками.

    Продолжай.

---

**Конец HANDOFF_template.md.**
