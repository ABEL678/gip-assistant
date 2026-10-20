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

**`Premise.data` — каждое поле имеет `owner`** (проектная позиция / результат подбора / паспорт изделия). Если `owner` не указан — это «нет данных» (нельзя проверить). См. DOMAIN.md §3.4.1.

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
| verification_status | Enum | да | confirmed / not_confirmed / requires_check (default) / no_data. DOMAIN.md §4.4.1. |
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

### 2.1. Верификация Goal — как работает

`verification_status` **не** просто поле. Это **результат** работы агента-валидатора (см. §6.1).

**Когда выставляется:**
- **`requires_check`** — по умолчанию. Goal создан вручную или предложен системой, но **не проверен**.
- **`confirmed`** — валидатор нашёл **два места** в вводных (источник и следствие), и **источник** у каждой цифры. Например: договор (срок) + ТЗ (требование) → Goal «Сдать том 7 к декабрю 2026».
- **`not_confirmed`** — валидатор нашёл **противоречие** (например, Goal противоречит договору).
- **`no_data`** — валидатор **не нашёл** данных. Это **не ошибка**. Это **сигнал** к RFI (запрос).

**Кто выставляет:**
- **Агент-валидатор** (см. §6.1) — при вызове `POST /goals/{id}/validate`.
- **ГИП** — вручную (если не согласен с валидатором).

**Как влияет на утверждение:**
- `confirmed` — ГИП **может** утвердить.
- `requires_check` — ГИП **должен** проверить вручную.
- `no_data` — ГИП **должен** создать RFI (запрос), а **не** утверждать.
- `not_confirmed` — ГИП **должен** отклонить или исправить Goal.

### 2.2. Новые сущности (ревизии)

**Revision (Ревизия)** — новая версия документа. Поля:
- `id` — UUID.
- `document_id` — FK → documents (какой документ ревизуется).
- `version` — номер (1, 2, 3...).
- `date` — когда получена.
- `source` — кто прислал (смежник, заказчик).
- `notified` — уведомил ли смежник об изменении (bool).
- `stop_flag` — есть ли стоп-сигнал (bool).

**Change (Изменение)** — что изменилось между ревизиями. Поля:
- `id` — UUID.
- `revision_id` — FK → revisions.
- `field` — какое поле (например, «отверстие D250»).
- `old_value` — было.
- `new_value` — стало.
- `status` — `added` / `removed` / `changed` / `unchanged`.

**RevisionDecision (Решение по ревизии)** — что ГИП решил по каждому изменению. Поля:
- `id` — UUID.
- `change_id` — FK → changes.
- `decision` — `accepted` / `accepted_with_frame` / `remark` / `rejected` / `moved` / `deadline`.
- `decided_by` — кто принял (ГИП).
- `deadline` — срок ответа смежнику (если `moved` или `remark`).

**StopFlag (Стоп-сигнал)** — признак, что надо остановиться и выяснить. Поля:
- `id` — UUID.
- `revision_id` — FK → revisions.
- `reason` — один из 6 признаков (см. §4.4.3).
- `resolved` — bool (выяснили или нет).

**Правило:** если у `Revision` `notified = false` — это `changed_silently` (см. §4.4.1). ГИП должен увидеть это до сравнения.

### 2.3. Result (Результат)

**Поля:**
- `id` — UUID.
- `project_id` — FK → projects.
- `formulation` — str (потребительская** **ценность** **для** **Заказчика**).
- `source` — str (предмет** **договора**/**приложение**).
- `approved_by` — UUID (Заказчик).
- `created_at` — timestamp.
- `updated_at` — timestamp.

**Связь** `Result` ↔ `Goal` (M:N). **Таблица** `result_goals`: `result_id`, `goal_id`, `created_at`.

**Правило:** `Result` **не** **порождает** `Goal`. **Он** **задаёт** **направление**.

### 2.4. ProjectStandard (стандарт проекта)

**Поля:**
- `id` — UUID.
- `premise_id` — FK → premises.
- `type` — `deadline` / `composition` / `format`.
- `value` — JSONB (дата, **список**, **формат**).
- `approved_by` — UUID (Заказчик).
- `created_at` — timestamp.
- `updated_at` — timestamp.

**Связь** `ProjectStandard` ↔ `Goal` (M:N). **Таблица** `standard_goals`: `standard_id`, `goal_id`, `created_at`.

**Правило:** `ProjectStandard` **не** **порождает** `Goal`. **Он** **ограничивает** **их**.

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

### 3.1. Модель БД — как хранится verification_status и owner

**`verification_status` в GoalModel:**

- Колонка: `verification_status` типа `Enum(VerificationStatus, name="verification_status", create_type=False)`.
- Значения: `confirmed`, `not_confirmed`, `requires_check`, `no_data`.
- Default: `requires_check`.
- Индекс: `idx_goals_verification_status`.
- Миграция Alembic: **создаёт** enum-тип + колонку + индекс.

**`owner` в Premise.data:**

- `Premise.data` — JSONB. **Каждое поле** хранится как объект `{value, owner, source}`.
- Пример: `{"deadline": {"value": "2026-12-01", "owner": "contract", "source": "Договор №1"}}`.
- Если `owner` **не указан** — это «нет данных» (нельзя проверить).
- **Схема** (`Premise.schema`) задаёт **какие** поля есть и **какой** у них `owner` по умолчанию.

**Пример схемы для категории `contract`:**

```json
{
  "deadline": {"type": "date", "owner": "contract", "required": true},
  "amount": {"type": "number", "owner": "contract", "required": false}
}
```

**Правило:** при создании/обновлении Premise.data каждое поле должно иметь owner (из схемы или явно). Если owner нет — валидатор выставит no_data.

### 3.2. Модель БД (ревизии)

**Таблицы:**
- `revisions` — с FK на `documents.id`, индексы: `idx_revisions_document`, `idx_revisions_date`.
- `changes` — с FK на `revisions.id`, индексы: `idx_changes_revision`, `idx_changes_status`.
- `revision_decisions` — с FK на `changes.id`, индексы: `idx_revision_decisions_change`.
- `stop_flags` — с FK на `revisions.id`, индексы: `idx_stop_flags_revision`, `idx_stop_flags_resolved`.

**Миграция Alembic:** создаёт 4 таблицы + FK + индексы. **Не** трогает `documents` (он уже есть).

**Enum'ы:**
- `ChangeStatus` — `added`, `removed`, `changed`, `unchanged`.
- `RevisionDecisionType` — `accepted`, `accepted_with_frame`, `remark`, `rejected`, `moved`, `deadline`.

**Правило:** `revision_id` в `changes` и `stop_flags` — **CASCADE** (при удалении ревизии — удаляются изменения и стоп-флаги).

## §4. DTO

Pydantic-схемы в `backend/src/application/dto/`:
- `premise.py`: `PremiseSchema`, `PremiseCreate`, `PremiseRead`, `PremiseUpdate`.
- `goal.py`: `GoalSchema`, `GoalCreate`, `GoalRead`, `GoalUpdate`, `GoalProposal`.
- `verification_status.py`: `VerificationStatus` (enum: confirmed / not_confirmed / requires_check / no_data). DOMAIN.md §4.4.1.
- `premise_data_field.py`: `PremiseDataField` — `{value, owner, source}`. Если `owner` не указан — «нет данных».

`GoalProposal` — эфемерная схема для предложения:
- `formulation` — str.
- `deadline` — date | None.
- `priority` — int | None.
- `premise_ids` — list[UUID] (какие вводные стали источником).
- `rule` — str (какое правило сработало: «договор_срок», «тз_требование», «требование_заказчика», «просроченный_ид»).

### 4.1. DTO — как сериализуется PremiseDataField

**`PremiseDataField`:**

```python
class PremiseDataField(BaseModel):
    value: Any
    owner: str | None = None
    source: str | None = None
```

**Пример использования в `PremiseRead`:**

```json
{
  "id": "...",
  "category": "contract",
  "name": "Договор №1",
  "data": {
    "deadline": {"value": "2026-12-01", "owner": "contract", "source": "Договор №1"},
    "amount": {"value": 1500000, "owner": "contract", "source": "Договор №1"}
  }
}
```

**Граница:** если `owner = None` — это «нет данных». Валидатор не сможет проверить Goal, который ссылается на это поле.

### 4.2. DTO (ревизии)

**DTO-файлы:**
- `revision.py`: `RevisionSchema`, `RevisionCreate`, `RevisionRead`, `RevisionUpdate`.
- `change.py`: `ChangeSchema`, `ChangeCreate`, `ChangeRead`.
- `revision_decision.py`: `RevisionDecisionSchema`, `RevisionDecisionCreate`, `RevisionDecisionRead`.
- `stop_flag.py`: `StopFlagSchema`, `StopFlagCreate`, `StopFlagRead`.

**Enum'ы в DTO:**
- `ChangeStatus` (4 значения).
- `RevisionDecisionType` (6 значений).

## §5. Порты и репозитории

Порты в `backend/src/domain/ports/repositories.py`:
- `PremiseRepository` (ABC).
- `GoalRepository` (ABC).

Репозитории в `backend/src/adapters/db/repositories/`:
- `premise_repository.py` — `SqlAlchemyPremiseRepository`.
- `goal_repository.py` — `SqlAlchemyGoalRepository`.

Метод `save` — через `session.merge()`. Mapping — `_to_domain` / `_to_model`.

### 5.1. Порты и репозитории (ревизии)

**Порты:**
- `RevisionRepository` (ABC).
- `ChangeRepository` (ABC).
- `RevisionDecisionRepository` (ABC).
- `StopFlagRepository` (ABC).

**Репозитории:**
- `revision_repository.py` — `SqlAlchemyRevisionRepository`.
- `change_repository.py` — `SqlAlchemyChangeRepository`.
- `revision_decision_repository.py` — `SqlAlchemyRevisionDecisionRepository`.
- `stop_flag_repository.py` — `SqlAlchemyStopFlagRepository`.

**Метод `save`** — через `session.merge()`. Mapping — `_to_domain` / `_to_model`.

## §6. Сервисы

Сервисы в `backend/src/domain/services/`:
- `premise_service.py` — `PremiseService`: CRUD, валидация по схеме категории.
- `goal_service.py` — `GoalService`: CRUD, связи с Premise.
- `goal_proposal_service.py` — `GoalProposalService`: механизм вывода на правилах.

**Абстракция GoalValidatorService:**

- **Порт (ABC):** `backend/src/domain/ports/goal_validator.py` — `GoalValidatorService` (интерфейс).
- **Веха 1–5:** `backend/src/domain/services/rule_based_goal_validator.py` — `RuleBasedGoalValidator(GoalValidatorService)`: детерминированные правила 1–6.
- **Веха 6:** `LLMGoalValidator(GoalValidatorService)` — недетерминированный, на LLM.
- **Зависимость:** сервисы зависят от порта (ABC), а не от конкретной реализации.

**4 правила вывода в GoalProposalService:**

Правило 1 — договор со сроком → Goal:
- Если premise.category == contract
- И premise.data.get(«deadline») не пусто
- → предложить Goal:
  - formulation = «Сдать {premise.name} к {premise.data['deadline']}»
  - deadline = premise.data['deadline']
  - premise_ids = [premise.id]
  - rule = «договор_срок»

Правило 2 (переделано) — ТЗ → ProjectStandard:
- Если premise.category == tz и premise.data.get(«requirement») не пусто →
- предложить ProjectStandard: type = "composition", value = premise.data['requirement'].
- Не предлагать Goal. ТЗ — не цель, а стандарт.

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

### 6.1. Агент-валидатор (часть Вехи 1)

Проверяет предложения (от смежников, от системы) на **доказанность**:
- Есть ли **два места** в документе (источник и следствие)?
- Есть ли **источник** у каждой цифры?
- Если данных нет — **предложить RFI** (запрос), а не «решение».

Работает на правилах (веха 1–5), без LLM.

См. Дорожная карта §5.1.8.

#### 6.1.1. Агент-валидатор — алгоритм

**Вход:** Goal (формулировка, deadline, premise_ids) + список Premise (с `data` и `owner`).

**Шаги:**

1. **Проверить, что Goal ссылается на Premise.** Если `premise_ids` пуст — `no_data`.
2. **Для каждой Premise:**
   - Если `owner` у поля **не указан** — `no_data`.
   - Если `owner` указан, но **значение** пустое — `no_data`.
3. **Проверить два места.** Для Goal **должны** быть **два места** в вводных:
   - **Источник** (например, договор со сроком).
   - **Следствие** (например, ТЗ с требованием).
   Если **одного** места нет — `requires_check`.
4. **Проверить источник у каждой цифры.** Если в Goal есть число (срок, сумма), оно **должно** быть в `Premise.data` с `owner`. Если нет — `no_data`.
5. **Проверить противоречие.** Если Goal **противоречит** договору (например, срок позже договорного) — `not_confirmed`.
6. **Итог:**
   - Если **все** проверки пройдены — `confirmed`.
   - Если **одна** провалена — `not_confirmed` (если противоречие) или `no_data` (если нет данных).
   - Если **две** и более — `requires_check`.
7. **Проверить** **соответствие** `Goal` → `ProjectStandard`. **Если** **не** **соответствует** — `not_confirmed`.
8. **Проверить** **связь** `Goal` → `Result`. **Если** **нет** — `requires_check`.

#### 6.1.2. Агент-валидатор — выход

`POST /goals/{id}/validate` возвращает:

```json
{
  "goal_id": "...",
  "verification_status": "confirmed",
  "evidence": [
    {"premise_id": "...", "field": "deadline", "value": "2026-12-01", "owner": "contract"},
    {"premise_id": "...", "field": "requirement", "value": "Сдать том 7", "owner": "tz"}
  ],
  "missing": [],
  "contradictions": []
}
```

**Поля:**

- `verification_status` — итоговый статус.
- `evidence` — доказательства (два места + источник у каждой цифры).
- `missing` — чего не хватает (если `no_data`).
- `contradictions` — противоречия (если `not_confirmed`).

**Граница:** если `evidence` пуст — это не `confirmed`. Это `requires_check` (валидатор не нашёл два места).

#### 6.1.3. Три уровня проверки ревизии

- **Уровень 1** (контроль входа) — `RevisionControlService` (6.8b).
- **Уровень 2** (сравнение) — `RevisionDiffService` (6.8b).
- **Уровень 3** (инженерное суждение) — UI + ГИП (6.8d).

#### 6.1.4. Как устроен валидатор (три уровня)

**Валидатор** — **не** **чек-лист** (**список** **галочек**). **Это** **функция**, **которая** **возвращает** **статус** **и** **доказательства**.

**Уровень 1. Детерминированные правила.**
- **См.** **§6.1.1** (шаги 1–8).

**Уровень 2. Протокол 2–3 прогонов.**
- **См.** **§6.3.1**.

**Уровень 3. Инженерное суждение (UI + ГИП).**
- **Валидатор** **показывает** `evidence`, `missing`, `contradictions`.
- **ГИП** **утверждает** **или** **отклоняет**.
- **Это** — **не** **чек-лист**. **Это** **интерфейс**, **где** **ГИП** **видит** **доказательства** **и** **принимает** **решение**.


### 6.2. Матрица смежников (часть Вехи 1)

Правила вывода связей между разделами (10 связей: АР↔ОВ, АР↔КЖ, АР↔ВК, АР↔ЭО, АР↔ПБ, АР↔ПЗУ, ОВ↔КЖ, ОВ↔ЭО, ОВ↔ТХ, ОВ↔ПБ). Если в договоре есть два раздела — предложить связь.

См. Дорожная карта §5.1.9.

#### 6.2.1. Матрица смежников — как работает

**Вход:** `project_id` + список Premise (категория `contract` или `tz`).

**Шаги:**

1. **Найти все разделы** в договоре/ТЗ (например, «АР», «ОВ», «КЖ»).
2. **Для каждой пары разделов** проверить, есть ли связь в матрице:
   - АР ↔ ОВ, АР ↔ КЖ, АР ↔ ВК, АР ↔ ЭО, АР ↔ ПБ, АР ↔ ПЗУ,
     ОВ ↔ КЖ, ОВ ↔ ЭО, ОВ ↔ ТХ, ОВ ↔ ПБ.
3. **Если связь есть** — вернуть её с формулировкой «что согласовать»
   и «сигнал риска».

**Где искать разделы:**
- **(B)** Если `premise.data["sections"]` **есть** (список строк) — брать **только** его.
- **(C)** Если `sections` **нет** — сканировать **все** **строковые** значения `data` на `/^[А-ЯA-Z]{2,6}$/`. **Пропускать** числа, даты, объекты. Если значение — список строк — проверять каждую строку.
- **(A)/(D)** — **не** использовать (`name`, `link` — не список разделов).

**Выход** `GET /goals/similarity-matrix`:

```json
{
  "links": [
    {
      "from": "АР",
      "to": "ОВ",
      "what": "Отверстия и шахты под воздуховоды, венткамеры, дымоудаление",
      "risk": "Пробивка по факту, простой, переделка узла"
    },
    {
      "from": "АР",
      "to": "КЖ",
      "what": "Проёмы в несущих, нагрузки от перегородок, оси и отметки",
      "risk": "Пересчёт узла, усиление"
    }
  ]
}
```

**Граница:** если в договоре нет раздела — связь не предлагается. Если связь есть в матрице, но не в договоре — не предлагается (нет вводной).

### 6.3. Протокол 2–3 прогонов (часть Вехи 1)

Агент-валидатор работает по протоколу: 2–3 прогона, сведение (unanimous = приоритет, majority = в работу, split = на ручную проверку). Итог собирает человек.

См. DOMAIN.md §4.4.2, Дорожная карта §5.1.10.

#### 6.3.1. Протокол 2–3 прогонов — как работает

**Вход:** `project_id` + список предложенных Goal.

**Шаги:**

1. **Для каждого Goal** запустить валидатор **3 раза** (с разными seed / temperature).
2. **Свести** результаты:
   - **unanimous** (3/3 — во всех трёх) — приоритет.
   - **majority** (2/3 — в двух из трёх) — в работу.
   - **split** (1/3 — в одном из трёх) — на ручную проверку.
3. **Вернуть** свод.

**Выход** `POST /goals/proposals/run-3-times`:

```json
{
  "summary": {
    "unanimous": [{"goal_id": "...", "formulation": "Сдать том 7", "verification_status": "confirmed"}],
    "majority": [{"goal_id": "...", "formulation": "Обновить ИД", "verification_status": "requires_check"}],
    "split": [{"goal_id": "...", "formulation": "Согласовать планировку", "verification_status": "no_data"}]
  }
}
```

**Граница:** протокол работает только для валидатора. Для расчётов и графики — не применяется (там нужен инженер).

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

### 7.1. Эндпоинты для валидатора, матрицы, протокола (часть Вехи 1)

Добавить к CRUD:

- `POST /api/goals/{id}/validate` — проверить Goal на доказанность
  (есть ли два места, источник у цифры). Возвращает `verification_status`
  (confirmed / not_confirmed / requires_check / no_data).
- `GET /api/projects/{project_id}/goals/similarity-matrix` — связи между
  разделами по матрице смежников (10 связей: АР↔ОВ, АР↔КЖ, АР↔ВК,
  АР↔ЭО, АР↔ПБ, АР↔ПЗУ, ОВ↔КЖ, ОВ↔ЭО, ОВ↔ТХ, ОВ↔ПБ). Возвращает список
  связей с формулировками «что согласовать».
- `POST /api/projects/{project_id}/goals/proposals/run-3-times` — протокол
  2–3 прогонов. Возвращает свод: unanimous (3/3, приоритет), majority (2/3,
  в работу), split (1/3, на ручную проверку).

**Граница:** эти эндпоинты **не** заменяют CRUD. Они **дополняют** его.
Валидатор работает **до** утверждения Goal. Матрица — **при** предложении
связей. Протокол — **при** проверке предложений.

### 7.2. Эндпоинты ревизий

- `POST /api/documents/{document_id}/revisions` — создать ревизию.
- `GET /api/documents/{document_id}/revisions` — список ревизий.
- `GET /api/revisions/{id}` — ревизия по ID.
- `POST /api/revisions/{id}/changes` — добавить изменение.
- `GET /api/revisions/{id}/changes` — список изменений.
- `POST /api/changes/{id}/decision` — принять решение.
- `POST /api/revisions/{id}/stop-flags` — добавить стоп-сигнал.

## §8. Тесты

Unit-тесты в `backend/tests/`:
- `test_premise_service.py` — CRUD Premise, валидация по схеме.
- `test_goal_service.py` — CRUD Goal, связи с Premise.
- `test_goal_proposal_service.py` — 4 правила (по 2–3 теста на правило).

Smoke-тесты маппинга:
- `test_premise_mapping.py`.
- `test_goal_mapping.py`.

Цель: +25–30 тестов. Итого в проекте — ~150.

### 8.1. Тесты ревизий

- `test_revision_service.py` — CRUD Revision.
- `test_change_service.py` — CRUD Change.
- `test_revision_decision_service.py` — CRUD RevisionDecision.
- `test_stop_flag_service.py` — CRUD StopFlag.
- Цель: +30–40 тестов.

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
- `PremiseCard.tsx` — владелец у каждого поля (если указан).
- `PremiseForm.tsx`.
- `GoalCard.tsx` — бейдж статуса проверки (подтверждено / не соответствует / требует проверки / нет данных).
- `GoalForm.tsx`.
- `GoalProposalList.tsx` — список предложений с утверждением.

Роутинг в `App.tsx`.

UI структуры — список для MVP (ответ на вопрос 6).

### 9.1. UI ревизий

- `RevisionPage.tsx` — список ревизий.
- `RevisionDiffPage.tsx` — сравнение (уровень 2).
- `RevisionDecisionPage.tsx` — форма ответа (6 статусов, уровень 3).
- `StopFlagPage.tsx` — стоп-сигналы.

### 9.2. UI Result и ProjectStandard

- `ResultPage.tsx` — список результатов (1–3** **на** **проект**).
- `ProjectStandardPage.tsx` — список стандартов (из** **ТЗ**).
- `ResultCard.tsx` — карточка** **результата** (с** **связью** **на** `Goal`).
- `ProjectStandardCard.tsx` — карточка** **стандарта** (с** **связью** **на** `Goal`).

## §10. Открытые вопросы вехи

- Вопрос 6: UI структуры — **решено**: карточки со статусом проверки и владельцем.
- Вопрос 13: механизм вывода — **решено**: правила 1–4 + агент-валидатор + матрица смежников + протокол 2–3 прогонов.
- Вопрос 14: утверждение — **решено**: по одному + список + правки + ГИП утверждает **с учётом** статуса проверки.
- Вопрос 15: границы автоматизации — только явное из вводных (решено).

### 10.1. Проверка характеристик (для вехи 1)

**Нативность:**
- ГИП **создаёт** `Result` **из** **договора** → **≤ 3** **кликов**.
- ГИП **создаёт** `Goal` **из** `Premise` → **≤ 3** **кликов**.
- **Нет** **обучающих** **экранов** (система** **объясняет** **себя** **через** **подсказки**).

**Юзабилити:**
- Ошибок** **при** **создании** `Goal` — **≤ 1** **на** **10** (тест** **на** **5** **ГИПах**).
- SUS** **≥ 80** (после** **пилота**).

**Ценность:**
- Время** **на** **создание** `Result` **из** **договора** — **≤ 5** **минут** (было** **30**).
- Время** **на** **создание** `Goal` **из** `Premise` — **≤ 2** **минут** (было** **10**).

**Доверие:**
- Ложных** **срабатываний** **валидатора** — **≤ 10%** (тест** **на** **10** **целях**).
- Пропусков** **на** **критичных** **полях** — **0** (тест** **на** **ревизии**).

### 10.2. Как проводится проверка характеристик

**Проверка** — **не** **один** **раз** **в** **конце**. **Это** **процесс** **на** **каждом** **шаге**.

**Уровень 1. На каждой подсессии (6.8e-1, 6.8e-2...).**
- **Кто:** GigaCode (или разработчик) перед коммитом.
- **Что:**
  - Нативность: кликов до цели ≤ 3?
  - Юзабилити: ошибок при создании Goal ≤ 1 на 10?
  - Доверие: ложных срабатываний валидатора ≤ 10%?
- **Формат:** чек-лист в коммит-сообщении (или `docs/quality/6.8e-1.md`).
- **Если не достигнуто — не коммитить.**

**Уровень 2. На демо вехи (в конце 6.8e).**
- **Кто:** ГИП (или пилотный ГИП).
- **Что:** все четыре характеристики с метриками из `DOMAIN.md` §2.5.
- **Ценность измеряется в цифрах** (было 30 мин → стало 5).
- **Результат:** акт демо (или протокол).
- **Если не достигнуто — фича не принимается, возвращается на доработку.**

**Уровень 3. На пилоте (веха 6).**
- **Кто:** пилотный ГИП + ГИП (автор).
- **Что:**
  - SUS ≥ 80 (опрос пилотных ГИПов).
  - Время на приём ревизии (до 60 мин → после 10).
  - Пропущенных изменений 0 на критичных полях (замер на реальных проектах).
- **Результат:** отчёт пилота.

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
