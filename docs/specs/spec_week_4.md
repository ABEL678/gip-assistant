# spec_week_4.md — Веха 4: Система ведёт RFI

## §1. Что делаем

Веха 4 «Система ведёт RFI».

ГИП видит RFI как особый Task с причиной (Decision или Goal), Actions
(составить / отправить / получить / зарегистрировать), результатом
(Document с новыми ИД) и сроками. Система предлагает RFI на основе
Decision без ИД и просроченных RFI. ГИП утверждает. Полученные ИД
пополняют вводные (Premise).

Ценность: ГИП не теряет запросы на данные. RFI → Document → новые ИД
→ пополнение вводных. Вводные становятся живыми (DOMAIN.md §3.4, §4.6).

## §2. Сущности

### 2.1. RFI как Task (не отдельная таблица)

**Решение зафиксировано:** RFI — это `Task` с флагом `is_rfi=True`, а не
отдельная таблица `rfis`. Причина — DOMAIN.md §4.6: «RFI — особая
разновидность Task». Отдельная таблица дублировала бы `TaskRepository`
(`get_by_id`, `list_by_project`, `save`) и разошлась бы с `Task.state`.

**Новые колонки в `tasks`:**

| Поле | Тип | Обяз. | Комментарий |
|---|---|---|---|
| is_rfi | bool | да | default False. Дискриминатор |
| rfi_cause_decision_id | UUID | нет | FK → decisions (SET NULL) |
| rfi_cause_goal_id | UUID | нет | FK → goals (SET NULL) |
| rfi_due_date | date | нет | Срок ожидания ответа |
| rfi_state | Enum | нет | open / sent / answered / registered / closed / escalated. NULL для не-RFI |

**CHECK на `tasks`:**
(is_rfi = false)
OR (rfi_cause_decision_id IS NOT NULL OR rfi_cause_goal_id IS NOT NULL)

CHECK (
  (is_rfi = false AND rfi_state IS NULL)
  OR (is_rfi = true AND rfi_state IS NOT NULL)
)

text
То есть: если `is_rfi = true` — обязательна хотя бы одна причина
(DOMAIN.md §4.6: «Причина. Всегда — нехватка данных»). Если
`is_rfi = false` — обе колонки должны быть NULL.

**Почему `rfi_state` — отдельная колонка, а не производное от `Task.state`:**
1. `Task.state` — общий жизненный цикл (план / в работе / выполнено /
   отменено). `rfi_state` — специфичный для RFI (open / sent / answered /
   registered / closed / escalated). Это два разных измерения.
2. Может быть: RFI отправлен (`Task.state = в работе`), ответ получен
   (`rfi_state = answered`), но ИД ещё не зарегистрированы
   (`rfi_state ≠ registered`). Совмещать — потеря информации.
3. `rfi_просрочен` работает по `rfi_due_date` + `rfi_state != closed` —
   не по `Task.state`. Если RFI просрочен, но `Task.state = в работе` —
   эскалация всё равно нужна.

**Partial-индексы** (`postgresql_where=text("is_rfi = true")`):
- `idx_tasks_rfi_due_date` — на `(rfi_due_date)`. Для правила `rfi_просрочен`.
- `idx_tasks_rfi_cause_decision` — на `(rfi_cause_decision_id)`. Для правила `decision_без_ид`.
- `idx_tasks_rfi_cause_goal` — на `(rfi_cause_goal_id)`. Для UI «показать RFI по Goal».
- `idx_tasks_is_rfi` — на `(is_rfi)`. Для `list_by_project` с фильтром.

### 2.2. Связь RFI ↔ Premise — через Document, не M:N

**Решение зафиксировано:** `rfi_premises` M:N **не создаём**. Связь
производная: `RFI → Document → Premise`.

Причина — DOMAIN.md §3.4: цепочка «RFI → Action → Document → Premise».
Прямая M:N `rfi_premises` обходила бы Document и теряла бы источник
(«откуда пришёл этот ИД?»). Document — общий предок.

**Новые колонки (из 6.12b):**

| Поле | Тип | Смысл |
|---|---|---|
| `Premise.source_document_id` | nullable FK → documents (SET NULL) | «этот ИД пришёл из документа» |
| `Document.rfi_id` | nullable FK → tasks (SET NULL) | «этот документ — ответ на RFI» |
| `Document.trigger_action_id` | nullable FK → actions (SET NULL) | «этот документ породил Action» |

**Валидация `Document.rfi_id`** — в `DocumentService`, не в БД:
при `rfi_id IS NOT NULL` проверить `task.is_rfi = true` и
`task.project_id = document.project_id`. Триггеры в проекте не
используются (как с `tasks.decision_id` в 6.11a — FK есть, «decision
из того же проекта» — валидация в сервисе).

**Запрос «какие Premise пришли из RFI»** — производный:
```sql
SELECT premise.* FROM premises
JOIN documents ON premises.source_document_id = documents.id
WHERE documents.rfi_id = :rfi_id
Один JOIN, не отдельная таблица.

2.3. Document ↔ Action — 1:1 с двух сторон
Решение зафиксировано: две связи, не M:N.

actions.result_document_id (nullable FK → documents SET NULL) —
«этот Action создал Document» (DOMAIN.md §7.1: «результат»).

documents.trigger_action_id (nullable FK → actions SET NULL) —
«этот Document породил Action» (DOMAIN.md §7.1: «триггер»).

Обе — 1:1, nullable. M:N action_documents — YAGNI, расширим в вехе 5,
если понадобится, не ломая эти колонки.

2.4. Enum RfiState
6 значений: open / sent / answered / registered / closed / escalated.

open — создан, Actions не начаты.

sent — запрос отправлен, ждём ответ.

answered — ответ получен (Document с rfi_id).

registered — новые ИД зарегистрированы (Premise с source_document_id).

closed — RFI закрыт.

escalated — просрочен, эскалирован (правило rfi_просрочен).

Enum — в backend/src/domain/value_objects/enums.py. В модели —
Enum(RfiState, name="rfi_state", create_type=False).

§3. Модель БД
Модели в backend/src/adapters/db/models/:

task.py — обновить: +5 колонок, CHECK, 4 partial-индекса.

action.py — обновить: +result_document_id, индекс.

document.py — обновить (6.12b): +rfi_id, индекс.

premise.py — обновить (6.12b): +source_document_id, индекс.

Миграции Alembic:

6.12a — одна миграция:

tasks: +5 колонок + CHECK ck_tasks_rfi_cause + 4 partial-индекса.

actions: +result_document_id + индекс idx_actions_result_document.

documents: +trigger_action_id + индекс idx_documents_trigger_action.

6.12b — одна миграция:

documents: +rfi_id + индекс idx_documents_rfi.

premises: +source_document_id + индекс idx_premises_source_document.

FK ondelete:

tasks.rfi_cause_decision_id — SET NULL.

tasks.rfi_cause_goal_id — SET NULL.

actions.result_document_id — SET NULL.

documents.trigger_action_id — SET NULL.

documents.rfi_id — SET NULL (6.12b).

premises.source_document_id — SET NULL (6.12b).

§4. DTO
backend/src/application/dto/rfi.py:

RfiBase(BaseModel) — rfi_cause_decision_id, rfi_cause_goal_id,
rfi_due_date, rfi_state (default OPEN), title (в домене Task поле называется title),
deadline, assignee_id, is_complex (наследуются от Task).

RfiCreate(RfiBase) — project_id передаётся в пути. is_rfi = true
выставляется сервисом (не из DTO).

RfiUpdate(BaseModel) — все поля optional (title, deadline, assignee_id, is_complex, rfi_cause_*, rfi_due_date, rfi_state).

RfiRead(RfiBase) — id, project_id, created_at, updated_at,
premise_ids (производное через Document — реальный список, не пустой).

Требование (canvas edge bug, spec_week_3 §4): RfiRead.premise_ids —
реальный список. _to_domain обязан вызвать _fetch_premise_ids,
который делает JOIN через documents. Без этого списки вернутся пустыми.

`_fetch_premise_ids` возвращает `[]` для не-RFI Task, не `None`. Иначе
`RfiRead.premise_ids` упадёт на Pydantic-валидации (`list[UUID]` не
принимает `None`).

RfiProposal(BaseModel) — эфемерный:

id — uuid5 (детерминированный для UI).

action: Literal["create", "escalate"] — что делать с предложением.

rule: str — decision_без_ид / rfi_просрочен.

formulation, rationale (эфемерная, не Task; при from-proposal мапится в Task.title).

reason_decision_id (для create), existing_rfi_id (для escalate).

rfi_due_date.

@model_validator(mode="after")
def _check_action_fields(self):
    if self.action == "create" and self.existing_rfi_id is not None:
        raise ValueError("existing_rfi_id only for escalate")
    if self.action == "escalate" and self.existing_rfi_id is None:
        raise ValueError("existing_rfi_id required for escalate")
    return self

RfiProposalApprove(BaseModel) — formulation, rationale,
rfi_cause_decision_id, rfi_due_date, rfi_state (default OPEN). Без
rfi_cause_goal_id (правило decision_без_ид его не выставляет; для
ручного создания Goal-RFI — через POST /rfis).

`rfi_state` — это `RfiState` (open / sent / …), а не `TaskState`.
При утверждении `RfiCreate` выставляет `Task.state = PLAN`, а
`rfi_state` — отдельно.

§5. Порты и репозитории
Порты в backend/src/domain/ports/repositories.py:

RfiRepository (ABC) — 6.12b. Не дублирует TaskRepository, а
специализирует его:

list_rfis_by_project(project_id) -> list[Task] — Task с is_rfi=true.

get_rfi_by_id(id) -> Task | None.

list_by_cause_decision(decision_id) -> list[Task].

list_by_cause_goal(goal_id) -> list[Task].

list_overdue(today, project_id) -> list[Task] — rfi_due_date < today AND rfi_state NOT IN (closed, registered).

`premise_ids` — через `Document` (см. §2.2). JOIN `_fetch_premise_ids`
реализован private-методом `TaskRepository`; в контракт `RfiRepository`
он не входит.

TaskRepository (существующий) — добавить в _to_domain / _to_model
новые поля (is_rfi, rfi_cause_*, rfi_due_date, rfi_state).
DocumentRepository — добавить trigger_action_id, rfi_id (6.12b).
PremiseRepository — добавить source_document_id (6.12b).
ActionRepository — добавить result_document_id.

save для RFI — через TaskRepository.save (не дублировать).
Синхронизация premise_ids — не в репозитории, а через Document
(см. §2.2). _to_domain в TaskRepository вызывает _fetch_premise_ids
для is_rfi=true.

§6. Сервисы
backend/src/domain/services/rfi_service.py — RfiService (6.12b):

CRUD RFI.

Валидации:

project_id существует.

Ровно одна причина (rfi_cause_decision_id XOR rfi_cause_goal_id).
В БД CHECK допускает OR, сервис строже — XOR. Форма UI должна
валидировать XOR.

rfi_cause_decision_id / rfi_cause_goal_id — из того же проекта.

rfi_state — валидный, только для is_rfi=true.

is_rfi выставляется сервисом (True), не из DTO.

Создаёт Task с is_rfi=true.

backend/src/domain/services/rfi_proposal_service.py —
RfiProposalService (6.12b), 2 правила:

Правило 1 — decision_без_ид:

Decision в state plan / in_progress.

У Decision нет связанных Premise (проверка по decision_premises).

created_at > N дней назад (N = 5, константа в сервисе).

→ предложить:

action = "create"

rule = "decision_без_ид"

formulation = «Запросить ИД для решения: {decision.formulation}»

reason_decision_id = decision.id

rfi_due_date = today + 14 (константа).

Правило 2 — rfi_просрочен:

Task с is_rfi=true.

rfi_due_date < today.

rfi_state NOT IN (closed, registered).

→ предложить:

action = "escalate"

rule = "rfi_просрочен"

formulation = «Эскалировать RFI: {task.formulation}»

rationale = «Просрочен на {days} дней»

existing_rfi_id = task.id.

Почему НЕ goal_без_ид: Goal — «что сделать», Decision — «как сделать».
RFI нужен для Decision, а не для Goal. Goal без Decision — это сигнал
для DecisionProposalService (правило goal_без_решения, spec_week_3 §6),
а не для RFI. Дублировать — неправильный порядок вывода.

Метод propose_rfis(project_id) -> list[RfiProposal]. Не сохраняет
в БД. Возвращает эфемерный список. Без дедупликации (как в spec_week_3 §6).

§7. DI и эндпоинты
DI в backend/src/adapters/api/dependencies.py:

get_rfi_service → RfiServiceDep.

get_rfi_proposal_service → RfiProposalServiceDep.

Роуты в backend/src/adapters/api/routes/rfis.py (6.12c):

GET /api/projects/{project_id}/rfis — список RFI.

POST /api/projects/{project_id}/rfis — создать RFI.

GET /api/rfis/{id} — по id.

PATCH /api/rfis/{id} — обновить.

DELETE /api/rfis/{id} — удалить.

GET /api/projects/{project_id}/rfis/proposals — предложения.

POST /api/projects/{project_id}/rfis/from-proposal — утвердить
предложение action = "create" (создаёт новый RFI).

POST /api/rfis/{id}/escalate — утвердить предложение
action = "escalate" (PATCH существующего RFI: rfi_state = escalated).

Порядок: /proposals и /from-proposal ПЕРЕД /{id} (spec_week_3 §7).

Почему два эндпоинта, а не один: create и escalate — разные
действия (POST создаёт, PATCH обновляет). REST-семантика. UI читает
proposal.action и зовёт нужный.

Регистрация в main.py + routes/__init__.py.

Ошибки: ValueError → 400, IntegrityError → 409, not found → 404.

§8. Тесты
6.12a (backend/tests/):

test_task_rfi_mapping.py — smoke: is_rfi, 5 новых полей, CHECK
(обе причины NULL при is_rfi=false → IntegrityError; обе NULL при
is_rfi=true → IntegrityError; одна из причин → OK), partial-индексы
(через EXPLAIN).

test_action_document_mapping.py — smoke: result_document_id,
trigger_action_id.

test_rfi_repository_persist_end_to_end.py — особый тест (защита
от canvas edge bug): RFI с reason_decision + Document с rfi_id +
2 Premise с source_document_id → save → get_rfi_by_id → premise_ids
непустой. (Частично в 6.12b — Document.rfi_id и Premise.source_document_id
появляются там. В 6.12a — только smoke, что TaskRepository не
теряет новые поля при save/get.)

6.12b:

test_rfi_service.py — CRUD, валидации (ровно одна причина, same
project, is_rfi=true выставляется сервисом).

test_rfi_proposal_service.py — 2 правила (по 2–3 теста на правило):

decision_без_ид: Decision без Premise > 5 дней → предложение;
Decision с Premise → не предлагает; Decision моложе 5 дней → не
предлагает.

rfi_просрочен: RFI просрочен → предложение escalate; RFI в
closed/registered → не предлагает; RFI не просрочен → не
предлагает.

test_document_rfi_link.py — Document.rfi_id валидация в
DocumentService: rfi_id на не-RFI Task → ValueError; rfi_id на
RFI из другого проекта → ValueError.

6.12c:

test_rfis_routes.py — 8 эндпоинтов (httpx.AsyncClient + ASGITransport).

6.12d — UI build (tsc).

6.12e — агент RFI: test_rfi_agent.py — проверка list_overdue,
эскалация, лог.

Цель по вехе 4: +45–55 тестов. Итого: ~437–447.

§9. UI
API-клиент frontend/src/api/rfiApi.ts — 8 методов.
Хук frontend/src/hooks/useRfis.ts — 8 хуков.

Страница frontend/src/pages/RfiPage.tsx — список RFI + блок
«Предложенные RFI».

Компоненты frontend/src/components/:

RfiCard.tsx — карточка (rfi_state бейдж, причина, срок, связи).

RfiForm.tsx — форма (reason_decision / reason_goal, rfi_due_date,
rfi_state).

RfiProposalList.tsx — список предложений. Для action = "create" —
кнопка «Создать», для action = "escalate" — кнопка «Эскалировать».

Роутинг: App.tsx (+маршрут /projects/:id/rfis) + секция «RFI» в
ProjectPage.tsx.

UI — список для MVP. Карточки со статусом и связями.

§10. Открытые вопросы вехи
Вопрос 3 (DOMAIN.md §11): Action ↔ Document — решено (частично):
Action.result_document_id + Document.trigger_action_id (1:1, обе
nullable). M:N — отложено до вехи 5, если понадобится.

Вопрос 11 (DOMAIN.md §11): «Как система видит нехватку ИД?» —
решено: правило decision_без_ид (RfiProposalService). Агент RFI
(6.12e) добавит автономные действия.

Document.role (enum result/trigger/form/new_input) — не
вводим в вехе 4. Роли покрыты двумя FK (result_document_id,
trigger_action_id). Расширим в вехе 5, если понадобится.

10.1. Проверка характеристик (для вехи 4)
Нативность:

ГИП создаёт RFI из предложения → ≤ 3 кликов.

ГИП связывает RFI с Decision → ≤ 2 кликов (поле в форме).

Нет обучающих экранов.

Юзабилити:

Ошибок при создании RFI — ≤ 1 на 10 (тест на 5 ГИПах).

SUS ≥ 80 (после пилота).

Ценность:

Время на создание RFI с причиной — ≤ 2 минут (было 8 в Excel).

Доля RFI с заполненной причиной — 100% (CHECK в БД).

Доля просроченных RFI, по которым сработала эскалация — ≥ 90%.

Доверие:

Ложных срабатываний RfiProposalService (правило decision_без_ид) —
≤ 10% (тест на 10 решениях).

Пропущенных RFI (decision без ИД, не предложен) — ≤ 5%.

Ложных эскалаций (rfi_просрочен на закрытом RFI) — 0%.

§11. Демо
ГИП создаёт Decision «Передать расчёт ВК» → нажимает «Предложить RFI»
→ система предлагает RFI «Запросить ИД для решения: Передать расчёт
ВК» (action = create, причина из Decision, срок +14 дней) → ГИП
утверждает → RFI появляется в списке. ГИП создаёт Action «Получить
ответ» → прикрепляет Document (входящее письмо) → создаёт Premise
«Нагрузки на ВК» → связывает с Document → RFI rfi_state = registered,
вводные пополнились.

Второй сценарий: RFI просрочен (rfi_due_date в прошлом) → система
предлагает эскалацию (action = escalate) → ГИП утверждает → RFI
rfi_state = escalated, Action «Эскалировать» создан.

§12. Что НЕ входит
Агент RFI (автономные действия, 6.12e).

Агент сроков (веха 5).

LLM (веха 6).

Document.role (enum result/trigger/form/new_input) — отложено.

M:N action_documents / rfi_premises — отложено.

goal_без_ид (правило) — не вводим (онтологически неверно, см. §6).

UI дашборда, отчётов, скелета, экспорта, поиска (очередь после вехи 4).

Автоматическое создание RFI без утверждения.