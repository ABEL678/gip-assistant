# HANDOFF.md — эстафета между сессиями

> **Назначение:** файл-эстафета. Пишется по запросу человека — перед
> завершением сессии в чате с ИИ-ассистентом (DeepSeek, ChatGPT, Claude),
> или при приближении к лимиту контекста.
> Читается первым в новом чате. Позволяет продолжить работу без потери контекста.

**Дата:** 18.10.2026
**Сессия:** 6.8a
**Статус:** закрыта

---

## 1. Что было в прошлой сессии

- ✅ `VerificationStatus(StrEnum)` — CONFIRMED, NOT_CONFIRMED, REQUIRES_CHECK, NO_DATA
- ✅ Goal entity: поле `verification_status` (после state, default REQUIRES_CHECK)
- ✅ GoalModel: колонка + индекс `idx_goals_verification_status`
- ✅ GoalRepository: mapping `_to_domain` / `_to_model` (с защитой от None)
- ✅ DTO: `GoalSchema` + `GoalProposal` с verification_status; `GoalUpdate` — не трогать
- ✅ `PremiseDataField` — типизированное поле data с owner/source + field_validator (coerce plain values)
- ✅ Миграция `cd056578f798` (upgrade + downgrade)
- ✅ Тесты: 193 passed (все, включая интеграционный)
- ✅ Исправление: `values_callable=lambda e: [x.value for x in e]` — lowercase enum в БД

## 2. Что делаем сейчас

**Сессия 6.8b — сервисы (CRUD + валидатор + матрица + протокол).**

- **Прогресс:** 0% — не начато
- **Промпт для GigaCode:** `docs/tasks/6.8b_prompt.md` (создать из шаблона)
- **Источник истины:** `docs/specs/spec_week_1.md` §4, §4.1, §5
- **Критерии готовности:** сервисы CRUD + агент-валидатор + матрица смежников + протокол 2–3 прогонов

## 3. Что дальше

1. Создать промпт `docs/tasks/6.8b_prompt.md` из шаблона
2. 6.8b — сервисы: GoalService (CRUD + verification_status валидатор), PremiseService (обновление)
3. 6.8c — эндпоинты (CRUD + 3 эндпоинта) + тесты
4. 6.8d — UI (страницы, карточки, статус, владелец)
5. Мержить в main, удалять ветку

## 4. Что уже в контексте (не надо пересказывать)

- `docs/Дорожная_карта_7.0.md` — стратегия.
- `docs/context/CONTEXT.md` — резюме.
- `docs/context/TASKS.md` — статус.
- `docs/context/ARCHITECTURE.md` — структура.
- `docs/context/DATABASE.md` — схема БД.
- `docs/context/API.md` — эндпоинты.
- `docs/context/RULES.md` — правила.
- `docs/context/DOMAIN.md` — онтология.
- `docs/specs/spec_week_1.md` — финальная спека Вехи 1.
- `AGENTS.md` — правила для GigaCode.

## 5. Открытые вопросы / блокеры

- [x] DATABASE.md обновлён: goals.verification_status + idx_goals_verification_status (коммит docs: ...).

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
    - Мы на сессии 6.8b.
    - Задача: сервисы (CRUD + валидатор + матрица + протокол).
    - Полный промпт для GigaCode — в docs/tasks/6.8b_prompt.md.
    - Твоя роль: дать GigaCode промпт, проверить diff, помочь с ошибками.

    Продолжай.

---

**Конец HANDOFF.md.**
