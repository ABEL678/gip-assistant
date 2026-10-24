# HANDOFF.md — эстафета между сессиями

> **Назначение:** файл-эстафета. Пишется по запросу человека — перед
> завершением сессии в чате с ИИ-ассистентом (DeepSeek, ChatGPT, Claude),
> или при приближении к лимиту контекста.
> Читается первым в новом чате. Позволяет продолжить работу без потери контекста.

**Дата:** 22.10.2026
**Сессия:** Веха 3 → Веха 4 (RFI)
**Статус:** Веха 3 ЗАКРЫТА полностью (6.11a → 6.11b → 6.11c → 6.11d → 6.11e). 392 теста, frontend build зелёный.

---

## 1. Что было в прошлой сессии

**Веха 3 — полностью закрыта (22.10.2026):**

- ✅ **6.11a** — модель Decision + миграция `8aad8fd713f0` (298 тестов).
- ✅ **6.11b** — модели Norm + DecisionLink + DecisionNorm + миграция `c52a3c176d47` (310 тестов).
- ✅ **6.11c** — 5 сервисов + DecisionProposalService (2 правила) (366 тестов).
- ✅ **6.11d** — 21 эндпоинт (decisions 7, norms 5, decision-links 5, decision-norms 4) + 26 тестов роутов (392 теста).
- ✅ **6.11e** — UI: 4 API-клиента, 3 хука, 7 компонентов, 3 страницы (DecisionsPage, NormsPage, DecisionLinkPage), роутинг.

**Коммиты вехи 3:** `8fa1bd8` (6.11b), `d35aee4` (6.11c), `ca297f5` (6.11d), `85822e4` (6.11e).

**Итог вехи 3:**
- 392 теста pytest.
- 27 таблиц в БД.
- 60+ эндпоинтов API.
- Весь стек: domain → application → adapters → frontend.

## 2. Что делаем сейчас

**Веха 3 закрыта. Переход к Вехе 4 (RFI).**

**Цель вехи 4:** «живые вводные» — RFI как особый Task, Document ↔ Action, агент RFI.

**Порядок подсессий (план, не утверждён до спеки):**
- **6.12a** — модель RFI + миграция + DTO + порты + репозитории.
- **6.12b** — Document ↔ Action (связь) + «живые вводные» (RFI → Premise).
- **6.12c** — RfiService + правила (для решения X нет ИД больше N дней).
- **6.12d** — эндпоинты + DI.
- **6.12e** — UI (RfiPage, RfiCard, RfiForm).
- **6.12f** — Агент RFI (первый автономный агент, `DOMAIN.md §9.2`).

**ВАЖНО: спеки на веху 4 НЕТ.** Первый шаг — написать `docs/specs/spec_week_4.md` (по образцу spec_week_1/3). Код — после спеки.

## 3. Что дальше

1. **Спека вехи 4** (`spec_week_4.md`) — по образцу `spec_week_3.md`, §1–§12.
2. **6.12a** — модель RFI.
3. **6.12b** — Document ↔ Action.
4. **6.12c** — сервис.
5. **6.12d** — эндпоинты.
6. **6.12e** — UI.
7. **6.12f** — агент RFI.
8. После вехи 4 — «Очередь после вехи 3» (дашборд, скелет, отчёты, экспорт, поиск) — теперь уже «после вехи 4».

## 4. Что уже в контексте (не надо пересказывать)

- `docs/context/DOMAIN.md` v1.1 — онтология ядра. **Главный документ.**
- `docs/Дорожная_карта_7.0.md` — стратегия.
- `docs/specs/spec_week_3.md` — финальная спека Вехи 3.
- `docs/context/CONTEXT.md` v2.13 — резюме.
- `docs/context/TASKS.md` v2.5 — статус.
- `docs/context/ARCHITECTURE.md` — структура.
- `docs/context/DATABASE.md` — схема БД.
- `docs/context/API.md` v1.1 — эндпоинты.
- `docs/context/RULES.md` — правила.
- `AGENTS.md` — правила для GigaCode.
- `GIGACODE.md` v1.3 — правила (адаптация под GigaIDE + GLM-5.3).

## 5. Открытые вопросы / блокеры

- [ ] **`decision_id` в домене Task** — отклонение от спеки §2.1 (6.11a). В домене Task есть поле decision_id, но в спеке связь только через FK в БД. Зафиксировано в TASKS.md §4. Решение: узаконить или откатить — в вехе 4 или позже.
- [ ] **API.md baseline** — несвежий (до 6.11d не включал Actions, Results, ProjectStandards, Revisions). Полная сверка с фактическими роутерами — отдельная задача.
- [ ] **CONTEXT.md** — §4/§6 всё ещё ссылается на `docs/archive/` — почистить.

**Блокеров нет.**

## 6. Ключи / пути / команды

- **Проект:** `C:\Users\abelo\GIP-Assistant\gip-assistant`
- **Инструменты:** GigaIDE + GLM-5.3 (Cloud.ru). Встроенный терминал GigaIDE висит на Windows — известный баг. Все команды Git/Alembic/pytest — через **внешний CMD** (открыть из Пуск, `cd` в проект).
- **Backend (запуск):** `uvicorn backend.src.main:app --reload` (из корня, внешний CMD).
- **Backend (venv):** `cd backend && ..\.venv\Scripts\activate`
- **Frontend:** `cd frontend && npm run dev`
- **Тесты:** `pytest backend/tests/ -v` (из корня, внешний CMD).
- **Alembic:** `cd backend && ..\.venv\Scripts\activate && alembic current` / `alembic upgrade head` (из backend/, внешний CMD).
- **Ruff:** `.venv\Scripts\activate && ruff check backend/`
- **Docker:** `docker compose -f docker/docker-compose.yml up -d` (из корня, поднимает gip_db на 5555).
- **БД-инспекция:** `docker exec -it gip_db psql -U gip -d gip_assistant -c "..."` (юзер gip, БД gip_assistant).
- **GitHub:** https://github.com/ABEL678/gip-assistant

## 7. Как продолжить в новом чате

**Первое сообщение (для рутинного чата):**

    Привет. Продолжаем «ГИП-Ассистент». Прочитай:
    1. docs/context/HANDOFF.md
    2. docs/context/DOMAIN.md (v1.1)
    3. docs/specs/spec_week_3.md (образец для спеки вехи 4)
    4. docs/context/CONTEXT.md
    5. docs/context/TASKS.md
    6. AGENTS.md + GIGACODE.md

    Веха 3 закрыта (392 passed, миграции 8aad8fd713f0 + c52a3c176d47).
    Переходим к вехе 4 (RFI). Спеки на веху 4 нет — первый шаг:
    написать docs/specs/spec_week_4.md по образцу spec_week_3.md.

    Твоя роль: написать спеку вехи 4, проверить её, дать промпт на 6.12a.

---

**Конец HANDOFF.md.**
