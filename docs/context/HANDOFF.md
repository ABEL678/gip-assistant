# HANDOFF.md — эстафета между сессиями

> **Назначение:** файл-эстафета. Пишется по запросу человека — перед
> завершением сессии в чате с ИИ-ассистентом (DeepSeek, ChatGPT, Claude),
> или при приближении к лимиту контекста.
> Читается первым в новом чате. Позволяет продолжить работу без потери контекста.

**Дата:** 17.10.2026
**Сессия:** 6.3 (закрыта) — веха 1a–1d
**Статус:** закрыта

---

## 1. Что было в этой сессии (17.10.2026, веха 1a–1d)

**Веха 1a: домен + модели + миграция**
- Домен: Premise, Goal, GoalProposal (dataclass).
- SQLAlchemy-модели: PremiseModel, GoalModel, GoalPremiseModel.
- Миграция 686491cea3fd (premises + goals + goal_premises).
- smoke-тесты маппинга.

**Веха 1b: DTO + порты + репозитории**
- DTO: PremiseSchema (4 схемы), GoalSchema (5 схем), GoalProposal, GoalProposalApprove.
- Порты: PremiseRepository, GoalRepository (2 ABC).
- Репозитории: SqlAlchemyPremiseRepository, SqlAlchemyGoalRepository (CRUD).

**Веха 1c: сервисы + 4 правила вывода**
- PremiseService (CRUD).
- GoalService (CRUD).
- GoalProposalService (4 правила: договор_срок, тз_требование, требование_заказчика, просроченный_ид).
- Enum-паттерн: `Enum(EnumClass, name="...", create_type=False)`.
- DateTime(timezone=True) для timestamp-полей.
- Дедупликация proposals по нормализованной formulation.

**Веха 1d: DI + эндпоинты + тесты роутов**
- DI: `dependencies.py` — PremiseServiceDep, GoalServiceDep, GoalProposalServiceDep (6 зависимостей).
- Роуты: `premises.py` (5 эндпоинтов CRUD) + `goals.py` (7 эндпоинтов: CRUD + proposals + from-proposal).
- 17 тестов роутов: `test_premises_routes.py` (7) + `test_goals_routes.py` (10).
- httpx.AsyncClient + ASGITransport — обход проблемы FastAPI 0.143.x + TestClient.
- Все 187 тестов pytest проходят (170 старых + 17 новых).
- AGENTS.md обновлён: правила для тестов роутов и «не удалять тесты».

---

## 2. Что делаем сейчас

Ничего в коде. Веха 1a–1d закрыта.

---

## 3. Что дальше

1. **Веха 1f — UI:**
   - PremisesPage.tsx, GoalsPage.tsx.
   - GoalProposalList.tsx.
   - premiseApi.ts, goalApi.ts.
   - usePremises, useGoals.
   - PremiseCard, PremiseForm, GoalCard, GoalForm.
2. **Затем — веха 2** (Action + Task-адаптация).

---

## 4. Что уже в контексте (не надо пересказывать)

- **`docs/context/DOMAIN.md`** — v1.1. Главный документ онтологии. Читать первым.
- `docs/archive/Дорожная_карта_6.4.md` (архив).
- `docs/archive/ТЗ_4.4.md` (архив).
- `docs/context/CONTEXT.md` — v2.2 (обновлено после 1d).
- `docs/context/TASKS.md` — v2.2 (обновлено после 1d).
- `docs/context/ARCHITECTURE.md` — структура.
- `docs/context/DATABASE.md` — 17 таблиц.
- `docs/context/API.md` — 51 эндпоинт.
- `docs/context/RULES.md` — правила кода.
- `docs/specs/spec_week_1.md` — спека вехи 1.
- `AGENTS.md` — v1.2 (правила для GigaCode, включая тесты роутов).

---

## 5. Открытые вопросы / блокеры

**Открытые вопросы (из DOMAIN.md §11):**

- [ ] Явная сущность «Вводная» или каждая категория — отдельная?
- [ ] Методы управления — явная сущность или производная?
- [ ] Связь Action ↔ Document: 1:1 или M:N?
- [ ] Decision ↔ Decision: как формализовать последовательные/вложенные?
- [ ] Приоритеты у Goal/Decision/Task/Action — свойство или следствие?
- [ ] UI структуры: список / граф / канбан / доска?
- [ ] Миграция Task из Этапа 1 — мигрировать или начать с чистого листа?
- [ ] Делегирование агентам — как настраивается?
- [ ] Видимость работы агентов — лог / уведомления / дашборд?
- [ ] Сколько агентов в MVP — один / два / все пять?
- [ ] Как система видит нехватку ИД — ГИП сам или агент подсказывает?
- [ ] Методы управления — явно или производно?
- [ ] Механизм вывода. Как система выводит структуру из вводных? Правила? Шаблоны? LLM? Гибрид?
- [ ] Утверждение. Как ГИП утверждает предложенное? По одному? Списком? С правками? Что с отклонённым?
- [ ] Границы автоматизации. Что система предлагает всегда, что — только по запросу, что — никогда?

**Блокеры — не изменились:**

- [ ] GitHub Actions для авто-генерации DATABASE.md / API.md — не настроены.
- [ ] B027 (TaskRepository.get_by_pair) — техдолг Этапа 1.
- [ ] GigaCode запускает pytest не из корня.
- [ ] GigaCode запускает python -c без активации .venv.
- [ ] GigaCode делает отдельный коммит вместо --amend.
- [ ] GigaCode коммитит в main без feature-ветки.
- [ ] ESLint в frontend не настроен (только tsc).

---

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
- **Текущий HEAD:** `9a94cda` (feat/week-1d-di-routes)
- **Ветка в паузе:** `feat/entity-type-templates-domain` (не мержить, не удалять)

---

## 7. Как продолжить в новом чате

**Первое сообщение в новом чате с DeepSeek (или другим ИИ):**

    Привет. Продолжаем проект «ГИП-Ассистент».

    Прочитай (по порядку):
    1. docs/context/DOMAIN.md — онтология (v1.1).
    2. docs/context/HANDOFF.md — эстафета (сессия 6.3).
    3. docs/context/CONTEXT.md — резюме (v2.2).
    4. docs/context/TASKS.md — статус (v2.2).
    5. docs/specs/spec_week_1.md — спека вехи 1.
    6. AGENTS.md — правила (v1.2).

    Веха 1a–1d закрыта, 187 тестов зелёных. Идём в веху 1f — UI.

---

**Конец HANDOFF.md.**
