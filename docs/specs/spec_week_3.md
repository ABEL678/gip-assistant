# spec_week_3.md — Веха 3: Система предлагает решения и связи

## §1. Что делаем

Веха 3 «Система предлагает решения и связи».

ГИП видит решения с обоснованиями, связи Goal ↔ Decision ↔ Task.
Norm как внешний норматив. Система предлагает Decision на основе
Goal и вводных. ГИП утверждает.

Ценность: ГИП видит не только «что сделать» (Goal), но и «как сделать»
(Decision) с обоснованием из вводных и ссылкой на нормы.

## §2. Сущности

### 2.1. Decision (Решение)

Таблица полей:

| Поле | Тип | Обяз. | Комментарий |
|---|---|---|---|
| id | UUID | да | PK |
| project_id | UUID | да | FK → projects |
| formulation | str | да | Формулировка (≤ 500) |
| rationale | text | нет | Обоснование |
| context | text | нет | Контекст |
| deadline | date | нет | Срок |
| state | Enum | да | plan / in_progress / accepted / cancelled / replaced |
| created_by | UUID | нет | FK → users |
| created_at | timestamp | да | |
| updated_at | timestamp | да | |

**Связи Decision:**

- `Decision ↔ Goal` (M:N) — через `decision_goals`. Одно решение ведёт к нескольким целям (`DOMAIN.md §4.2`).
- `Decision ↔ Premise` (M:N) — через `decision_premises`. Обоснование опирается на вводные.
- `Decision → Task` (1:N) — через FK `tasks.decision_id` (nullable). **Не** ассоциативная таблица.
- `Decision ↔ Norm` (M:N) — через `decision_norms` (в 6.11b, вместе с Norm).
- `Decision ↔ Decision` (M:N) — через `decision_links` (в 6.11b). Тип связи: `sequential` / `parallel` / `nested`.

**`verification_status` — не добавляем.** В `DOMAIN.md §4.4.1` сказано: только Action и Goal. Decision — нет.

### 2.2. Norm (Нормативный документ)

Таблица полей:

| Поле | Тип | Обяз. | Комментарий |
|---|---|---|---|
| id | UUID | да | PK |
| project_id | UUID | да | FK → projects |
| code | str | да | Обозначение (уникально в проекте) |
| title | str | да | Название |
| norm_type | Enum | да | gost / snip / npa / xml_schema / other |
| issued_at | date | нет | Дата введения / редакция |
| source_url | str | нет | Источник (ссылка) |
| document_id | UUID | нет | FK → documents (если есть файл) |
| created_at | timestamp | да | |
| updated_at | timestamp | да | |

**Связи Norm:**

- `Norm ↔ Decision` (M:N) — через `decision_norms` (в 6.11b).
- `Norm ↔ Document` (1:1) — через `document_id` (nullable FK, в 6.11b).

**Норма — вводная, но отдельная сущность.** `DOMAIN.md §7.2`: «частный случай вводных, но достаточно важный, чтобы быть отдельной сущностью». В `Premise` Norm не дублируем.

### 2.3. DecisionLink (Связь решений)

Таблица полей:

| Поле | Тип | Обяз. | Комментарий |
|---|---|---|---|
| id | UUID | да | PK |
| project_id | UUID | да | FK → projects |
| from_decision_id | UUID | да | FK → decisions |
| to_decision_id | UUID | да | FK → decisions |
| link_type | Enum | да | sequential / parallel / nested |
| created_at | timestamp | да | |

**Ограничения:**

- `from_decision_id != to_decision_id` — self-link запрещён.
- Уникальность `(from_decision_id, to_decision_id, link_type)` — одна связь одного типа между парой решений.
- Оба решения — из одного проекта (`project_id`).

**Почему отдельная сущность, а не `parent_id`:** `DOMAIN.md §11, вопрос 4` — решается здесь. Отдельная сущность даёт M:N с типом связи (последовательная / параллельная / вложенная), как у `DocumentLink` в 1.5. `parent_id` — только дерево, не покрывает параллельные и последовательные.

### 2.4. Ассоциативные таблицы

`decision_goals`:
- `decision_id` — FK → decisions (CASCADE)
- `goal_id` — FK → goals (CASCADE)
- `created_at`
- PK составной (decision_id, goal_id).

`decision_premises`:
- `decision_id` — FK → decisions (CASCADE)
- `premise_id` — FK → premises (CASCADE)
- `created_at`
- PK составной (decision_id, premise_id).

`decision_norms` — **в 6.11b** (после Norm).

`decision_links` — **в 6.11b** (вместе с Norm, чтобы не раздувать 6.11a).

## §3. Модель БД

SQLAlchemy-модели в `backend/src/adapters/db/models/`:
- `decision.py` — `DecisionModel`.
- `decision_goal.py` — `DecisionGoalModel` (ассоциативная).
- `decision_premise.py` — `DecisionPremiseModel` (ассоциативная).
- `norm.py` — **в 6.11b**.
- `decision_link.py` — **в 6.11b**.

Миграция Alembic (6.11a) — одна, создаёт:
- `decisions` — 3 индекса: `idx_decisions_project`, `idx_decisions_state`, `idx_decisions_deadline`.
- `decision_goals` — PK + 2 индекса: `idx_decision_goals_decision`, `idx_decision_goals_goal`.
- `decision_premises` — PK + 2 индекса: `idx_decision_premises_decision`, `idx_decision_premises_premise`.
- Колонка `tasks.decision_id` (nullable FK) + индекс `idx_tasks_decision`.

Enum-значения — в `backend/src/domain/value_objects/enums.py`.

Типы:
- `DecisionState` — 5 значений: plan / in_progress / accepted / cancelled / replaced.
- `DecisionLinkType` — 3 значения: sequential / parallel / nested (**в 6.11b**).

**Enum в SQLAlchemy:** `Enum(DecisionState, name="decision_state", create_type=False)` — по правилу AGENTS.md. Миграция создаёт тип, модель использует `create_type=False`.

### 3.1. FK ondelete

- `decisions.project_id` — CASCADE.
- `decisions.created_by` — SET NULL.
- `decision_goals.*` — CASCADE (при удалении decision или goal).
- `decision_premises.*` — CASCADE.
- `tasks.decision_id` — SET NULL (если decision удалён, task остаётся без decision).

## §4. DTO

Pydantic-схемы в `backend/src/application/dto/`:

`decision.py`:
- `DecisionSchema(BaseModel)` — formulation (min_length=1, max_length=500), rationale, context, deadline, state (default PLAN), premise_ids, goal_ids.
- `DecisionCreate(DecisionSchema)` — project_id передаётся в пути.
- `DecisionUpdate(BaseModel)` — все поля optional.
- `DecisionRead(DecisionSchema)` — id, project_id, created_by, created_at, updated_at. `model_config = ConfigDict(from_attributes=True)`.

`norm.py` — **в 6.11b**.

`decision_link.py` — **в 6.11b**.

**`DecisionRead`:** `premise_ids` и `goal_ids` — реальные списки из БД, не пустые. Это та же ошибка, что была с Goal (canvas edge bug, 6.7): если `_to_domain` не вызовет `_fetch_premise_ids` и `_fetch_goal_ids` — списки будут пустыми. В спеке это требование явное.

## §5. Порты и репозитории

Порты в `backend/src/domain/ports/repositories.py`:
- `DecisionRepository` (ABC) — 6.11a.
- `NormRepository` (ABC) — 6.11b.
- `DecisionLinkRepository` (ABC) — 6.11b.

Репозитории в `backend/src/adapters/db/repositories/`:
- `decision_repository.py` — `SqlAlchemyDecisionRepository` (6.11a).
- `norm_repository.py` — 6.11b.
- `decision_link_repository.py` — 6.11b.

**Метод `save` Decision** (6.11a):
- `_to_model` — только скалярные поля.
- `session.merge` + flush + refresh — скалярные поля.
- Синхронизация `decision_goals` и `decision_premises` — DELETE + INSERT по `decision_id` (не через relationship).
- `_to_domain` **обязан** вызвать `_fetch_premise_ids` и `_fetch_goal_ids`.
- `save` перечитывает decision через `get_by_id` (не возвращает из merge).

Это тот же паттерн, что чинили в `goal_repository.py` (canvas edge bug, 6.7). Без него `premise_ids` / `goal_ids` вернутся пустыми.

**`get_by_id` / `list_by_project`** — оба вызывают `_to_domain` (с `_fetch_*_ids`).

**`delete`** — DELETE FROM decisions WHERE id = :id (CASCADE чистит ассоциативные).

## §6. Сервисы

Сервисы в `backend/src/domain/services/`:

`decision_service.py` — `DecisionService`:
- CRUD Decision.
- Валидации: formulation не пустой; project_id существует; premise_ids / goal_ids — из того же проекта; state — валидный.
- Связи с Premise и Goal — через репозиторий.

`norm_service.py` — `NormService` (6.11b).

`decision_link_service.py` — `DecisionLinkService` (6.11b).

**Правила вывода Decision в DecisionProposalService** (2 правила, 6.11a):

Правило 1 — Goal без Decision → предложить Decision «Определить способ реализации»:
- Если у Goal **нет** связанных Decision (проверка по `decision_goals`).
- → предложить Decision:
  - formulation = «Определить способ реализации цели: {goal.formulation}»
  - goal_ids = [goal.id]
  - state = PLAN
  - rule = «goal_без_решения»

Правило 2 — Goal с дедлайном и без обоснования → предложить Decision с обоснованием из вводных:
- Если у Goal есть `deadline` и есть `premise_ids`.
- → предложить Decision:
  - formulation = «Обосновать срок: {goal.formulation}»
  - rationale = «Срок {goal.deadline} из вводных»
  - premise_ids = goal.premise_ids
  - goal_ids = [goal.id]
  - rule = «срок_из_вводных»

Метод `propose_decisions(project_id) -> list[DecisionProposal]`. Не сохраняет в БД. Возвращает эфемерный список.

**Почему только 2 правила:** Decision — тактический уровень («как сделать»). Больше вариативности, чем у Goal. В вехах 1–5 система осторожна (`DOMAIN.md §2`: «только явное из вводных»). LLM (веха 6) добавит сюда больше.

## §7. DI и эндпоинты

DI в `backend/src/adapters/api/dependencies.py`:
- `get_decision_service` → `DecisionServiceDep`.
- `get_norm_service` → `NormServiceDep` (6.11b).
- `get_decision_link_service` → `DecisionLinkServiceDep` (6.11b).
- `get_decision_proposal_service` → `DecisionProposalServiceDep`.

Роуты в `backend/src/adapters/api/routes/`:

`decisions.py` (6.11a):
- GET /api/projects/{project_id}/decisions
- POST /api/projects/{project_id}/decisions
- GET /api/decisions/{id}
- PATCH /api/decisions/{id}
- DELETE /api/decisions/{id}
- GET /api/projects/{project_id}/decisions/proposals — предложения
- POST /api/projects/{project_id}/decisions/from-proposal — утвердить предложение

`norms.py` — 6.11b.
`decision_links.py` — 6.11b.

Регистрация в `main.py` + `routes/__init__.py`.

**Граница:** эндпоинты proposals/from-proposal не заменяют CRUD. Они дополняют.

## §8. Тесты

Unit-тесты в `backend/tests/`:

6.11a:
- `test_decision_service.py` — CRUD Decision, валидации, связи с Premise и Goal.
- `test_decision_proposal_service.py` — 2 правила (по 2–3 теста на правило).
- `test_decision_mapping.py` — smoke: domain ↔ model, M:N (premise_ids, goal_ids), каскад.

6.11b:
- `test_norm_service.py`.
- `test_decision_link_service.py`.
- `test_norm_mapping.py`.
- `test_decision_link_mapping.py`.

Цель по вехе 3: +35–45 тестов. Итого в проекте: ~325–335.

**Особый тест (6.11a):** `test_decision_premise_goal_ids_persist_end_to_end` — decision с 2 premise_ids и 2 goal_ids → save → get_by_id → оба списка непустые. Это защита от canvas edge bug.

## §9. UI

API-клиенты в `frontend/src/api/`:
- `decisionApi.ts` (6.11a).
- `normApi.ts` (6.11b).
- `decisionLinkApi.ts` (6.11b).

Хуки в `frontend/src/hooks/`:
- `useDecisions.ts` (6.11a).
- `useNorms.ts` (6.11b).
- `useDecisionLinks.ts` (6.11b).

Страницы в `frontend/src/pages/`:
- `DecisionsPage.tsx` — список решений + блок «Предложенные решения».
- `NormsPage.tsx` (6.11b).
- `DecisionLinkPage.tsx` (6.11b).

Компоненты в `frontend/src/components/`:
- `DecisionCard.tsx` — карточка с бейджем состояния (plan / in_progress / accepted / cancelled / replaced), связями Goal и Premise.
- `DecisionForm.tsx`.
- `DecisionProposalList.tsx` — список предложений с утверждением.
- `NormCard.tsx` (6.11b).
- `DecisionLinkCard.tsx` (6.11b).

Роутинг в `App.tsx`.

**UI структуры — список для MVP** (как и в вехе 1). Карточки со статусом и связями.

### 9.1. UI Norm и DecisionLink (6.11b)

- `NormPage.tsx` — список норм, форма.
- `DecisionLinkPage.tsx` — список связей с типом (sequential / parallel / nested).
- `NormCard.tsx` — карточка нормы (код, название, тип, источник).
- `DecisionLinkCard.tsx` — карточка связи (from → to, тип).

## §10. Открытые вопросы вехи

- **Вопрос 4 (DOMAIN.md §11):** Decision ↔ Decision — **решено**: отдельная сущность `DecisionLink` с полем `link_type` (enum: sequential / parallel / nested). Аналог `DocumentLink` из 1.5. Не `parent_id`.
- **Вопрос 12 (DOMAIN.md §11):** Методы управления — **решено**: производная от структуры. Не сущность. Не отображается в UI как отдельная карточка. ГИП видит методы через связи Goal ↔ Decision ↔ Task и через обоснования Decision.
- **Вопрос 3 (DOMAIN.md §11):** Action ↔ Document — **не решается в вехе 3**. Решается в вехе 4 (RFI → Document → новые ИД).

### 10.1. Проверка характеристик (для вехи 3)

**Нативность:**
- ГИП создаёт Decision из предложения → ≤ 3 кликов.
- ГИП связывает Decision с Goal → ≤ 3 кликов.
- Нет обучающих экранов.

**Юзабилити:**
- Ошибок при создании Decision — ≤ 1 на 10 (тест на 5 ГИПах).
- SUS ≥ 80 (после пилота).

**Ценность:**
- Время на создание Decision с обоснованием — ≤ 3 минут (было 10 в Excel).
- Время на просмотр всех связей Goal ↔ Decision ↔ Task — ≤ 2 минут.

**Доверие:**
- Доля Decision с обоснованием из вводных — 100% (если предложено системой).
- Ложных срабатываний DecisionProposalService — ≤ 10% (тест на 10 целях).

## §11. Демо

ГИП создаёт Goal «Сдать том 7 в экспертизу» → нажимает «Предложить
решения» → система предлагает Decision «Определить способ реализации
цели: Сдать том 7 в экспертизу» с обоснованием из договора → ГИП
утверждает → Decision появляется в списке, связь Goal → Decision
видна. ГИП создаёт Task → связывает с Decision → видит связь
Goal → Decision → Task.

## §12. Что НЕ входит

- RFI (веха 4).
- Document ↔ Action (веха 4).
- Агент сроков (веха 5).
- LLM (веха 6).
- UI дашборда, отчётов, скелета, экспорта, поиска (очередь после вехи 3, `TASKS.md`).
- Автоматическое создание Decision без утверждения.