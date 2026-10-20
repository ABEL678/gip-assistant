# HANDOFF.md — эстафета между сессиями

> **Назначение:** файл-эстафета. Пишется по запросу человека — перед
> завершением сессии в чате с ИИ-ассистентом (DeepSeek, ChatGPT, Claude),
> или при приближении к лимиту контекста.
> Читается первым в новом чате. Позволяет продолжить работу без потери контекста.

**Дата:** 20.10.2026
**Сессия:** 6.8j → 6.9 (переход)
**Статус:** веха 1 закрыта, демо готово

---

## 1. Что было

**6.8i (эндпоинты Result + ProjectStandard):**
- ✅ ResultService + ProjectStandardService CRUD + валидации.
- ✅ 15 unit-тестов. Коммит `19d37c7`.

**6.8j-1 (UI Result + ProjectStandard):**
- ✅ ResultPage, ProjectStandardPage — страницы CRUD.
- ✅ ResultCard, ProjectStandardCard — карточки.
- ✅ ResultForm, ProjectStandardForm — формы.
- ✅ ResultGoalsPanel, StandardGoalsPanel — панели связей с целями.
- ✅ API-клиенты + хуки. Коммит `1d57292`.

**6.8j-2 (UI Revisions):**
- ✅ RevisionsPage — страница ревизий.
- ✅ RevisionCard — карточка ревизии.
- ✅ RevisionForm — форма создания ревизии.
- ✅ RevisionDiffPanel — просмотр diff между версиями.
- ✅ API-клиенты + хуки. Коммит `65f943b`.

**Итог:** веха 1 полностью готова. 271 passed. Демо для ГИПа готово.

## 2. Что делаем сейчас

**Демо вехи 1 (для ГИПа).**

Показать:
- Канвас (React Flow): вводные, цели, связи.
- CRUD: цели, вводные, результаты, стандарты.
- Валидация целей (6 правил).
- Матрица смежников.
- Протокол (unanimous/majority/split).
- Ревизии и diff.
- Документы (ГОСТ).

После демо → обратная связь → 6.9 (канвас).

## 3. Что дальше (порядок — строгий)

1. **Демо вехи 1** — показать ГИПу.
2. **Обратная связь** — собрать замечания.
3. **6.9 (канвас)** — улучшение канваса (§6.4.1 спеки).
4. **Мерж** — после 6.9.

## 4. Что уже в контексте (не пересказывать)

- `docs/context/DOMAIN.md` v1.1 — онтология.
- `docs/Дорожная_карта_7.0.md` — стратегия.
- `docs/specs/spec_week_1.md` — финальная спека Вехи 1.
- `docs/context/CONTEXT.md`, `TASKS.md`, `DATABASE.md` — обновлены.
- `AGENTS.md` — правила GigaCode.

## 5. Открытые вопросы

Нет.

## 6. Ключи / пути / команды

- **Проект:** `C:\Users\abelo\GIP-Assistant\gip-assistant`
- **Backend:** `cd backend && ..\.venv\Scripts\activate`
- **Backend (запуск):** `uvicorn backend.src.main:app --reload` (из корня)
- **Frontend:** `cd frontend && npm run dev`
- **Тесты:** `pytest backend/tests/ -v` (из корня)
- **Alembic:** `cd backend && ..\.venv\Scripts\activate && alembic current`
- **Ruff:** `.venv\Scripts\activate && ruff check backend/`
- **Docker:** `docker compose -f docker/docker-compose.yml up -d` (из корня, поднимает gip_db на 5555)
- **БД-инспекция:** `docker exec -it gip_db psql -U gip -d gip_assistant -c "..."` (юзер gip, БД gip_assistant)
- **GitHub:** https://github.com/ABEL678/gip-assistant

## 7. Как продолжить в новом чате

**Первое сообщение (для рутинного чата):**

    Привет. Продолжаем проект «ГИП-Ассистент». Прочитай:
    1. docs/context/HANDOFF.md
    2. docs/context/DOMAIN.md (v1.1)
    3. docs/Дорожная_карта_7.0.md
    4. docs/specs/spec_week_1.md
    5. docs/context/CONTEXT.md
    6. docs/context/TASKS.md
    7. AGENTS.md

    Мы на 6.9 (канвас). Веха 1 готова, демо для ГИПа.
    6.8i, 6.8j-1, 6.8j-2 закрыты. 271 passed.
    Твоя роль: дать GigaCode промпт, проверить diff, помочь с ошибками.

---

**Конец HANDOFF.md.**
