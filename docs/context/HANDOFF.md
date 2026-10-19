# HANDOFF.md — эстафета между сессиями

> **Назначение:** файл-эстафета. Пишется по запросу человека — перед
> завершением сессии в чате с ИИ-ассистентом (DeepSeek, ChatGPT, Claude),
> или при приближении к лимиту контекста.
> Читается первым в новом чате. Позволяет продолжить работу без потери контекста.

**Дата:** 20.10.2026
**Сессия:** 6.8e-1 → 6.8e-2 (переход)
**Статус:** 6.8e-1 закрыт, 6.8e-2 не начат

---

## 1. Что было в сессии 6.8e-1

Четыре коммита:

| Коммит | Что |
|--------|-----|
| `03b285d` | Модель БД: 4 новые таблицы (revisions, changes, revision_decisions, stop_flags), premise_id к documents, Alembic-миграция `a1b2c3d4e5f7` |
| `d0a0979` | Фикс миграции: `create_type=False` на `sa.Enum` + `_create_enums_sync()` с `DO $$ BEGIN ... EXCEPTION WHEN duplicate_object THEN NULL; END $$` для чистых и грязных БД (PG < 14). Фикс дубликата `idx_tasks_to_section` в `d357e719c8bf`. | 225 |
| `72da399` | docs(specs): README — описание формата спеков | — |
| `7e80458` | Фикс docker: `POSTGRES_PASSWORD: ${DB_PASSWORD:-gip}` — вернуть fallback, запуск из корня | — |

**Итог 6.8e-1:** 4 таблицы (revisions, changes, revision_decisions, stop_flags), premise_id в documents. Enum-типы `change_status` и `revision_decision_type` создаются явно через `_create_enums_sync()` с `create_type=False` на колонках. Миграция работает на чистых и грязных БД, совместима с PG < 14. 225 passed, ruff чисто.

## 1.5. Что было в сессии 6.8b (архив)

Три подсессии, 5 коммитов:

| Подсессия | Коммит | Что | passed |
|-----------|--------|-----|--------|
| 6.8b-1 | `130c334` | GoalValidatorService — правила 1–6 (§6.1.1) + ValidationResult / ValidationEvidence DTO + Premise.data_field(name) хелпер + PremiseDataField перенесён в domain/value_objects/premise_data.py | 201 |
| 6.8b-1 fix | `fe894d0` | Rule 5 перед Rule 4 — убрать ложный no source for deadline при противоречии | 202 |
| 6.8b-2 | `21880b7` | SimilarityMatrixService — 10 связей (§6.2.1), поиск разделов (B): data["sections"], (C): строковые значения data | 212 |
| 6.8b-3 refactor | `964579d` | GoalValidatorService → ABC-порт в domain/ports/goal_validator.py; реализация → RuleBasedGoalValidator в domain/services/rule_based_goal_validator.py; спека §6.3.1 обновлена (unanimous/majority/split) | 212 |
| 6.8b-3 feat | `411932f` | ProposalProtocolService — unanimous / majority / split свод (§6.3.1) + ProtocolSummary DTO + 7 тестов | 219 |

**Итог 6.8b:** три сервиса готовы — RuleBasedGoalValidator (правила 1–6), SimilarityMatrixService (10 связей), ProposalProtocolService (протокол). 219 passed. ruff чисто.

## 2. Что делаем сейчас

**6.8e-2 — сервисы ревизий.**

- ✅ Промпт готов (спека §6.4.1 RevisionControlService + RevisionDiffService).
- ⏳ Код не начат.

Цель: `RevisionControlService` (создание/список/текущая версия) + `RevisionDiffService` (diff между версиями по changes).

## 2.5. Что было в сессии 6.8b (архив)

Ничего. 6.8b закрыт. Ждём старта 6.8c.

## 3. Что дальше (порядок — строгий)

1. **6.8e-2** — сервисы ревизий: `RevisionControlService` + `RevisionDiffService` (§6.4.1 спеки).
2. **6.8e-3** — DI + эндпоинты + тесты роутов для ревизий.
3. **6.8e-4** — UI (страница ревизий, карточки, diff-view).
4. Мерж в main — после 6.8e-4.

## 4. Что уже в контексте (не пересказывать)

- `docs/context/DOMAIN.md` v1.1 — онтология.
- `docs/Дорожная_карта_7.0.md` — стратегия.
- `docs/specs/spec_week_1.md` — финальная спека Вехи 1 (обновлена §6.3.1: unanimous/majority/split + абстракция GoalValidatorService).
- `docs/context/CONTEXT.md`, `TASKS.md`, `DATABASE.md` — обновлены.
- `AGENTS.md` — правила GigaCode.

## 5. Открытые вопросы

1. **Формат ответа similarity-matrix** — `{"links": [...]}` (как в примере §6.2.1) или голый список `[...]` (как в §7.1)? Рекомендация: `{"links": [...]}` — единообразно с другими эндпоинтами (список + метаданные).
2. **ValueError из validate → 404** — через HTTPException(status_code=404) в роуте (или через глобальный exception handler, если он уже есть в main.py).
3. **run-3-times в проде** — один валидатор (RuleBasedGoalValidator). В тестах — mock. Сервис уже принимает `list[GoalValidatorService]` — DI передаст `[rule_based]`.
4. **Техдолг:** в проекте два паттерна enum — UPPERCASE (`goal_state`, `premise_category`) и lowercase (`verification_status`). Унификация — веха 6 (или отдельный refactor).
5. **docker-compose.yml** — требует запуска из корня репозитория: `docker compose -f docker/docker-compose.yml up -d`. `.env` в корне подхватится через `env_file: ../.env`. Fallback `POSTGRES_PASSWORD: ${DB_PASSWORD:-gip}`.

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

    Мы на 6.8e-2. Задача: сервисы ревизий (RevisionControlService + RevisionDiffService, §6.4.1 спеки).
    6.8e-1 закрыт (4 таблицы: revisions, changes, revision_decisions, stop_flags; enum-фикс; 225 passed).
    Вопросы в §5 HANDOFF: формат similarity-matrix, ValueError→404, docker-compose запуск из корня.
    Твоя роль: дать GigaCode промпт, проверить diff, помочь с ошибками.

---

**Конец HANDOFF.md.**
