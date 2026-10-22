# ГИП-Ассистент — CONTEXT

> **Назначение:** этот файл — «резюме проекта на 2 страницы». Копируй его
> в начало каждого нового чата с ИИ-ассистентом. Он даёт минимальный
> контекст, достаточный для продуктивной работы.
>
> **Главный документ проекта — `DOMAIN.md`.** CONTEXT.md — краткая выжимка.
> Если противоречие между CONTEXT.md и DOMAIN.md — верен DOMAIN.md.

**Версия:** 2.11 (22.10.2026)
**Актуально на:** после сессии 6.11c (веха 3, часть c)
**Стек:** FastAPI + SQLAlchemy 2.0 async + PostgreSQL 15 + React 18 + TS

---

## 1. Что это за продукт

**ГИП-Ассистент** — среда управления проектом для ГИПа (главного инженера
проекта). Не «удобный Excel» и не «красивый Проводник». А **среда, где
структура проекта вырастает из вводных и логики управления**.

**Формула ядра:**

    Управление проектом = Вводные предпосылки + Логика управления + Механизм вывода

- **Вводные предпосылки** — внешняя образующая: договор, ТЗ, требования
  Заказчика, ИД, нормы, НПА, гос. бюрократия, внутренние ресурсы.
- **Логика управления** — Goal / Decision / Task / Action.
- **Механизм вывода** — то, что превращает вводные в структуру. Система знает вводные и предлагает структуру. ГИП утверждает.
- **Вместе** они определяют: какая будет структура управления проектом
  и какие методы управления применять.

**Что это даёт ГИПу:**

- Видеть проект не как набор файлов, а как **связную картину**:
  что от чего зависит, что где горит, что блокирует.
- Не терять связи между документами (письмо → запрос → том → срок).
- Работать со **структурой, которая не жёсткая** — меняется под ситуацию
  проекта (договор, команда, площадка).
- Делегировать рутину **агентам** (сроки, RFI, связи, нормы, XML).

**Топ-5 болей ГИПа (из 12 интервью):**

1. Координация смежников (10/12).
2. Контроль просрочек (9/12).
3. Потеря задач (8/12).
4. Согласования (7/12) — после пилота.
5. Изменения / РВИ (6/12) — после пилота.

---

## 2. Ядро продукта

**Три слоя:**

| Слой | Что | Где документирован |
|------|-----|---------------------|
| **Вводные** | Внешняя образующая. Договор, ТЗ, требования, ИД, нормы, НПА, ресурсы. | DOMAIN.md §3 |
| **Логика управления** | Goal → Decision → Task → Action. RFI — особый Task. | DOMAIN.md §4 |
| **Структура управления проектом** | Результат. То, что складывается из вводных + логики на конкретном проекте. | DOMAIN.md §5 |

**Дополнительно:**

- **Document** — полиморфная сущность (триггер / результат / форма / новые ИД). DOMAIN.md §7.1.
- **Norm** — внешний норматив. DOMAIN.md §7.2.
- **Агенты** — сотрудники с ролью: сроков, RFI, связей, норм, XML. DOMAIN.md §9.
- **LLM** — механизм вывода (часть DOMAIN.md §9.1). Понимает текст, распознаёт, генерирует.
- **Второй столп онтологии:** система знает вводные → предлагает структуру → ГИП утверждает. Это не таск-трекер.

**Ключевые свойства ядра:**

1. **Вводные и логика — не статичны.** Вводные пополняются через RFI. Логика перестраивается под ситуацию.
2. **Структура — не модель, а результат.** Разная на разных проектах.
3. **Гибкость.** ГИП может работать на любом уровне. Система не требует заполнять всё.
4. **Движение двустороннее.** Сверху вниз (планирование) и снизу вверх (реакция на факт).
5. **Агент предлагает — ГИП решает.** Автономия — только там, где делегировано.

---

## 3. Архитектура (кратко)

**Гексагональная:** domain / application / adapters.

- **Backend:** FastAPI + SQLAlchemy 2.0 async + Alembic. Домен чистый, не зависит от FastAPI/SQLAlchemy.
- **Frontend:** React 18 + Vite + TypeScript + shadcn/ui + TanStack Query + Axios.
- **Bot:** aiogram 3.x.
- **Storage:** MinIO AIStor Free (S3).
- **LLM:** Qwen 2.5 7B локально на VPS (16 GB RAM).
- **Агенты:** слой поверх структуры, работают с LLM.

**Гибридная модель данных:**

- **Системные сущности** (фиксированные): Project, Goal, Decision, Task, Action, RFI, Document, DocumentVersion, DocumentLink, Norm, User, Executor, ImportLog.
- **Пользовательские сущности** (generic): EntityType + Entity, хранятся в JSONB.

Подробнее — `ARCHITECTURE.md`.

---

## 4. Что сделано (факт)

**Backend вехи 1 (1a–1d) — ЗАКРЫТА:**

- 3 таблицы: premises, goals, goal_premises.
- 12 эндпоинтов.
- 187 тестов.
- Backend работает.

**6.8b — ЗАКРЫТ (18.10.2026):**

- ✅ `RuleBasedGoalValidator` — правила 1–6 (§6.1.1).
- ✅ `SimilarityMatrixService` — 10 связей (§6.2.1).
- ✅ `ProposalProtocolService` — unanimous/majority/split (§6.3.1).
- ✅ `GoalValidatorService` → ABC-порт (веха 6 → `LLMGoalValidator`).
- ✅ 219 passed, ruff чисто.

**Веха 1 (UI) — ЗАКРЫТА (17.10.2026):

- ✅ Загрузка исходников (drop zone → файл → БД).
- ✅ Канвас (React Flow): вводные, цели, связи.
- ✅ Удаление: связей, целей, вводных (с подтверждением).
- ✅ Правила вывода из вводных (4 правила).
- ✅ 187 тестов backend (зелёные).
- ✅ Frontend build успешен.

- 17 таблиц: projects, tasks, cross_tasks, task_status_history, executors, users, import_logs, entity_types, entities, document_types, documents, document_versions, document_links, alembic_version, **premises, goals, goal_premises**.
- Миграции: f9f9bed0be0f, 272f011cf740, 78ada0d52056, d357e719c8bf, c719d9b4537e, **686491cea3fd (premises + goals)**.
- Универсальный Excel-парсер.
- 51 эндпоинтов (17 + 22 ГОСТ + 12 premises/goals).
- 187 теста pytest (122 + 17 сервисов + 17 роутов).
- Гексагональная архитектура: domain / application / adapters.
- 11 портов, 11 SQLAlchemy-репозиториев, 8 сервисов + **PremiseService, GoalService, GoalProposalService**.

**6.8f — ЗАКРЫТ (20.10.2026):**

- ✅ Result + ProjectStandard + result_goals + standard_goals.
- ✅ 4 таблицы: results, result_goals, project_standards, standard_goals.
- ✅ Миграция `b8f3a1c2d9e0`.
- ✅ 2 порта: ResultRepository, ProjectStandardRepository.
- ✅ 2 репозитория: SqlAlchemyResultRepository, SqlAlchemyProjectStandardRepository.
- ✅ DTO: ResultCreate/Read/Update, ProjectStandardCreate/Read/Update.
- ✅ 16 файлов, +643 строки. Коммит `9c98717`.

**6.8g — ЗАКРЫТ (20.10.2026):**

- ✅ ResultService — CRUD + валидация formulation.
- ✅ ProjectStandardService — CRUD + валидация existence.
- ✅ 15 unit-тестов. Коммит `5e0a7c9`.

**6.8i — ЗАКРЫТ (20.10.2026):**

- ✅ Result + ProjectStandard CRUD-эндпоинты.
- ✅ Тесты роутов (httpx.AsyncClient + ASGITransport).
- ✅ Коммит `19d37c7`.

**6.8j-1 — ЗАКРЫТ (20.10.2026):**

- ✅ ResultPage, ProjectStandardPage — страницы CRUD.
- ✅ ResultCard, ProjectStandardCard — карточки.
- ✅ ResultForm, ProjectStandardForm — формы.
- ✅ ResultGoalsPanel, StandardGoalsPanel — панели связей с целями.
- ✅ API-клиенты + хуки. Коммит `1d57292`.

**6.8j-2 — ЗАКРЫТ (20.10.2026):**

- ✅ RevisionsPage — страница ревизий.
- ✅ RevisionCard — карточка ревизии.
- ✅ RevisionForm — форма создания ревизии.
- ✅ RevisionDiffPanel — просмотр diff между версиями.
- ✅ API-клиенты + хуки. Коммит `65f943b`.

**Веха 2 — ЗАКРЫТА (20.10.2026):**

- ✅ **6.10a** — модель `Action` + миграция `f9eba6941cdf`. Коммит `953b558`.
- ✅ **6.10b** — `Task.is_complex`. Коммит `f5a527d`.
- ✅ **6.10c** — `ActionService` + `TaskService` + 10 тестов. Коммит `07ea2c3`.
- ✅ **6.10d** — эндпоинты `Action` (6 штук) + DI + 7 тестов. Коммит `ddnf57c`.
- ✅ **6.10e** — UI `Action` (ActionsPage, ActionCard, ActionForm) + интеграция в ProjectPage. Коммит `4b1a50d`.
- ✅ 288 passed, frontend build зелёный.

**Веха 3 — 6.11a (22.10.2026):**

- ✅ **Decision** — доменная сущность + `DecisionState` (5 значений).
- ✅ **Модели:** `DecisionModel`, `DecisionGoalModel`, `DecisionPremiseModel`.
- ✅ **Таблицы:** `decisions`, `decision_goals`, `decision_premises`.
- ✅ **tasks.decision_id** — FK SET NULL + индекс.
- ✅ **Порт:** `DecisionRepository`.
- ✅ **Репозиторий:** `SqlAlchemyDecisionRepository` (M:N через _fetch_*_ids).
- ✅ **DTO:** `DecisionBase`, `DecisionCreate`, `DecisionUpdate`, `DecisionRead`.
- ✅ **Миграция:** `8aad8fd713f0`.
- ✅ **298 тестов pytest.**

**Веха 3 — 6.11b (22.10.2026):**

- ✅ **Norm** — доменная сущность + `NormType` (5 значений).
- ✅ **DecisionLink** — доменная сущность + `DecisionLinkType` (3 значения).
- ✅ **Модели:** `NormModel`, `DecisionLinkModel`, `DecisionNormModel`.
- ✅ **Таблицы:** `norms`, `decision_links`, `decision_norms`.
- ✅ **Порты:** `NormRepository`, `DecisionLinkRepository`, `DecisionNormRepository`.
- ✅ **Репозитории:** `SqlAlchemyNormRepository`, `SqlAlchemyDecisionLinkRepository`, `SqlAlchemyDecisionNormRepository`.
- ✅ **DTO:** `NormBase/Create/Update/Read`, `DecisionLinkBase/Create/Read`.
- ✅ **Миграция:** `c52a3c176d47`.
- ✅ **310 тестов pytest.**

**Веха 3 — 6.11c (22.10.2026):**

- ✅ **Сервисы:** DecisionService (CRUD + валидации premise_ids/goal_ids из того же проекта), NormService (code уникален в проекте), DecisionLinkService (self-link → ValueError), DecisionNormService (link/unlink, идемпотентно), DecisionProposalService (2 правила вывода: goal_без_решения, срок_из_вводных; без дедупликации).
- ✅ **Домен:** DecisionProposal entity (эфемерная).
- ✅ **DTO:** DecisionProposal.
- ✅ **Порт:** NormRepository.get_by_code.
- ✅ **DI:** 5 service-getter'ов + 4 repo-getter'а.
- ✅ **366 тестов pytest.**

**Веха 1a–1d (октябрь 2026) — ЗАКРЫТО:**

- 3 новые таблицы: premises, goals, goal_premises.
- Домен: Premise, Goal, GoalProposal (dataclass).
- DTO: PremiseSchema, GoalSchema, GoalProposal, GoalProposalApprove.
- Порты: PremiseRepository, GoalRepository.
- Сервисы: PremiseService, GoalService, GoalProposalService (4 правила вывода).
- DI: 6 зависимостей.
- 12 эндпоинтов (5 premises + 7 goals).
- 17 тестов роутов (httpx.AsyncClient + ASGITransport).
- 187 тестов pytest (было 122).

**Веха 1 (UI) — ВОССТАНОВЛЕНА (19.10.2026):**

- ✅ Списки + формы: PremisesPage, GoalsPage.
- ✅ PremiseCard — owner-бейджи в data.
- ✅ PremiseForm — data + schema_ textarea (JSON).
- ✅ GoalCard — verification_status бейдж + кнопка «Проверить» + evidence popup.
- ✅ GoalForm — schema_ textarea + readonly status.
- ✅ GoalProposalList — утвердить/отклонить/править.
- ✅ SimilarityMatrixPanel — список связей from_section ↔ to_section.
- ✅ ProtocolSummaryPanel — кнопка запуска + unanimous/majority/split.
- ✅ TypeScript — без ошибок.
- ✅ Frontend build успешен.

**Frontend:**

- Уровень 1 UI: EntityTypesPage, EntityTypeConstructorPage, EntitiesPage + компоненты.
- Уровень 1.5 UI: DocumentsPage, DocumentConstructorPage, DocumentVersionsPage, DocumentLinksPage + компоненты.
- 5 API-клиентов, 22 хука TanStack Query, 9 UI-файлов документов.
- 5 маршрутов документов.

**Bot:** aiogram 3.x, @gip_assistant_ru_bot, /start /help /link /status.

**Инфра:** Docker Compose (gip_db на 5555), Nginx-конфиг (план).

**AI-контекст и документация:**

- **`docs/context/DOMAIN.md` v1.1** — онтология ядра. **Главный документ.
- `docs/archive/Дорожная_карта_6.4.md` (архив).
- `docs/archive/ТЗ_4.4.md` (архив).
- `docs/context/CONTEXT.md` — этот файл.
- `docs/context/TASKS.md`, `ARCHITECTURE.md`, `DATABASE.md`, `API.md`, `RULES.md`, `HANDOFF.md`.
- `AGENTS.md` — правила для GigaCode.

---

## 5. Что в работе / следующий шаг

**На 22.10.2026, после 6.11c:**

- 6.11a/b/c закрыты: модель Decision + Norm + DecisionLink + сервисы (366 passed).
- Следующая подсессия — **6.11d** (эндпоинты + DI для роутов).
- Порядок: 6.11d (эндпоинты) → 6.11e (UI).

**Ветка `feat/entity-type-templates-domain`** — в паузе, не мержить, не удалять.

---

## 6. Ключевые документы

- **`docs/context/DOMAIN.md`** — онтология ядра. **Читать первым.**
- `docs/archive/Дорожная_карта_6.4.md` (архив).
- `docs/archive/ТЗ_4.4.md` (архив).
- `docs/context/` — AI-контекст (**коммитится**):
  - `CONTEXT.md` — этот файл.
  - `ARCHITECTURE.md` — структура и слои.
  - `DATABASE.md` — схема БД.
  - `API.md` — эндпоинты.
  - `RULES.md` — правила кода.
  - `TASKS.md` — что сделано / в работе / дальше.
  - `HANDOFF.md` — эстафета.
- `AGENTS.md` (в корне) — правила для ИИ-агентов.

---

## 7. Ключевые принципы

1. **Домен чистый** (без FastAPI/SQLAlchemy).
2. **Порты и адаптеры** (гексагональная архитектура).
3. **Вводные + логика = структура управления проектом.** Ядро продукта.
4. **Структура не жёсткая.** Вырастает из вводных. Меняется под ситуацию.
5. **Система знает вводные — предлагает — ГИП утверждает.** Второй столп онтологии. Это не таск-трекер.
6. **XML — обязательное требование экспертизы.**
7. **AI-контекст — часть продукта.**
8. **ИИ-инструменты — только с поддержкой в РФ:** GigaCode (PyCharm).
9. **Один шаг за раз, с проверками.**
10. **Тесты для бизнес-логики обязательны.**
11. **Не коммитить в main напрямую.**
12. **Не менять `.env` и секреты.**
13. **UX — канвас, не списки.** ГИП думает связями. Списки — дремуче.
14. **Абстракция валидатора.** `GoalValidatorService` — порт (ABC). Реализации: `RuleBasedGoalValidator` (веха 1–5), `LLMGoalValidator` (веха 6). Сервисы зависят от порта.

---

## 8. Что НЕ делать (антипаттерны)

- Не использовать Celery, Redis, RabbitMQ (MVP).
- Не использовать публичные облачные LLM.
- Не менять архитектуру без согласования.
- Не использовать `try/except` для валидации (Pydantic).
- Не добавлять новые зависимости без явного разрешения.
- Не смешивать правила кода (RULES.md) и правила текстов ПД.
- Не коммитить в `main` напрямую.
- **Не строить продукт на описании, которое человек дал постфактум.** Проверять модель на реальных сценариях.
- **Не навязывать структуру.** Система поддерживает все уровни, но не требует заполнять всё.
- **Не путать «документооборот» и «управление проектом».** Продукт — второе.

---

## 9. Контакты и ссылки

- **GitHub:** https://github.com/ABEL678/gip-assistant (private).
- **Домен (план):** gip-assistant.ru.
- **Схемы Минстроя:** https://minstroyrf.gov.ru/tim/xml-skhemy/.
- **GigaCode:** https://gigacode.ru.
- **gpt2giga:** https://github.com/ai-forever/gpt2giga.
- **GigaChat API:** https://developers.sber.ru/portal/products/gigachat-api.
- **Стек (backend):** FastAPI 0.110+, SQLAlchemy 2.0+, PostgreSQL 15+.
- **Стек (frontend):** React 18+, Vite 5+, TypeScript 5+, shadcn/ui.

---

**Конец CONTEXT.md v2.11.**