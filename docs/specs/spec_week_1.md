# spec_week_1.md — Веха 1: Система знает вводные и предлагает цели

## §1. Что делаем

Веха 1 «Система знает вводные и предлагает цели».

ГИП заводит вводные (договор, ТЗ, требования Заказчика, ИД, нормы,
НПА, гос. бюрократия, внутренние ресурсы) как сущности. Система
предлагает Goal на основе вводных (правила 1–4). ГИП утверждает,
правит, отклоняет.

Ценность: ГИП видит вводные как сущности и получает предложенные
цели — не формулирует с нуля.

## §2. Сущности

**Premise (Вводная).**

Вариант C: обёртка + JSONB + схема по категориям.

Таблица полей:

| Поле | Тип | Обяз. | Комментарий |
|---|---|---|---|
| id | UUID | да | PK |
| project_id | UUID | да | FK → projects |
| category | Enum | да | contract / tz / customer_requirement / source_data / norm / npa / bureaucracy / internal |
| name | str | да | Краткое название |
| source | str | нет | Откуда пришла |
| date | date | нет | Когда вступила в силу |
| actual | bool | да | Актуальна (default true) |
| mandatory | bool | да | Обязательна (default true) |
| link | str | нет | Ссылка на документ-источник |
| valid_until | date | нет | Срок действия (для ИД) |
| data | JSONB | нет | Типизированные поля по категории |
| schema | JSONB | нет | Схема полей для категории |
| created_at | timestamp | да | |
| updated_at | timestamp | да | |

**Goal (Цель).**

| Поле | Тип | Обяз. | Комментарий |
|---|---|---|---|
| id | UUID | да | PK |
| project_id | UUID | да | FK → projects |
| formulation | str | да | Формулировка |
| deadline | date | нет | Срок |
| responsible_id | UUID | нет | FK → users |
| priority | int | нет | 1–5 |
| state | Enum | да | plan / in_progress / achieved / cancelled |
| created_by | UUID | нет | FK → users |
| created_at | timestamp | да | |
| updated_at | timestamp | да | |

**Связь Goal ↔ Premise (M:N).**

Таблица `goal_premises`:

| Поле | Тип | Комментарий |
|---|---|---|
| goal_id | UUID | FK → goals |
| premise_id | UUID | FK → premises |
| created_at | timestamp | |

Первичный ключ — составной (goal_id, premise_id).

## §3. Модель БД

SQLAlchemy-модели в `backend/src/adapters/db/models/`:
- `premise.py` — `PremiseModel`.
- `goal.py` — `GoalModel`.
- `goal_premise.py` — `GoalPremiseModel` (ассоциативная).

Миграция Alembic — одна, создаёт 3 таблицы + индексы:
- `idx_premises_project` — на `project_id`.
- `idx_premises_category` — на `category`.
- `idx_premises_actual` — на `actual`.
- `idx_goals_project` — на `project_id`.
- `idx_goals_state` — на `state`.
- `idx_goals_deadline` — на `deadline`.

Enum-значения — в `backend/src/domain/value_objects/enums.py`.

Типы:
- `PremiseCategory` — 8 значений.
- `GoalState` — 4 значения.

## §4. DTO

Pydantic-схемы в `backend/src/application/dto/`:
- `premise.py`: `PremiseSchema`, `PremiseCreate`, `PremiseRead`, `PremiseUpdate`.
- `goal.py`: `GoalSchema`, `GoalCreate`, `GoalRead`, `GoalUpdate`, `GoalProposal`.

`GoalProposal` — эфемерная схема для предложения:
- `formulation` — str.
- `deadline` — date | None.
- `priority` — int | None.
- `premise_ids` — list[UUID] (какие вводные стали источником).
- `rule` — str (какое правило сработало: «договор_срок», «тз_требование», «требование_заказчика», «просроченный_ид»).

## §5. Порты и репозитории

Порты в `backend/src/domain/ports/repositories.py`:
- `PremiseRepository` (ABC).
- `GoalRepository` (ABC).

Репозитории в `backend/src/adapters/db/repositories/`:
- `premise_repository.py` — `SqlAlchemyPremiseRepository`.
- `goal_repository.py` — `SqlAlchemyGoalRepository`.

Метод `save` — через `session.merge()`. Mapping — `_to_domain` / `_to_model`.

## §6. Сервисы

Сервисы в `backend/src/domain/services/`:
- `premise_service.py` — `PremiseService`: CRUD, валидация по схеме категории.
- `goal_service.py` — `GoalService`: CRUD, связи с Premise.
- `goal_proposal_service.py` — `GoalProposalService`: механизм вывода на правилах.

**4 правила вывода в GoalProposalService:**

Правило 1 — договор со сроком → Goal:
- Если premise.category == contract
- И premise.data.get(«deadline») не пусто
- → предложить Goal:
  - formulation = «Сдать {premise.name} к {premise.data['deadline']}»
  - deadline = premise.data['deadline']
  - premise_ids = [premise.id]
  - rule = «договор_срок»

Правило 2 — ТЗ с требованием → Goal:
- Если premise.category == tz
- И premise.data.get(«requirement») не пусто
- → предложить Goal:
  - formulation = premise.data['requirement']
  - premise_ids = [premise.id]
  - rule = «тз_требование»

Правило 3 — требование Заказчика → Goal:
- Если premise.category == customer_requirement
- И premise.data.get(«content») не пусто
- → предложить Goal:
  - formulation = premise.data['content']
  - premise_ids = [premise.id]
  - rule = «требование_заказчика»

Правило 4 — просроченный ИД → Goal «Обновить ИД»:
- Если premise.category == source_data
- И premise.valid_until < today
- → предложить Goal:
  - formulation = «Обновить {premise.name}»
  - deadline = premise.valid_until + 30 days
  - premise_ids = [premise.id]
  - rule = «просроченный_ид»

Метод `propose_goals(project_id) -> list[GoalProposal]`.
Не сохраняет в БД. Возвращает эфемерный список.

## §7. DI и эндпоинты

DI в `backend/src/adapters/api/dependencies.py`:
- `get_premise_service` → `PremiseServiceDep`.
- `get_goal_service` → `GoalServiceDep`.
- `get_goal_proposal_service` → `GoalProposalServiceDep`.

Роуты в `backend/src/adapters/api/routes/`:

`premises.py` — CRUD для Premise:
- GET /api/projects/{project_id}/premises
- POST /api/projects/{project_id}/premises
- GET /api/premises/{id}
- PATCH /api/premises/{id}
- DELETE /api/premises/{id}

`goals.py` — CRUD для Goal + предложения:
- GET /api/projects/{project_id}/goals
- POST /api/projects/{project_id}/goals
- GET /api/goals/{id}
- PATCH /api/goals/{id}
- DELETE /api/goals/{id}
- GET /api/projects/{project_id}/goals/proposals — предложения
- POST /api/projects/{project_id}/goals/from-proposal — утвердить предложение

Регистрация в `main.py` + `routes/__init__.py`.

## §8. Тесты

Unit-тесты в `backend/tests/`:
- `test_premise_service.py` — CRUD Premise, валидация по схеме.
- `test_goal_service.py` — CRUD Goal, связи с Premise.
- `test_goal_proposal_service.py` — 4 правила (по 2–3 теста на правило).

Smoke-тесты маппинга:
- `test_premise_mapping.py`.
- `test_goal_mapping.py`.

Цель: +25–30 тестов. Итого в проекте — ~150.

## §9. UI

API-клиенты в `frontend/src/api/`:
- `premiseApi.ts`.
- `goalApi.ts`.

Хуки в `frontend/src/hooks/`:
- `usePremises.ts`.
- `useGoals.ts`.

Страницы в `frontend/src/pages/`:
- `PremisesPage.tsx` — список вводных, форма создания/редактирования.
- `GoalsPage.tsx` — список целей + блок «Предложенные цели» с кнопками утвердить / отклонить / править.

Компоненты в `frontend/src/components/`:
- `PremiseCard.tsx`.
- `PremiseForm.tsx`.
- `GoalCard.tsx`.
- `GoalForm.tsx`.
- `GoalProposalList.tsx` — список предложений с утверждением.

Роутинг в `App.tsx`.

UI структуры — список для MVP (ответ на вопрос 6).

## §10. Открытые вопросы вехи

- Вопрос 6: UI структуры — список для MVP (решено).
- Вопрос 13: механизм вывода — правила 1–4 (решено в спеке).
- Вопрос 14: утверждение — по одному + список + правки (решено).
- Вопрос 15: границы автоматизации — только явное из вводных (решено).

## §11. Демо

ГИП заводит договор «Сдать том 7 к декабрю 2026» → нажимает
«Предложить цели» → система предлагает Goal «Сдать том 7 к декабрю
2026» → ГИП утверждает → Goal появляется в списке, связь с Premise
видна.

## §12. Что НЕ входит

- Decision, Task, Action (веха 2–3).
- RFI (веха 4).
- Агент сроков (веха 5).
- LLM (веха 6).
- Автоматическое создание Goal без утверждения.
