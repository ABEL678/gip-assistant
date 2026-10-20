# HANDOFF.md — эстафета между сессиями

> **Назначение:** файл-эстафета. Пишется по запросу человека — перед
> завершением сессии в чате с ИИ-ассистентом (DeepSeek, ChatGPT, Claude),
> или при приближении к лимиту контекста.
> Читается первым в новом чате. Позволяет продолжить работу без потери контекста.

**Дата:** 20.10.2026
**Сессия:** 6.10e → Веха 3 (переход)
**Статус:** Веха 2 закрыта, 288 passed, готовы к вехе 3.

---

## 1. Что было

**6.10a — модель Action + миграция `f9eba6941cdf`.**
- ✅ Action model, DTO, порты, репозитории.
- ✅ Коммит `953b558`.

**6.10b — Task.is_complex (без удаления CrossTask).**
- ✅ `Task.is_complex` — новое поле.
- ✅ Коммит `f5a527d`.

**6.10c — ActionService + TaskService + 10 тестов.**
- ✅ CRUD-сервисы + валидации.
- ✅ Коммит `07ea2c3`.

**6.10d — эндпоинты Action (6 штук) + DI + 7 тестов роутов.**
- ✅ POST/PATCH/DELETE /api/actions, GET /api/projects/{id}/actions, GET /api/tasks/{id}/actions.
- ✅ Коммит `ddnf57c`.

**6.10e — UI Action (ActionsPage, ActionCard, ActionForm, useActions) + интеграция в ProjectPage.**
- ✅ Frontend build успешен.
- ✅ Коммит `4b1a50d`.

**Итог:** 288 passed, frontend build зелёный, веха 2 закрыта.

## 2. Что делаем сейчас

**Веха 2 закрыта.**

Следующая подсессия — Веха 3 (Decision + Norm + DecisionLink).

## 3. Что дальше (порядок строгий)

1. **6.11a** — модель Decision + миграция + DTO + порты + репозитории.
2. **6.11b** — модель Norm + DecisionLink + миграция.
3. **6.11c** — сервисы DecisionService, NormService, DecisionLinkService.
4. **6.11d** — эндпоинты + DI.
5. **6.11e** — UI (DecisionsPage, NormsPage, DecisionLinkPage).

## 4. Что уже в контексте (не пересказывать)

- `docs/context/DOMAIN.md` v1.1 — онтология ядра. **Главный документ.**
- `docs/Дорожная_карта_7.0.md` — стратегия.
- `docs/specs/spec_week_1.md` — финальная спека Вехи 1.
- `docs/context/CONTEXT.md`, `TASKS.md`, `DATABASE.md`, `API.md`, `RULES.md`, `ARCHITECTURE.md` — обновлены.
- `AGENTS.md` — правила GigaCode.

## 5. Открытые вопросы

- [ ] 6.10f (интеграция Action с Task) — отложено (сделаем после вехи 3 или в 6.12).
- [ ] `responsible_id` в ActionForm — не добавлен (нет API users — появится в вехе 6).

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

    Привет. Продолжаем «ГИП-Ассистент». Прочитай:
    1. docs/context/HANDOFF.md
    2. docs/context/DOMAIN.md (v1.1)
    3. docs/Дорожная_карта_7.0.md
    4. docs/specs/spec_week_1.md
    5. docs/context/CONTEXT.md
    6. docs/context/TASKS.md
    7. AGENTS.md

    Мы на вехе 3 (Decision + Norm + DecisionLink).
    Веха 2 закрыта (6.10a–6.10e, 288 passed).
    Твоя роль: дать GigaCode промпт на 6.11a, проверить diff, помочь с ошибками.

---

**Конец HANDOFF.md.**
