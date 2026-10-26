# TASKS.md — статус проекта

> **Назначение:** что сделано / в работе / дальше. Обновляется перед каждым
> новым чатом с ИИ. Помогает понять статус проекта без пересказа.
>
> **Главный документ проекта — `DOMAIN.md`.** TASKS.md — статус.
> Если противоречие между TASKS.md и DOMAIN.md — верен DOMAIN.md.

**Версия:** 2.12
**Обновлено:** 27.10.2026
**Автор:** ГИП, руководитель разработки

---

## Легенда

| Символ | Значение |
|--------|----------|
| ✅ | Сделано |
| 🔄 | В работе |
| ⏳ | Запланировано |
| 🚫 | Заблокировано |
| ❌ | Отменено |

---

## 1. Что сделано (Done)

### Этап 0. Подготовка (сентябрь–октябрь 2026)

- ✅ Регистрация ИП на УСН 6%.
- ✅ ОКВЭД: 62.01, 62.02, 62.09, 63.11.
- ✅ ЭЦП через ФНС.
- ✅ Домен gip-assistant.ru куплен.
- ✅ Customer Development (12+ интервью с ГИПами).
- ✅ Конкурентный анализ.
- ⏳ Товарный знак — в процессе.

### Этап 1. Прототип (октябрь 2026) — ЗАКРЫТ

**Backend:**

- ✅ FastAPI + SQLAlchemy 2.0 async + PostgreSQL 15 + Alembic.
- ✅ 8 таблиц: projects, tasks, cross_tasks, task_status_history,
  executors, users, import_logs, alembic_version.
- ✅ Миграции: f9f9bed0be0f (initial 7 tables), 272f011cf740 (to_section_code).
- ✅ Гексагональная архитектура (domain / application / adapters).
- ✅ 16+ эндпоинтов.
- ✅ Универсальный Excel-парсер (merged cells, автопоиск шапки, serial-даты).
- ✅ 39 тестов pytest.

**Frontend:**

- ✅ React 18 + Vite + TypeScript + shadcn/ui + Tailwind.
- ✅ TanStack Query + React Router + Axios.
- ✅ Импорт Excel.
- ✅ TaskList (500+ задач, фильтры, inline).
- ✅ Матрица смежников (10×10, 14 ячеек, цвета, смена статуса).
- ✅ Страница задач пары.

**Bot:**

- ✅ aiogram 3.x.
- ✅ @gip_assistant_ru_bot.
- ✅ Команды /start, /help, /link, /status.
- ✅ Код ежедневной сводки (не запущен в проде).

**Инфра:**

- ✅ Docker Compose (gip_db на 5555).
- ✅ Nginx-конфиг (черновик).
- ✅ Монорепо: backend/, frontend/, website/, docker/, docs/.

### Уровень 1 (MVP): Универсальные сущности — backend (октябрь 2026) — ЗАКРЫТ

- ✅ Домен: EntityType, Entity.
- ✅ SQLAlchemy-модели: EntityTypeModel, EntityModel (TimestampMixin).
- ✅ Миграция 78ada0d52056 (entity_types + entities + GIN-индекс).
- ✅ DTO: EntityTypeSchema, FieldDefinition, EntityTypeCreate/Read/Update,
  EntityCreate/Read/Update (с AliasChoices для schema).
- ✅ Порты репозиториев (EntityTypeRepository, EntityRepository).
- ✅ Репозитории (SqlAlchemy*) — save через merge.
- ✅ Сервисы: EntityTypeService, EntityService.
- ✅ API: 10 эндпоинтов.
- ✅ DI: EntityTypeServiceDep, EntityServiceDep.
- ✅ 26 unit-тестов pytest.
- ✅ **Итого в проекте: 65 тестов pytest**.

### AI-контекст и документация (октябрь 2026)

- ✅ Дорожная карта 6.4 — в архиве.
- ✅ ТЗ 4.4 — в архиве.
- ✅ `docs/context/CONTEXT.md` — создан (**v2.0** после сессии 6.0).
- ✅ `docs/context/ARCHITECTURE.md` — создан.
- ✅ `docs/context/DATABASE.md` — создан.
- ✅ `docs/context/API.md` — создан.
- ✅ `docs/context/RULES.md` — создан.
- ✅ `docs/context/TASKS.md` — создан (этот файл, v2.0).
- ✅ `docs/README.md` — карта документации (25.10.2026, заменила `docs/context/README.md`).
- ✅ `AGENTS.md` — создан (в корне).
- ✅ GigaCode — установлен и протестирован.
- ✅ **`docs/context/DOMAIN.md` v1.0** — создан в сессии 6.0.

  **GigaCode:**
  - ✅ Плагин установлен в PyCharm.
  - ✅ Project Context → `docs/context/` подключён.
  - ✅ `AGENTS.md` подключён через Rules (apply: always, mode: all).
  - ✅ Auto-Approve — пусто (безопасно).
  - ✅ Протестирован на 5 сценариях.
  - ✅ Вывод: GigaCode заменяет 80% запланированного самописного агента.

### Уровень 1 (MVP): UI конструктора типов — ЗАКРЫТ (12.10.2026)

- ✅ entityApi.ts.
- ✅ useEntityTypes.ts, useEntities.ts.
- ✅ EntityTypeCard.tsx, FieldEditor.tsx, FieldList.tsx.
- ✅ EntityTypesPage.tsx, EntityTypeConstructorPage.tsx.
- ✅ DynamicField.tsx, DynamicTable.tsx, EntitiesPage.tsx.
- ✅ textarea.tsx (shadcn/ui).
- ✅ Интеграция в ProjectPage.tsx.
- ✅ Роутинг в App.tsx (4 маршрута).
- ✅ TypeScript — без ошибок.

### Сессия 5.4a (Frontend API-клиенты и хуки для ГОСТ-документов) — ЗАКРЫТ (16.10.2026)

- ✅ documentEnums.ts — 4 enum-типа.
- ✅ 4 API-клиента: documentTypesApi, documentsApi, documentVersionsApi, documentLinksApi.
- ✅ 4 хуковых файла: useDocumentTypes, useDocuments, useDocumentVersions, useDocumentLinks.
- ✅ TypeScript — без ошибок.
- ✅ **Итого: 22 хука, 5 API-клиентов.**

### Сессия 5.4b-1 (DocumentsPage + DocumentCard) — ЗАКРЫТ (16.10.2026)

- ✅ DocumentCard.tsx.
- ✅ DocumentsPage.tsx (фильтр по lifecycle_status, grid, empty/error/loading).
- ✅ TypeScript — без ошибок.

### Сессия 5.4b-2 (DocumentConstructorPage — форма) — ЗАКРЫТ (16.10.2026)

- ✅ DocumentConstructorPage.tsx (3 карточки).
- ✅ Два payload: create / update (PATCH).
- ✅ Sentinel "__none__".
- ✅ TypeScript — без ошибок.

### Сессия 5.4b-3 (роутинг + секция «Документы» в ProjectPage) — ЗАКРЫТ (16.10.2026)

- ✅ App.tsx — 3 маршрута документов.
- ✅ ProjectPage.tsx — секция «Документы».
- ✅ TypeScript — без ошибок.

### Сессия 5.4c (DocumentVersionsPage + VersionCard + VersionForm) — ЗАКРЫТ (16.10.2026)

- ✅ VersionCard.tsx, VersionForm.tsx, DocumentVersionsPage.tsx.
- ✅ TypeScript — без ошибок.

### Сессия 5.4d (DocumentLinksPage + LinkCard + LinkForm) — ЗАКРЫТ (16.10.2026)

- ✅ LinkCard.tsx, LinkForm.tsx, DocumentLinksPage.tsx.
- ✅ TypeScript — без ошибок.

### Сессия 5.4e (роутинг версий/связей + кнопки на форме) — ЗАКРЫТ (16.10.2026)

- ✅ App.tsx — 2 маршрута (versions, links).
- ✅ DocumentConstructorPage.tsx — кнопки «Версии»/«Связи».
- ✅ TypeScript — без ошибок.
- ✅ **Итого: 5 маршрутов документов, 9 UI-файлов.**

### Уровень 1.5 (ГОСТ-хранение) — ЗАКРЫТ (14–15.10.2026)

**Сессия 5.1 (домен + модели):**
- ✅ Домен: Document, DocumentVersion, DocumentLink, DocumentType.
- ✅ VO: 4 Enum.
- ✅ SQLAlchemy-модели: 4 таблицы.
- ✅ Миграция c719d9b4537e + сиды document_types.
- ✅ Обновление DATABASE.md.

**Сессия 5.2a (порты):**
- ✅ 4 порта репозиториев.
- ✅ Итого портов: 11.

**Сессия 5.2b (DTO):**
- ✅ 4 DTO-файла: 13 Pydantic-классов.

**Сессия 5.2c-1 (репозитории):**
- ✅ 4 SQLAlchemy-репозитория.
- ✅ Enum-маппинг.
- ✅ set_current: два UPDATE в одной транзакции.
- ✅ Итого репозиториев: 11.

**Сессия 5.2c-2 (smoke-тесты маппинга):**
- ✅ 8 smoke-тестов: test_document_mapping.py.
- ✅ Итого тестов pytest: 73.

**Сессия 5.2d (сервисы):**
- ✅ 4 сервиса: DocumentType, Document, DocumentVersion, DocumentLink.
- ✅ Валидации: уникальность кода, existence checks, self-link, same project.
- ✅ Итого сервисов: 8.

**Сессия 5.2e-1 (DI):**
- ✅ 2 __init__.py + dependencies.py.

**Сессия 5.2e-2 (роуты):**
- ✅ 4 роутера: 22 эндпоинта.
- ✅ Порядок: /by-code ПЕРЕД /{id}.
- ✅ Роуты через ServiceDep.

**Сессия 5.2e-3 (регистрация):**
- ✅ Регистрация в main.py.
- ✅ API.md: +22 эндпоинта.
- ✅ Итого эндпоинтов: 39.

**Сессия 5.2f-1 (unit-тесты сервисов, часть 1):**
- ✅ test_document_type_service.py (10 тестов).
- ✅ test_document_service.py (13 тестов).
- ✅ Итого тестов pytest: 96.

**Сессия 5.2f-2 (unit-тесты сервисов, часть 2):**
- ✅ test_document_version_service.py (15 тестов).
- ✅ test_document_link_service.py (11 тестов).
- ✅ Итого тестов pytest: 122.

### Сессия 6.0 (Пересборка ядра продукта) — ЗАКРЫТ (16.10.2026)

- ✅ **`docs/context/DOMAIN.md` v1.0** — онтология ядра.
- ✅ Формула: `вводные + логика = структура управления проектом и методы управления`.
- ✅ Вводные предпосылки: договор, ТЗ, требования Заказчика, ИД, нормы, НПА, гос. бюрократия, внутренние ресурсы.
- ✅ Логика управления: Goal → Decision → Task → Action.
- ✅ Task — группа действий (не уровень между Decision и Action).
- ✅ Постановка задачи и закрытие — тоже Action.
- ✅ RFI — особый Task (причина — нехватка ИД, результат — Document, пополняющий вводные).
- ✅ Norm — внешний норматив, отдельная сущность.
- ✅ Агенты: сроков, RFI, связей, норм, XML. Сотрудники с ролью.
- ✅ LLM — мозг, пассивный. Агенты — руки, активные.
- ✅ Отменены: «6 шаблонов документов», «Реестры» в UI, «вкладки как папки».
- ✅ Ветка `feat/entity-type-templates-domain` — в паузе.

### Сессия 6.1 (уточнение онтологии) — ЗАКРЫТ (16.10.2026)

- ✅ Второй столп: «Система знает вводные → предлагает → ГИП утверждает».
- ✅ Формула ядра: трёхэлементная (вводные + логика + механизм вывода).
- ✅ Механизм вывода двухуровневый: правила (вехи 1–5) + LLM (веха 6).
- ✅ ГИП — редактор, не «кнопка ок».
- ✅ Осторожность предложений: вехи 1–5 — только явное из вводных.
- ✅ DOMAIN.md обновлён до v1.1.
- ✅ HANDOFF.md обновлён.

### Веха 1 — ЗАКРЫТА (17.10.2026)

**Backend (1a–1d):**

- ✅ Домен, модели, миграция.
- ✅ DTO, порты, репозитории.
- ✅ Сервисы + 4 правила вывода.
- ✅ DI + 12 эндпоинтов + 17 тестов роутов.
- ✅ 187 тестов pytest.

**UI (1f):**

- ✅ Загрузка исходников (drop zone → файл → БД).
- ✅ Канвас (React Flow): вводные, цели, связи.
- ✅ Удаление: связей, целей, вводных (с подтверждением).
- ✅ Правила вывода из вводных:
  - Правило 1 (договор) — `date` / `data['deadline']`.
  - Правило 2 (ТЗ) — `name` + `LLM TODO`.
  - Правило 3 (требование) — `name`.
  - Правило 4 (ИД) — `valid_until < today`.
- ✅ 187 тестов backend (зелёные).
- ✅ Frontend build успешен.

---

### 6.8b — ЗАКРЫТ (18.10.2026)

**6.8b-1 (GoalValidatorService):**
- ✅ `GoalValidatorService` — правила 1–6 (§6.1.1).
- ✅ `ValidationResult` / `ValidationEvidence` DTO.
- ✅ `Premise.data_field(name)` хелпер.
- ✅ `PremiseDataField` перенесён в `domain/value_objects/premise_data.py`.
- ✅ 8 тестов. Фикс Rule 4/5 (порядок) + 1 тест.
- ✅ Коммиты: `130c334`, `fe894d0`.

**6.8b-2 (SimilarityMatrixService):**
- ✅ 10 связей (§6.2.1).
- ✅ Поиск разделов: (B) `data["sections"]`, (C) строковые значения `data`.
- ✅ 10 тестов.
- ✅ Коммит: `21880b7`.

**6.8b-3 (ProposalProtocolService + рефактор валидатора):**
- ✅ `GoalValidatorService` → ABC-порт (`domain/ports/goal_validator.py`).
- ✅ `RuleBasedGoalValidator` — реализация.
- ✅ Спека §6.3.1: unanimous / majority / split.
- ✅ `ProposalProtocolService` — свод (§6.3.1).
- ✅ `ProtocolSummary` DTO.
- ✅ 7 тестов.
- ✅ Коммиты: `964579d`, `411932f`.

**Итог:** 219 passed, ruff чисто.

---

## 2. В работе (In Progress)

**На 27.10.2026 — Веха 4 (RFI): 6.12a–6.12d закрыты; 6.14a закрыта; в работе — 6.14b–d.**

- ✅ 6.11b — ЗАКРЫТ (22.10.2026).
  - 3 новые сущности: Norm, DecisionLink, DecisionNorm.
  - 3 новые таблицы: norms, decision_links, decision_norms.
  - 2 новых enum'а: NormType (5), DecisionLinkType (3).
  - 3 новых порта, 3 новых репозитория, 2 DTO-файла.
  - Миграция: `c52a3c176d47`.
  - 12 smoke-тестов.
  - **Итого в проекте: 310 тестов pytest.**
- ✅ 6.11c — ЗАКРЫТ (22.10.2026).
  - 5 сервисов: DecisionService, NormService, DecisionLinkService, DecisionNormService, DecisionProposalService.
  - Домен: DecisionProposal entity (эфемерная). DTO: DecisionProposal.
  - Порт: NormRepository.get_by_code (уникальность code в проекте).
  - DI: 4 repo-getter'а + 5 service-getter'ов.
  - 56 unit-тестов.
  - **Итого в проекте: 366 тестов pytest.**
- ✅ 6.11d — ЗАКРЫТ (22.10.2026).
  - 4 роутера: decisions (7), norms (5), decision_links (5), decision_norms (4).
  - 21 новый эндпоинт: ValueError → 400, IntegrityError → 409, not found → 404.
  - DTO: DecisionProposalApprove (без state — по образцу GoalProposalApprove).
  - Регистрация в main.py + routes/__init__.py.
  - 26 тестов роутов (httpx.AsyncClient + ASGITransport).
  - **Итого в проекте: 392 теста pytest.**
- ✅ **6.11e** — UI вехи 3 (22.10.2026).
  - 4 API-клиента: decisionApi, normApi, decisionLinkApi, decisionNormApi.
  - 3 хука: useDecisions (7), useNorms (5), useDecisionLinks (5).
  - 7 компонентов: DecisionCard, DecisionForm, DecisionProposalList, NormCard, NormForm, DecisionLinkCard, DecisionLinkForm.
  - 3 страницы: DecisionsPage, NormsPage, DecisionLinkPage.
  - Роутинг: App.tsx (3 маршрута), ProjectPage.tsx (секция «Решения»).
  - `npm run build` зелёный.
- **Веха 3 закрыта: 6.11a → 6.11b → 6.11c → 6.11d → 6.11e.**
- ✅ **6.12d** — UI RFI (25.10.2026).
  - 6 новых файлов: `rfiApi.ts` (8 методов), `useRfis.ts` (8 хуков), `RfiCard`, `RfiForm`, `RfiProposalList`, `RfiPage`.
  - 2 изменённых: `App.tsx` (маршрут `projects/:id/rfis`), `ProjectPage.tsx` (секция «RFI»).
  - Локальное скрытие обработанных предложений + «Обновить»; `onError` у всех мутаций.
  - `npm run build` / `npm run lint` — зелёные; pytest — 450 passed.
- ✅ **6.14a** — слой данных LLM (27.10.2026).
  - Домен: `LLMSettings`, `LLMProvider` (2), `DataSecurityLevel` (3).
  - Порты: `LLMProviderPort`, `SecretCipherPort`, `LLMSettingsRepository`.
  - БД: `llm_settings` (BYTEA-ключ + last4, JSONB, partial unique index), `projects.data_security_level`.
  - Миграция: `65999c8dbf97` (идемпотентные `CREATE TYPE`).
  - Адаптеры/сервисы: `FernetCipher`, `SqlAlchemyLLMSettingsRepository`, `LLMSettingsService`.
  - Тесты: +31; **итого 481 passed**.

## 3. Дальше (Next)

**6.12d (UI RFI) — ЗАКРЫТА и проверена вручную (27.10.2026).**
- Создание RFI из формы работает (причина — Goal, срок, состояние).
- Карточка RFI отображает бейдж, причину, срок, связи.
- Тестовый проект: `5abc7792-0bdf-4ee9-8c96-4320d16978b2`.

### Ось времени (план-график)

- ⏳ Ось времени — план-график.
- ⏳ Просрочки — красным.
- ⏳ Критический путь — жирным.

### Веха 1 — агенты

- ⏳ Агент-валидатор (проверка на доказанность) — часть Вехи 1.
- ⏳ RFI-предложение (когда данных нет) — часть Вехи 1.

### Веха 1 (6.8) — по подсессиям

- ✅ **6.8a** — модель БД (миграция `verification_status` + `PremiseDataField`), DTO, порты/репозитории.
- ✅ **6.8b** — сервисы (валидатор + матрица + протокол). Коммиты `130c334`, `fe894d0`, `21880b7`, `964579d`, `411932f`.
- ✅ **6.8c** — DI + эндпоинты + тесты роутов.
- ✅ **6.8d** — UI (страницы, карточки, статус, владелец, матрица, протокол).
- ✅ **6.8f** — Result + ProjectStandard + result_goals + standard_goals + миграция + DTO + порты + репозитории.
- ✅ **6.8g** — сервисы Result + ProjectStandard (CRUD + валидации + 15 тестов).
- ✅ **6.8i** — эндпоинты Result + ProjectStandard + тесты роутов.
- ✅ **6.8j-1** — UI Result + ProjectStandard (страницы, карточки, формы, панели связей).
- ✅ **6.8j-2** — UI Revisions (страница, карточки, форма, diff-панель).

### Веха 2 — ЗАКРЫТА (20.10.2026)

- ✅ **6.10a** — модель `Action` + миграция `f9eba6941cdf`. Коммит `953b558`.
- ✅ **6.10b** — `Task.is_complex`. Коммит `f5a527d`.
- ✅ **6.10c** — `ActionService` + `TaskService` + 10 тестов. Коммит `07ea2c3`.
- ✅ **6.10d** — эндпоинты `Action` (6 штук) + DI + 7 тестов. Коммит `ddnf57c`.
- ✅ **6.10e** — UI `Action` (ActionsPage, ActionCard, ActionForm) + интеграция в ProjectPage. Коммит `4b1a50d`.
- ✅ 288 passed, frontend build зелёный.

### Веха 2 — Action + Task-адаптация

- ✅ 6.10a–6.10e — ЗАКРЫТО.
- ✅ 288 passed.

### Веха 3 — Decision + Norm + DecisionLink

- ✅ **6.11a** — модель Decision + миграция + DTO + порты + репозитории (22.10.2026).
  - Домен: `Decision` entity, `DecisionState` enum (5 значений).
  - Модели: `DecisionModel`, `DecisionGoalModel`, `DecisionPremiseModel`.
  - Таблицы: `decisions`, `decision_goals`, `decision_premises`.
  - Колонка: `tasks.decision_id` (FK SET NULL).
  - Порт: `DecisionRepository`.
  - Репозиторий: `SqlAlchemyDecisionRepository` (с _fetch_goal/premise_ids).
  - DTO: `DecisionBase`, `DecisionCreate`, `DecisionUpdate`, `DecisionRead`.
  - Миграция: `8aad8fd713f0`.
  - Тесты: 10 smoke-тестов (mapping, M:N, task.decision_id).
  - **Итого в проекте: 298 тестов pytest.**
- ✅ **6.11b** — модель Norm + DecisionLink + DecisionNorm + миграция + DTO + порты + репозитории (22.10.2026).
  - Домен: `Norm` entity, `DecisionLink` entity, `NormType` (5 значений), `DecisionLinkType` (3 значения).
  - Модели: `NormModel`, `DecisionLinkModel`, `DecisionNormModel`.
  - Таблицы: `norms`, `decision_links`, `decision_norms`.
  - Порты: `NormRepository`, `DecisionLinkRepository`, `DecisionNormRepository`.
  - Репозитории: `SqlAlchemyNormRepository`, `SqlAlchemyDecisionLinkRepository`, `SqlAlchemyDecisionNormRepository`.
  - DTO: `NormBase/Create/Update/Read`, `DecisionLinkBase/Create/Read`.
  - Миграция: `c52a3c176d47`.
  - Тесты: 12 smoke-тестов (mapping, enums, link/unlink, idempotency).
  - **Итого в проекте: 310 тестов pytest.**
- ✅ **6.11c** — сервисы вехи 3 (22.10.2026).
  - Сервисы: `DecisionService` (CRUD + валидации), `NormService` (code уникален в проекте), `DecisionLinkService` (self-link/дубль/проект → ValueError), `DecisionNormService` (link/unlink, идемпотентно), `DecisionProposalService` (2 правила: goal_без_решения, срок_из_вводных; без дедупликации).
  - Домен: `DecisionProposal` entity (эфемерная, uuid5-ids для UI).
  - DTO: `DecisionProposal`.
  - Порт: `NormRepository.get_by_code` (+ реализация).
  - DI: 4 repo-getter'а + 5 service-getter'ов (dependencies.py).
  - Экспорт 4 репозиториев 6.11a/b в repositories/__init__.py.
  - Тесты: 56 unit-тестов (5 файлов).
  - **Итого в проекте: 366 тестов pytest.**
- ✅ **6.11d** — эндпоинты + DI (22.10.2026).
  - 4 роутера: decisions (7), norms (5), decision_links (5), decision_norms (4).
  - 21 эндпоинт: CRUD + proposals/from-proposal + link/unlink.
  - 26 тестов роутов.
  - **Итого в проекте: 392 теста pytest.**
- ✅ **6.11e** — UI вехи 3 (22.10.2026).
  - 4 API-клиента, 3 хука, 7 компонентов, 3 страницы, роутинг.
  - `npm run build` зелёный.
- **Веха 3 закрыта: 6.11a → 6.11b → 6.11c → 6.11d → 6.11e.**

### Веха 3 — первые агенты

- ⏳ Агент сроков.
- ⏳ Агент RFI.

### Веха 4 — LLM + MinIO + XML + Auth

- ⏳ Qwen 2.5 7B локально.
- ⏳ MinIO (хранилище).
- ⏳ XML (агент XML + валидация XSD).
- ⏳ Auth (JWT + Argon2).

### Затем

- ⏳ Деплой на VPS.
- ⏳ Лендинг + комплаенс 152-ФЗ + пилот.

### LLM (Qwen 2.5 7B)

- ⏳ Развёртывание на VPS (16 GB RAM).
- ⏳ Подключение к агентам.
- ⏳ Распознавание структуры в тексте.

### Затем

- ⏳ MinIO (хранилище документов).
- ⏳ XML (агент XML + валидация XSD).
- ⏳ Auth (JWT + Argon2) + Telegram-сводка + деплой на VPS.
- ⏳ Лендинг + комплаенс 152-ФЗ + пилот.

### 6.14 — Админка LLM (4 подсессии)

**6.14 — Админка LLM** (веха 4, после 6.12d, до 6.12e). 4 подсессии:
- **6.14a** — domain (`LLMSettings`), порт `LLMProviderPort`, модель `llm_settings` (с `api_key_encrypted` + `api_key_last4`), миграция, репо, сервис. +поле `Project.data_security_level`.
- **6.14b** — адаптеры: `QwenAdapter`, `OpenAICompatibleAdapter`, `RuntimeLLMAdapter` (TTL 60s, светофор по `project.data_security_level`).
- **6.14c** — DTO, DI, роуты (`/api/admin/llm/status|switch|providers|settings`), тесты.
- **6.14d** — UI (`AdminLLMPage`), `adminLlmApi.ts`, `useAdminLlm.ts`.

### 6.13 — Дельта-подсессии (расширение вехи 1)

**6.13a** — парсинг PDF/DOCX + поле `text_content` в `DocumentVersion`.
**6.13b** — `PremiseService.link_document()` (связывание Document ↔ Premise).
**6.13c** — валидация в GUI (кнопка «Подтвердить» в `PremiseCard`).
**6.13d** — доработка `RevisionDiffPanel`.

Ссылка: `docs/context/MASTER_PIPELINE.md §3, §4`.

**Порядок:** 6.12d → 6.14a–d → 6.13a–d → 6.12e → 6.12f.

### 6.12e / 6.12f — агент RFI + gip-mcp-gateway

**6.12e** — агент RFI (автономные действия: `list_overdue`, эскалация, лог).
**6.12f** — `gip-mcp-gateway` (отдельный сервис, FastAPI-контейнер, MCP-протокол, Tools для агента RFI).

Ссылка: `ARCHITECTURE.md §7.6`, `RULES.md §12.5`, `docs/context/MASTER_PIPELINE.md §2 (шаг 6)`.

**Порядок:** 6.12e → 6.12f.

### Очередь после вехи 3 (доработка вехи 1)

Новые требования, зафиксированные в Дорожной карте 7.0
(§5.1.12–5.1.16). Реализуются **после** вехи 3 (Decision + Norm +
DecisionLink), не смешиваются с 6.11a–e.

| § | Что | Где описано |
|---|-----|-------------|
| 5.1.12 | Дашборд ГИПа (первый экран, «что горит») | Дорожная карта §5.1.12 |
| 5.1.13 | Скелет из договора (парсер → предложение структуры) | Дорожная карта §5.1.13 |
| 5.1.14 | Отчёты и недельный план (PDF/DOCX) | DOMAIN.md §2.7 + Дорожная карта §5.1.14 |
| 5.1.15 | Экспорт в MS Project XML | Дорожная карта §5.1.15 |
| 5.1.16 | Поиск по документам (полнотекстовый) | Дорожная карта §5.1.16 |

**Почему отдельно:** это сквозной пласт (UI + парсер + экспорт +
поиск), не часть модели Decision/Norm/DecisionLink. Смешивание
раздувает веху 3 и ломает ритм «одна подсессия — один коммит».

**Когда:** после 6.11e (UI вехи 3), до вехи 4 (RFI).

---

## 4. Блокеры (Blockers)

**На 22.10.2026 — блокеров нет.**

**Известные ограничения (не блокеры):**

- ⚠️ **Ветка `feat/entity-type-templates-domain`** — в паузе. Не мержить, не удалять. Решение — после пересборки дорожной карты.
- ⚠️ **GigaCode может «перебирать варианты»** — давать явные команды.
- ⚠️ **GigaCode Agent не имеет whitelist** — Auto-Approve пусто.
- ⚠️ **B027: TaskRepository.get_by_pair без @abstractmethod** — техдолг Этапа 1.
- ⚠️ **GitHub Actions** для авто-генерации DATABASE.md / API.md — не настроены.
- ⚠️ **ESLint в frontend** — не настроен (только tsc).
- ⚠️ **TestGoalPremiseIdsIntegration (test_goals_routes.py)** — fixture использует `session.begin()` → COMMIT на exit, вопреки комментарию «rollback». Данные не утекают при pytest (autouse `dispose_engine` + rollback на уровне сессии), но fixture commit — нарушение изоляции. Чинить — отдельная задача после вехи 4.
- ⚠️ **Двойная конвенция enum:** `RfiState` использует `.value` (строковые `'open'`, `'closed'`…), `GoalState` / `DecisionState` / `PremiseCategory` — `.name` (`'PLAN'`, `'CONTRACT'`). «Привести к одной (values) — после вехи 4».
- ⚠️ **N+1 в TaskRepository:** `get_by_project` / `get_by_pair` / `get_overdue` / `get_upcoming` — по одному `_fetch_premise_ids` на каждый RFI-ряд. Батчинг JOIN → batch IN — 6.12e / после вехи 4.
- ⚠️ **RfiRepository использует private-члены TaskRepository:** `_fetch_premise_ids` и `_to_domain`. При рефакторинге TaskRepository (например, вынос common logic) — проверить RfiRepository на совместимость.
- ⚠️ **6.11a: `decision_id` в домене Task и маппинге TaskRepository** —
  отклонение от спеки `spec_week_3.md §2.1` (там связь Decision → Task
  только через FK в БД, домен Task про Decision не знает). Причина:
  smoke-тест `test_tasks_decision_id` требует доменного поля.
  Решение в 6.11e: либо узаконить (Task зависит от Decision в домене),
  либо откатить (убрать из домена и маппинга, оставить только FK в БД).
- ⚠️ **API.md не полон:** до 6.11d не включал эндпоинты Actions, Results,
  ProjectStandards, Revisions (сессии 6.10d, 6.8i). В 6.11d добавлены 21
  эндпоинт вехи 3 (итого 60 + системные). Полная сверка с фактическими
  роутерами — отдельная задача.
- ⚠️ **Pre-existing дрейф типов (до 6.12a):** `project_standards.value`
  (JSON → JSONB), `result_goals.created_at` / `standard_goals.created_at`
  (TIMESTAMP → DateTime). `alembic check` подтверждает. Миграция 6.12a
  не трогала. При `alembic revision --autogenerate` в 6.12b–e — **вручную
  вычищать** этот дрейф из генерата. Отдельная задача «fix pre-existing
  type drift» — после вехи 4.
- ⚠️ **Циклические FK `actions ↔ documents` (6.12a, осознанный риск спеки §2.3):**
  `actions.result_document_id` + `documents.trigger_action_id` порождают
  SAWarning «unresolvable cycles». Autogenerate **не сравнивает** FK этих
  таблиц. При изменении FK `actions` / `documents` — **явная миграция**
  (`op.create_foreign_key` / `op.drop_constraint`), не autogenerate.
- ⚠️ **Безопасность агентов (новое, 24.10.2026):** архитектурный паттерн
  «Agent Gateway + gip-mcp-gateway + песочница + сетевые политики»
  зафиксирован в `ARCHITECTURE.md §7.6`, `DOMAIN.md §9.2.1`,
  `RULES.md §12.5`. Реализация — в вехе 4 (агент RFI).
  До реализации — агенты работают в режиме «только чтение через
  существующий API», без прямого доступа к БД и без сторонних MCP.
- ⚠️ **DATABASE.md — pre-existing дубли:** §2.17/§2.18/§2.19 (document_types, documents, document_versions — дважды), два `## 3.`. Чинить — отдельная задача «cleanup DATABASE.md» (после вехи 4).
- ⚠️ **LLM-ключи (6.14, Б1):** `api_key` — **шифрование** (Fernet, ключ `LLM_ENCRYPTION_KEY` в `.env`). В БД — `api_key_encrypted` (ciphertext), `api_key_last4` (для UI). Plaintext — только в памяти `RuntimeLLMAdapter`. `.env` — не коммитить.
- ⚠️ **Светофор (6.14, В2):** `Project.data_security_level` (enum `green`/`yellow`/`red`). `RuntimeLLMAdapter.generate(prompt, system_prompt, project_id)` — читает уровень; если `red` — `ValueError`. Regex — **не** используется.
- ⚠️ **Порядок (6.14, В3):** 6.12d → 6.14a–d → 6.12e. 6.14 — **вне** вехи 3, но **в** вехе 4 (после UI RFI, до агента RFI).
- ⚠️ **6.13a–d / 6.12f — очередь после вехи 4:** дельта-подсессии (парсинг PDF/DOCX, связывание Document↔Premise, валидация, RevisionDiffPanel) + `gip-mcp-gateway`. См. `docs/context/MASTER_PIPELINE.md`. Не начинать до закрытия 6.12d и 6.14a–d.
- ⚠️ **`RfiRead` без `description` (6.12d):** текст обоснования в карточке RFI не показывается; `rationale` виден только в предложении до утверждения. Правка backend-DTO + тестов — отдельная задача после вехи 4.
- ⚠️ **Предложения RFI не дедуплицируются (6.12d):** сервер возвращает предложение и после утверждения/эскалации; UI скрывает обработанные локально до «Обновить», после чего повторное создание возможно. Серверная дедупликация — после вехи 4.
- ⚠️ **`API.md` без расширенного раздела RFI (6.12d):** 8 RFI-эндпоинтов 6.12c детально не описаны. Документационный проход — отдельная задача.
- ⚠️ **Спека §11 vs backend 6.12c (6.12d):** спека предполагает Action «Эскалировать», backend создаёт только RFI-переход (`POST /rfis/{id}/escalate`). Согласовать спеку и реализацию — после вехи 4.
- ⚠️ **`Rfi.rfi_state` в TS non-null, DTO nullable (6.12d, m1):** у RFI-ряда значение всегда есть; fallback (ветка `null` → лейбл по умолчанию) — при расширении DTO.
- ⚠️ **`RfiForm` `useEffect` по `initialData` сбрасывает dirty-флаги (6.12d, m3):** после инвалидации `["rfis"]` открытая форма может потерять несохранённый ввод. Чинить при следующей правке формы.
- ⚠️ **`RfiPage` без `projectId` (6.12d, m5):** хуки disabled → `rfisLoading=true` навсегда вместо заглушки. Недостижимо: маршрут всегда с `:id`.
- ⚠️ **`RfiPage` create-ветка `if (!title) return` (6.12d, m6):** молчаливый no-op вместо ошибки (из формы недостижимо). Заменить при рефакторинге.
- ⚠️ **`handledProposals` не сбрасывается при смене `projectId` (6.12d, m7):** коллизий нет (ключи содержат UUID). Сброс — если появится смена проекта внутри страницы.

## 5. Журнал (Changelog)

### 27.10.2026 (сессия 6.14a — слой данных LLM)

- ✅ Домен: `LLMSettings` (только ciphertext + last4), `LLMProvider`, `DataSecurityLevel`; `Project.data_security_level`.
- ✅ Порты: `LLMProviderPort`, `SecretCipherPort`, `LLMSettingsRepository` (+`deactivate_all`).
- ✅ БД: `llm_settings` (PG enum `llm_provider`, JSONB `params`, BYTEA `api_key_encrypted`, CHECK key-pair, partial unique index) + `projects.data_security_level`.
- ✅ Миграция `65999c8dbf97`; идемпотентные `CREATE TYPE` через `DO $$`.
- ✅ `FernetCipher`, `SqlAlchemyLLMSettingsRepository`, `LLMSettingsService` (валидации, активация, `get_api_key`).
- ✅ `cryptography>=43` — прямая зависимость; `LLM_ENCRYPTION_KEY` в настройках.
- ✅ Тесты: +31 (mapping 8, cipher 7, service 11, persist 4, projects 1); pytest — 481 passed.
- ✅ По аудиту: минимум ключа 8 символов, `last4` только при длине > 4; `deactivate_all()` в persist-тесте; копия `params` в `_to_model`.

### 25.10.2026 (сессия 6.12d — UI RFI)

- ✅ `rfiApi.ts` — типы `Rfi`/`RfiCreate`/`RfiUpdate`/`RfiProposal`/`RfiProposalApprove`, словари состояний, `proposalKey`, 8 методов.
- ✅ `useRfis.ts` — 8 хуков; `useUpdateRfi` инвалидирует `["rfis", projectId]` и `["rfi", rfiId]`.
- ✅ Компоненты: `RfiCard` (просрочка по ISO-строкам, связи до 3 + «+N»), `RfiForm` (XOR причины, diff-payload на edit, `maxLength=1000`), `RfiProposalList` (create/escalate, `approving`).
- ✅ `RfiPage` — список, предложения, dialog-форма, delete, локальное скрытие обработанных предложений, `onError` у всех мутаций.
- ✅ `App.tsx` — маршрут `projects/:id/rfis`; `ProjectPage.tsx` — секция «RFI (N)» со словарём состояний.
- ✅ `npm run build` / `npm run lint` — зелёные; pytest — 450 passed.

### 25.10.2026 — docs: реорганизация документации

- ✅ `docs/README.md` — карта документации (4 уровня: Закон / Спеки / Статус / Рабочее).
- ✅ `GIGACODE.md` влит в `AGENTS.md` v1.4 (периметр данных, русский текст, три роли); `GIGACODE.md` — заглушка.
- ✅ `docs/context/AUDIT_PROMPTS.md` → `docs/tools/AUDIT_PROMPTS.md`.
- ✅ `docs/context/README.md` удалён (дубль); полезное перенесено в `docs/README.md`.
- ✅ `docs/tasks/6.12b_plan.md`, `6.12c_plan.md` → `docs/tasks/archive/`.
- ✅ `CONTEXT.md` v2.17 — сокращён (убрана история вех, ссылки на несуществующий `docs/archive/`).
- ✅ `HANDOFF.md` — актуализирован (6.12a/b/c закрыты, следующий шаг — 6.12d).
- ✅ `.gitignore` — добавлены `!docs/README.md`, `!docs/tools/**`; убраны мёртвые исключения.
- ✅ Удалён пустой артефакт `$(python` (0 байт).

### 25.10.2026 — docs: MASTER_PIPELINE (сквозной пайплайн)

- ✅ `docs/context/MASTER_PIPELINE.md` — 7 шагов (загрузка → парсинг → извлечение LLM → связывание → валидация → агент → ревизии).
- ✅ `TASKS.md §3` — 6.13a–d (дельта-подсессии), 6.12e / 6.12f (агент RFI + gip-mcp-gateway).
- ✅ `TASKS.md §4` — known issue (6.13a–d / 6.12f — очередь).

### 25.10.2026 — docs: LLM admin spec (6.14)

- ✅ `ARCHITECTURE.md §7.5` — «LLM-адаптеры и админка» (`RuntimeLLMAdapter`, Fernet, светофор).
- ✅ `DATABASE.md §2.21` — `llm_settings` (`api_key_encrypted` + `api_key_last4`).
- ✅ `RULES.md §12.5.6` — «LLM-настройки и ключи».
- ✅ `TASKS.md §3` — 6.14 (4 подсессии: 6.14a–d).
- ✅ `CONTEXT.md` — §5 (порядок: 6.12d → 6.14a–d → 6.12e) + §7 (принцип 16).

### 24.10.2026 (сессия 6.12c — RFI эндпоинты + DI)

- ✅ `routes/rfis.py` — 8 эндпоинтов: GET/POST /projects/{id}/rfis, GET/PATCH/DELETE /rfis/{id}, GET /projects/{id}/rfis/proposals, POST /projects/{id}/rfis/from-proposal, POST /rfis/{id}/escalate.
- ✅ Порядок: /proposals и /from-proposal ПЕРЕД /{id}.
- ✅ Ошибки: ValueError → 400, IntegrityError → 409, not found → 404.
- ✅ Маппинг: RfiProposalApprove.formulation → title, rationale → description.
- ✅ Регистрация: routes/__init__.py + main.py.
- ✅ 14 тестов роутов (httpx.AsyncClient + ASGITransport).
- ✅ **Итого в проекте: 450 тестов pytest.**

### 24.10.2026 — docs: agent security pattern

- ✅ ARCHITECTURE.md §7.5 — «Слой изоляции агентов (Agent Gateway + MCP)».
- ✅ DOMAIN.md §9.2.1 — «Периметр агента» (проекция данных).
- ✅ RULES.md §12.5 — «Безопасность агентов» (5 подразделов).

### 22.10.2026 (сессия 6.12a — RFI: модель + миграция + DTO + репо)

- ✅ `RfiState` enum (6 значений: open/sent/answered/registered/closed/escalated).
- ✅ TaskModel: +5 колонок (is_rfi, rfi_cause_decision_id, rfi_cause_goal_id, rfi_due_date, rfi_state) + 2 CHECK + 4 partial-индекса.
- ✅ ActionModel: +result_document_id + индекс.
- ✅ DocumentModel: +trigger_action_id + индекс.
- ✅ Domain Task: +5 полей (is_rfi, rfi_cause_*, rfi_due_date, rfi_state).
- ✅ Domain Action: +result_document_id.
- ✅ Domain Document: +trigger_action_id.
- ✅ DTO: rfi.py (RfiBase, RfiCreate, RfiUpdate, RfiRead).
- ✅ TaskRepository: _to_domain/_to_model + 5 полей + _fetch_premise_ids placeholder.
- ✅ ActionRepository: +result_document_id.
- ✅ DocumentRepository: +trigger_action_id.
- ✅ Миграция: `c0a9ff2f6038` (upgrade + downgrade OK).
- ✅ 12 тестов: test_task_rfi_mapping (5), test_action_document_mapping (4), test_rfi_repository_persist_end_to_end (3).
- ✅ **Итого в проекте: 404 теста pytest.** Ruff чисто по новым файлам.

### 22.10.2026 (сессия 6.11e — UI вехи 3)

- ✅ 4 API-клиента: decisionApi.ts (7 методов), normApi.ts (5), decisionLinkApi.ts (5), decisionNormApi.ts (4).
- ✅ 3 хука: useDecisions.ts (7 хуков), useNorms.ts (5), useDecisionLinks.ts (5).
- ✅ 7 компонентов: DecisionCard, DecisionForm, DecisionProposalList, NormCard, NormForm, DecisionLinkCard, DecisionLinkForm.
- ✅ 3 страницы: DecisionsPage (с блоком предложений), NormsPage (CRUD), DecisionLinkPage (CRUD).
- ✅ Роутинг: App.tsx (+3 маршрута), ProjectPage.tsx (секция «Решения» через useDecisions).
- ✅ `npm run build` — без ошибок.
- **Веха 3 закрыта: 6.11a → 6.11b → 6.11c → 6.11d → 6.11e.**

### 22.10.2026 (сессия 6.11d — эндпоинты вехи 3)

- ✅ 4 роутера: decisions.py (7), norms.py (5), decision_links.py (5), decision_norms.py (4).
- ✅ 21 эндпоинт: CRUD + proposals/from-proposal + связи + link/unlink.
- ✅ Ошибки: ValueError → 400, IntegrityError → 409, not found → 404.
- ✅ Порядок: /proposals и /from-proposal ПЕРЕД /{id}.
- ✅ DTO: DecisionProposalApprove (без state, по образцу GoalProposalApprove).
- ✅ API.md обновлён (v1.1): +4 раздела, 60 эндпоинтов + системные.
- ✅ 26 тестов роутов (httpx.AsyncClient + ASGITransport).
- ✅ **Итого в проекте: 392 теста pytest.** Ruff чисто. Миграций нет.

### 22.10.2026 (сессия 6.11c — сервисы вехи 3)

- ✅ 5 сервисов: DecisionService, NormService, DecisionLinkService, DecisionNormService, DecisionProposalService.
- ✅ Домен: `DecisionProposal` entity (эфемерная, uuid5-ids для UI).
- ✅ DTO: `DecisionProposal` в decision.py.
- ✅ Порт: `NormRepository.get_by_code` + реализация в SqlAlchemyNormRepository.
- ✅ DI: DecisionServiceDep, NormServiceDep, DecisionLinkServiceDep, DecisionNormServiceDep, DecisionProposalServiceDep.
- ✅ repositories/__init__.py — экспорт 4 репозиториев 6.11a/b (не были экспортированы).
- ✅ DecisionNormService — дополнение к §6 спеки (DOMAIN.md §7.2), по образцу DocumentLinkService.
- ✅ 56 unit-тестов (AsyncMock, pytest-asyncio).
- ✅ **Итого в проекте: 366 тестов pytest.** Ruff по новым файлам чисто.

### 20.10.2026 (Веха 2 — Action + Task adaptation)

- ✅ 6.10a: Action model + migration `f9eba6941cdf`. Коммит `953b558`.
- ✅ 6.10b: Task.is_complex. Коммит `f5a527d`.
- ✅ 6.10c: ActionService + TaskService + 10 тестов. Коммит `07ea2c3`.
- ✅ 6.10d: Action endpoints + 7 тестов. Коммит `ddnf57c`.
- ✅ 6.10e: Action UI (ActionsPage, ActionCard, ActionForm) + ProjectPage integration. Коммит `4b1a50d`.
- ✅ 288 passed. Веха 2 закрыта.

### 20.10.2026 (сессия 6.8f — Result + ProjectStandard)

- ✅ `ProjectStandardType` enum (deadline, composition, format).
- ✅ Domain entities: Result, ProjectStandard.
- ✅ Порты: ResultRepository, ProjectStandardRepository.
- ✅ SQLAlchemy-модели: ResultModel, ResultGoalModel, ProjectStandardModel, StandardGoalModel.
- ✅ DTO: ResultCreate/Read/Update, ProjectStandardCreate/Read/Update.
- ✅ Репозитории: SqlAlchemyResultRepository, SqlAlchemyProjectStandardRepository.
- ✅ Миграция `b8f3a1c2d9e0` (4 таблицы + enum + 4 индекса).
- ✅ 16 файлов, +643 строки. Коммит `9c98717`.
- ⏳ Alembic upgrade head (БД недоступна).

### 20.10.2026 (сессия 6.8g — ResultService + ProjectStandardService)

- ✅ ResultService — CRUD + валидация formulation.
- ✅ ProjectStandardService — CRUD + валидация existence.
- ✅ 15 unit-тестов (AsyncMock, pytest-asyncio).
- ✅ 5 файлов, +441 строки. Коммит `5e0a7c9`.
- ✅ 240 тестов pytest (225 + 15). Ruff чисто.

### 20.10.2026 (сессия 6.8i — эндпоинты Result + ProjectStandard)

- ✅ Result + ProjectStandard CRUD-эндпоинты.
- ✅ Тесты роутов (httpx.AsyncClient + ASGITransport).
- ✅ Коммит `19d37c7`.

### 20.10.2026 (сессия 6.8j-1 — UI Result + ProjectStandard)

- ✅ ResultPage, ProjectStandardPage — страницы CRUD.
- ✅ ResultCard, ProjectStandardCard — карточки.
- ✅ ResultForm, ProjectStandardForm — формы.
- ✅ ResultGoalsPanel, StandardGoalsPanel — панели связей с целями.
- ✅ API-клиенты + хуки.
- ✅ Коммит `1d57292`.

### 20.10.2026 (сессия 6.8j-2 — UI Revisions)

- ✅ RevisionsPage — страница ревизий.
- ✅ RevisionCard — карточка ревизии.
- ✅ RevisionForm — форма создания ревизии.
- ✅ RevisionDiffPanel — просмотр diff между версиями.
- ✅ API-клиенты + хуки.
- ✅ Коммит `65f943b`.

### 20.10.2026 (сессия 6.10e — UI для Action)

- ✅ `actionApi.ts` — типы + 6 API-методов.
- ✅ `useActions.ts` — 6 хуков (useActions, useAction, useActionsByTask, useCreateAction, useUpdateAction, useDeleteAction).
- ✅ `ActionCard.tsx` — карточка с state-бейджами.
- ✅ `ActionForm.tsx` — форма (formulation, measurable_result, deadline, state).
- ✅ `ActionsPage.tsx` — CRUD-страница с фильтрацией по `?task=...`.
- ✅ `App.tsx` — роут `/projects/:id/actions`.
- ✅ `ProjectPage.tsx` — секция "Действия" со счётчиком.
- ✅ Frontend build успешен. Коммит `4b1a50d`.

### 20.10.2026 (сессия 6.8f-2 — source_goal_id в Premise)

- ✅ PremiseModel: source_goal_id FK → goals, ondelete SET NULL.
- ✅ Premise entity: source_goal_id: UUID | None.
- ✅ DTO: PremiseSchema/Update/Read — source_goal_id.
- ✅ PremiseRepository: mapping _to_domain/_to_model.
- ✅ Миграция `8fc3a69b4247` (upgrade + downgrade).
- ✅ 6 файлов, +49 строк. Коммит `481e6e5`.
- ✅ 240 тестов pytest. Ruff чисто.

### 22.10.2026 (сессия 6.11b — Norm + DecisionLink + DecisionNorm)

- ✅ `NormType` enum (5 значений: gost, snip, npa, xml_schema, other).
- ✅ `DecisionLinkType` enum (3 значения: sequential, parallel, nested).
- ✅ Domain: `Norm`, `DecisionLink` entities.
- ✅ SQLAlchemy-модели: `NormModel`, `DecisionLinkModel`, `DecisionNormModel`.
- ✅ Таблицы: `norms`, `decision_links`, `decision_norms`.
- ✅ Порты: `NormRepository`, `DecisionLinkRepository`, `DecisionNormRepository`.
- ✅ Репозитории: `SqlAlchemyNormRepository`, `SqlAlchemyDecisionLinkRepository`, `SqlAlchemyDecisionNormRepository`.
- ✅ DTO: `NormBase/Create/Update/Read`, `DecisionLinkBase/Create/Read`.
- ✅ Миграция: `c52a3c176d47` (upgrade + downgrade OK).
- ✅ 12 smoke-тестов (mapping, enums, link/unlink, idempotency).
- ✅ **Итого в проекте: 310 тестов pytest.**

### 22.10.2026 (сессия 6.11a — Decision model + migration + ports + repo)

- ✅ Домен: `Decision` entity, `DecisionState` enum (5 значений).
- ✅ Модели: `DecisionModel`, `DecisionGoalModel`, `DecisionPremiseModel`.
- ✅ Таблицы: `decisions`, `decision_goals`, `decision_premises`.
- ✅ Колонка: `tasks.decision_id` (FK SET NULL) + индекс.
- ✅ Порт: `DecisionRepository`.
- ✅ Репозиторий: `SqlAlchemyDecisionRepository` (с _fetch_goal/premise_ids).
- ✅ DTO: `DecisionBase`, `DecisionCreate`, `DecisionUpdate`, `DecisionRead`.
- ✅ Миграция: `8aad8fd713f0`.
- ✅ Тесты: 10 smoke-тестов (mapping, M:N, task.decision_id).
- ✅ **Итого в проекте: 298 тестов pytest.**

### 19.10.2026 (сессия 6.8d — UI вехи 1)

- ✅ 6.8d закрыт (UI вехи 1 восстановлен).
- ✅ goalApi.ts — +3 типа DTO, +3 метода (validateGoal, getSimilarityMatrix, run3Times).
- ✅ useGoals.ts — +3 хука (useValidateGoal, useSimilarityMatrix, useRun3Times).
- ✅ PremiseCard.tsx — owner-бейджи в data.
- ✅ PremiseForm.tsx — data + schema_ textarea (JSON parsing с валидацией).
- ✅ GoalCard.tsx — verification_status бейдж + кнопка «Проверить» + evidence popup.
- ✅ GoalForm.tsx — schema_ textarea + readonly verification_status.
- ✅ SimilarityMatrixPanel.tsx — новый компонент (список связей from_section ↔ to_section).
- ✅ ProtocolSummaryPanel.tsx — новый компонент (кнопка запуска + unanimous/majority/split).
- ✅ GoalsPage.tsx — встроены блоки матрицы и протокола.
- ✅ Frontend build успешен, TypeScript — без ошибок.

- ✅ 6.8b-1: `GoalValidatorService` (правила 1–6) + `ValidationResult` + `PremiseDataField` в домене + фикс Rule 4/5. Коммиты `130c334`, `fe894d0`.
- ✅ 6.8b-2: `SimilarityMatrixService` — 10 связей. Коммит `21880b7`.
- ✅ 6.8b-3: рефактор `GoalValidatorService` → ABC + `RuleBasedGoalValidator`; `ProposalProtocolService` (unanimous/majority/split). Коммиты `964579d`, `411932f`.
- ✅ 219 passed, ruff чисто. 6.8b закрыт.
- 🔄 Переход на 6.8c (эндпоинты).

### 18.10.2026 (сессия 6.7 — онтология + спека)

- ✅ Онтология обновлена (8 вставок в DOMAIN.md, 8 в Дорожную карту 7.0).
- ✅ Создан `docs/specs/spec_week_1.md` — финальная (15 подразделов).
- ✅ Добавлены: `verification_status`, `owner`, агент-валидатор, матрица смежников, протокол 2–3 прогонов, 3 эндпоинта.
- ✅ Спека готова к кодингу. Код не начат.
- 🔄 Переход на 6.8a (модель БД).

### 16.10.2026 (веха 1d — DI + эндпоинты + тесты роутов)

- ✅ DI: `dependencies.py` — PremiseServiceDep, GoalServiceDep, GoalProposalServiceDep.
- ✅ Роуты: `premises.py` (5 эндпоинтов CRUD) + `goals.py` (7 эндпоинтов: CRUD + proposals + from-proposal).
- ✅ 17 тестов роутов: `test_premises_routes.py` (7) + `test_goals_routes.py` (10).
- ✅ httpx.AsyncClient + ASGITransport — обход проблемы FastAPI 0.143.x + TestClient.
- ✅ Все 187 тестов pytest проходят (170 старых + 17 новых).
- ✅ `AGENTS.md` обновлён: правила для тестов роутов и «не удалять тесты».
- ✅ Ветка `feat/week-1d-di-routes` запушена.

### 17.10.2026 (сессия 6.5)

- ✅ Загрузка исходников (drop zone → файл → БД).
- ✅ Канвас (React Flow): вводные, цели, связи.
- ✅ Удаление: связей, целей, вводных (с подтверждением).
- ✅ Правила вывода из вводных (4 правила).
- ✅ 187 тестов backend (зелёные).
- ✅ Frontend build успешен.
- ✅ Веха 1 закрыта.

### 17.10.2026 (сессия 6.7: fix canvas edge)

- ✅ Fix: persist premise_ids в GET/PATCH Goal (canvas edge bug).
- ✅ `goal.py` — добавлена `premise_links` relationship.
- ✅ `goal_premise.py` — добавлен `goal` back_populates.
- ✅ `goal_repository.py` — `_to_domain` без staticmethod, `_fetch_premise_ids`, `get_by_id`, `list_by_project`, `save` (перечитывание premise_ids напрямую из goal_premises).
- ✅ Alembic миграция `de7ac71d9ae0` (пустая, ORM-level relationship).
- ✅ Integration-тест `test_goal_premise_ids_persist_end_to_end` (httpx.AsyncClient + реальная БД).
- ✅ 193 теста pytest (зелёные).
- ✅ Ветка `fix/canvas-approve-refetch`.

### 18.10.2026 (сессия 6.8a — verification_status + PremiseDataField)

- ✅ `VerificationStatus(StrEnum)` — CONFIRMED, NOT_CONFIRMED, REQUIRES_CHECK, NO_DATA.
- ✅ Goal entity: поле `verification_status` (после state, default REQUIRES_CHECK).
- ✅ GoalModel: колонка + индекс `idx_goals_verification_status`.
- ✅ GoalRepository: mapping `_to_domain` / `_to_model` (с защитой от None).
- ✅ DTO: `GoalSchema` + `GoalProposal` — verification_status; `GoalUpdate` — не трогать.
- ✅ `PremiseDataField` — типизированное поле data с owner/source + field_validator (coerce plain values).
- ✅ Миграция `cd056578f798` (upgrade + downgrade).
- ✅ Тесты: test_goal_mapping.py, test_goals_routes.py — обновлены моки.
- ✅ 192 passed (1 integration test требует запущенный PostgreSQL).
- ⏳ Переход на 6.8b (сервисы).

### 18.10.2026 (сессия 6.9, шаг 1, итерация 9)

- ✅ Жёсткая структура графа: 2 корня + разделы.
- ✅ IDs детерминированы: `goal-pd`, `goal-rd`, `ar-pd`, `ar-rd`…
- ✅ Nodes и edges используют **одинаковые** IDs — линии видны.
- ✅ 10 узлов: goal-pd, goal-rd + 4×2 раздела.
- ✅ 12 связей: 4 (goal-pd→x-pd) + 4 (goal-rd→x-rd) + 4 (x-pd→x-rd).
- ✅ Парсер: regex `/^[А-ЯA-Z]{2,6}$/` — только аббревиатуры.
- ✅ Fallback: если «Разделы:» не найден → ["АР", "КР", "ВК", "ЭОМ"].

### 18.10.2026 (сессия 6.9, шаг 1, итерация 8)

- ✅ Мок-договор — чистый текст (без инструкций в коде).
- ✅ Кнопка «Мок-договор» — вставляет готовый текст в textarea.
- ✅ `data-gramm="false"` — Grammarly не мешает.
- ✅ `onPaste={() => {}}` — не блокирует Ctrl+V.
- ✅ Парсер: regex `/^[А-ЯA-Z]{2,6}$/` — только аббревиатуры.

### 18.10.2026 (сессия 6.9, шаг 1, итерация 7)

- ✅ Парсер договора: regex-извлечение ПД/РД + разделов из текста.
- ✅ Динамический граф: узлы и связи строятся из парсенных данных.
- ✅ UI: textarea с мок-текстом, кнопки «Загрузить договор» / «Построить» / «Сброс».
- ✅ Цвета: ПД — синий бейдж, РД — оранжевый бейдж.
- ✅ 369 строк (было 37).

### 18.10.2026 (сессия 6.9, шаг 1, итерация 6)

- ✅ CanvasDemoPage.tsx — минимальный граф с React Flow.
- ✅ 8 узлов: «Сдать ПД», «Сдать РД», АР/КР/ВК × ПД/РД.
- ✅ 9 связей: 6 чёрных (Сдать → АР/КР/ВК) + 3 красных пунктирных (ПД → РД).
- ✅ `GoalGraph` — чистый компонент без Layout.
- ✅ `markerEnd: MarkerType.ArrowClosed` — стрелки видны.
- ✅ `fitView` + контейнер 600px.
- ✅ Frontend build успешен.

### 17.10.2026 (сессия 6.4)

- ✅ Веха 1 — не работает end-to-end.
- Решение: не чинить — пересобрать UI.
- 19 веток — смержены, удалены.
- AGENTS.md — правило «мержить после подсессии».
- Новый UX: канвас.

### 16.10.2026 (сессия 6.1)

- ✅ Уточнение онтологии ядра.
- ✅ Второй столп: «Система знает вводные → предлагает → ГИП утверждает».
- ✅ Формула ядра: трёхэлементная (вводные + логика + механизм вывода).
- ✅ Механизм вывода двухуровневый: правила (вехи 1–5) + LLM (веха 6).
- ✅ ГИП — редактор, не «кнопка ок».
- ✅ DOMAIN.md обновлён до v1.1.
- ✅ HANDOFF.md обновлён.
- ✅ CONTEXT.md обновлён до v2.1.
- ✅ TASKS.md обновлён до v2.1.
- 🔄 Написание дорожной карты 7.0.
- 🔄 Написание дорожной карты 7.0.

### 16.10.2026 (сессия 6.0)

- ✅ Пересборка ядра продукта.
- ✅ Создан `docs/context/DOMAIN.md` v1.0 — онтология.
- ✅ Формула: вводные + логика = структура управления проектом.
- ✅ Отменены: «6 шаблонов документов», «Реестры», «вкладки как папки».
- ✅ Ветка `feat/entity-type-templates-domain` — в паузе.
- ✅ CONTEXT.md обновлён до v2.0.
- ✅ TASKS.md обновлён до v2.0.
- 🔄 Дорожная карта и ТЗ — будут пересобраны.

### 16.10.2026 (сессия 5.4e)

- ✅ Роутинг версий/связей + кнопки на форме.
- ✅ 2 маршрута в App.tsx.

### 16.10.2026 (сессия 5.4d)

- ✅ DocumentLinksPage + LinkCard + LinkForm.

### 16.10.2026 (сессия 5.4c)

- ✅ DocumentVersionsPage + VersionCard + VersionForm.

### 16.10.2026 (сессия 5.4b-3)

- ✅ Роутинг + секция «Документы» в ProjectPage.

### 16.10.2026 (сессия 5.4b-2)

- ✅ DocumentConstructorPage.

### 16.10.2026 (сессия 5.4b-1)

- ✅ DocumentsPage + DocumentCard.

### 16.10.2026 (сессия 5.4a)

- ✅ 4 API-клиента + 4 хуковых файла + enum-файл.
- ✅ 22 хука.

### 15.10.2026 (сессия 5.2f-2)

- ✅ unit-тесты DocumentVersionService + DocumentLinkService (26 тестов).
- ✅ 122 теста pytest. Уровень 1.5 backend закрыт полностью.

### 15.10.2026 (сессия 5.2f-1)

- ✅ unit-тесты DocumentTypeService + DocumentService (23 теста).
- ✅ 96 тестов pytest.

### 14.10.2026 (сессия 5.2e-3)

- ✅ Регистрация роутеров в main.py.
- ✅ 39 эндпоинтов.

### 14.10.2026 (сессия 5.2e-2)

- ✅ 4 роутера: 22 эндпоинта.

### 14.10.2026 (сессия 5.2e-1)

- ✅ DI-инфраструктура для ГОСТ-документов.

### 14.10.2026 (сессия 5.2d)

- ✅ 4 сервиса для ГОСТ-документов.

### 14.10.2026 (сессия 5.2c-2)

- ✅ 8 smoke-тестов маппинга.

### 14.10.2026 (сессия 5.2c-1)

- ✅ 4 SQLAlchemy-репозитория.

### 14.10.2026 (сессия 5.2b)

- ✅ 4 DTO-файла (13 Pydantic-классов).

### 14.10.2026 (сессия 5.2a)

- ✅ 4 порта репозиториев.

### 13.10.2026 (сессия 5.1)

- ✅ Домен + модели + миграция для ГОСТ-документов.
- ✅ 4 новые таблицы.

### 13.10.2026 (сессия 5)

- ✅ AGENTS.md: правило авто-синхронизации контекста.
- ✅ Создан HANDOFF.md.

### 12.10.2026 (сессия 4)

- ✅ Уровень 1 UI закрыт.

### 11.10.2026

- ✅ Дорожная карта 6.4 — обновлён раздел 15.
- ✅ ТЗ 4.4 — обновлены разделы 1.4, 1.5, 2.5, 2.6, 12, 15.
- ✅ `.gitignore` — исключение для `docs/context/`.
- ✅ `CONTEXT.md` — создан.

### 10.10.2026

- ✅ Уровень 1 backend: EntityType + Entity (26 тестов).

### 09.10.2026

- ✅ Уровень 1: миграция `78ada0d52056`.

### 08.10.2026

- ✅ Этап 1 закрыт.
- ✅ 39 тестов.

### 07.10.2026

- ✅ initial 7 tables (миграция f9f9bed0be0f).

## 6. Метрики проекта

| Метрика | Значение | Цель |
|---------|----------|------|
| Тесты pytest (backend) | 450 | — |
| Тесты (frontend) | 0 | — (UI сброшен) |
| Таблиц в БД | 24 (+ 3 в миграции 6.11a, + 3 в миграции 6.11b) = 27 | — |
| Эндпоинтов API | 50 | — |
| Клиентов | 0 | 1 пилот |
| MRR | 0 ₽ | 5 000 ₽ |
| `docs/context/` готовность | 9/9 файлов + `docs/README.md` | 9/9 |
| UI Уровня 1 | 100% | — |
| UI Уровня 1.5 | 100% | — |
| Портов репозиториев | 14 → 17 | — |
| Репозиториев SQLAlchemy | 13 → 16 | — |
| Сервисов | 18 | — |
| API-клиентов | 11 | — |
| Хуков TanStack Query | 53 | — |
| **DOMAIN.md** | **v1.1** | — |
| **Таблиц в БД** | **27 + 0 (колонки, не таблицы) = 27** | — |
| **React Flow страницы** | **3** (canvas-demo, timeline-demo, skeleton-demo) | — |
| **Новых сущностей (Goal/Decision/Action/Norm/RFI)** | **2** | **5** |
| **Агентов** | **0** | **5** |
| **UI вехи 3** | **100%** | — |
| **Веха 4 6.12a–d** | **ЗАКРЫТЫ** | — |

---

## 7. Как обновлять этот файл

**Правила:**

1. **Перед новым чатом с ИИ** — проверь актуальность.
2. **После завершения крупной задачи** — перенеси её из «В работе» в «Сделано».
3. **Каждый день работы** — добавь запись в «Журнал» (1-2 строки).
4. **Раз в неделю** — проверь блокеры и метрики.
5. **Не удаляй старые записи** из журнала — это история.

**Формат даты:** `DD.MM.YYYY`.

**Документация:** карта — `docs/README.md`; промпты аудита — `docs/tools/AUDIT_PROMPTS.md`; закрытые планы — `docs/tasks/archive/`.

**Порядок разделов (не меняй):**

1. Что сделано (Done)
2. В работе (In Progress)
3. Дальше (Next)
4. Блокеры (Blockers)
5. Журнал (Changelog)
6. Метрики проекта
7. Как обновлять этот файл

---

**Конец TASKS.md v2.9.**