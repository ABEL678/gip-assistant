# TASKS.md — статус проекта

> **Назначение:** что сделано / в работе / дальше. Обновляется перед каждым
> новым чатом с ИИ. Помогает понять статус проекта без пересказа.
>
> **Главный документ проекта — `DOMAIN.md`.** TASKS.md — статус.
> Если противоречие между TASKS.md и DOMAIN.md — верен DOMAIN.md.

**Версия:** 2.5
**Обновлено:** 18.10.2026
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
- ✅ `docs/context/README.md` — создан.
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

**На 22.10.2026 — Веха 3 (Decision + Norm + DecisionLink).**

- ⏳ 6.11b — модель Norm + DecisionLink + миграция + DTO + порты + репозитории.
- Код не начат.

## 3. Дальше (Next)

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
- ⏳ 6.11b — модель Norm + DecisionLink + миграция.
- ⏳ 6.11c — сервисы.
- ⏳ 6.11d — эндпоинты + DI.
- ⏳ 6.11e — UI.

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

**На 16.10.2026 — блокеров нет.**

**Известные ограничения (не блокеры):**

- ⚠️ **Ветка `feat/entity-type-templates-domain`** — в паузе. Не мержить, не удалять. Решение — после пересборки дорожной карты.
- ⚠️ **GigaCode может «перебирать варианты»** — давать явные команды.
- ⚠️ **GigaCode Agent не имеет whitelist** — Auto-Approve пусто.
- ⚠️ **B027: TaskRepository.get_by_pair без @abstractmethod** — техдолг Этапа 1.
- ⚠️ **GitHub Actions** для авто-генерации DATABASE.md / API.md — не настроены.
- ⚠️ **ESLint в frontend** — не настроен (только tsc).

---

## 4. Блокеры (Blockers)

### Известные ограничения (не блокеры)

- ⚠️ **6.11a: `decision_id` в домене Task и маппинге TaskRepository** —
  отклонение от спеки `spec_week_3.md §2.1` (там связь Decision → Task
  только через FK в БД, домен Task про Decision не знает). Причина:
  smoke-тест `test_tasks_decision_id` требует доменного поля.
  Решение в 6.11c: либо узаконить (Task зависит от Decision в домене),
  либо откатить (убрать из домена и маппинга, оставить только FK в БД).

## 5. Журнал (Changelog)

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

---

## 6. Метрики проекта

| Метрика | Значение | Цель |
|---------|----------|------|
| Тесты pytest (backend) | 298 | — |
| Тесты (frontend) | 0 | — (UI сброшен) |
| Таблиц в БД | 24 (+ 3 в миграции 6.11a) | — |
| Эндпоинтов API | 21 | — |
| Клиентов | 0 | 1 пилот |
| MRR | 0 ₽ | 5 000 ₽ |
| `docs/context/` готовность | 8/8 файлов | 8/8 |
| UI Уровня 1 | 100% | — |
| UI Уровня 1.5 | 100% | — |
| Портов репозиториев | 14 | — |
| Репозиториев SQLAlchemy | 13 | — |
| Сервисов | 13 | — |
| API-клиентов | 6 | — |
| Хуков TanStack Query | 28 | — |
| **DOMAIN.md** | **v1.1** | — |
| **React Flow страницы** | **3** (canvas-demo, timeline-demo, skeleton-demo) | — |
| **Новых сущностей (Goal/Decision/Action/Norm/RFI)** | **2** | **5** |
| **Агентов** | **0** | **5** |

---

## 7. Как обновлять этот файл

**Правила:**

1. **Перед новым чатом с ИИ** — проверь актуальность.
2. **После завершения крупной задачи** — перенеси её из «В работе» в «Сделано».
3. **Каждый день работы** — добавь запись в «Журнал» (1-2 строки).
4. **Раз в неделю** — проверь блокеры и метрики.
5. **Не удаляй старые записи** из журнала — это история.

**Формат даты:** `DD.MM.YYYY`.

**Порядок разделов (не меняй):**

1. Что сделано (Done)
2. В работе (In Progress)
3. Дальше (Next)
4. Блокеры (Blockers)
5. Журнал (Changelog)
6. Метрики проекта
7. Как обновлять этот файл

---

**Конец TASKS.md v2.5.**