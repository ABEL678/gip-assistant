# TASKS.md — статус проекта

> **Назначение:** что сделано / в работе / дальше. Обновляется перед каждым
> новым чатом с ИИ. Помогает понять статус проекта без пересказа.

**Версия:** 1.3
**Обновлено:** 15.10.2026
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
- ✅ Импорт Excel (dropzone + селектор шапки + маппинг).
- ✅ TaskList (500+ задач, фильтры, inline).
- ✅ Матрица смежников (10×10, 14 ячеек, цвета, смена статуса).
- ✅ Страница задач пары (группировка).

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
- ✅ Порты репозиториев (EntityTypeRepository, EntityRepository) в
  domain/ports/repositories.py.
- ✅ Репозитории (SqlAlchemy*) — в стиле проекта (save через merge).
- ✅ Сервисы: EntityTypeService, EntityService (валидация JSONB по схеме).
- ✅ API: 10 эндпоинтов (`POST/GET/PATCH/DELETE` для типов и записей).
- ✅ DI: EntityTypeServiceDep, EntityServiceDep в dependencies.py.
- ✅ 26 unit-тестов pytest (все зелёные).
- ✅ **Итого в проекте: 65 тестов pytest**.

### AI-контекст и документация (октябрь 2026)

- ✅ Дорожная карта 6.4 — готова.
- ✅ ТЗ 4.4 — готово.
- ✅ `.gitignore` обновлён (исключение `!docs/context/`).
- ✅ `docs/context/CONTEXT.md` — создан.
- ✅ `docs/context/ARCHITECTURE.md` — создан.
- ✅ `docs/context/DATABASE.md` — создан (10 таблиц, 21 индекс).
- ✅ `docs/context/API.md` — создан (17 эндпоинтов).
- ✅ `docs/context/RULES.md` — создан.
- ✅ `docs/context/TASKS.md` — создан (этот файл).
- ✅ `docs/context/README.md` — создан.
- ✅ `AGENTS.md` — создан (в корне).
- ✅ GigaCode — установлен и протестирован.

  **GigaCode:**
  - ✅ Плагин установлен в PyCharm (Marketplace + Sber ID).
  - ✅ Project Context → `docs/context/` подключён.
  - ✅ `AGENTS.md` подключён через Rules (apply: always, mode: all).
  - ✅ Auto-Approve — пусто (безопасно).
  - ✅ Протестирован на 5 сценариях: Ask (CONTEXT.md), Plan (эндпоинт),
    Agent (создание `__init__.py`), Agent (запуск pytest с активацией `.venv`),
    Agent (запуск alembic current).
  - ✅ Вывод: GigaCode заменяет 80% запланированного самописного агента.

  **Самописный ИИ-агент (отложен):**
  - ❌ Не пишем в MVP. Экономия 1-2 дня.
  - ⏳ Вернуться, если через 2-4 недели появится задача, которую
       GigaCode не решает.
  - ⏳ Потенциальные задачи: whitelist команд, Plan Mode с обязательным
       approve, специфичные Alembic-манипуляции.

### Уровень 1 (MVP): UI конструктора типов — ЗАКРЫТ (12.10.2026)

- ✅ entityApi.ts — API-клиент для EntityType + Entity.
- ✅ useEntityTypes.ts, useEntities.ts — TanStack Query хуки.
- ✅ EntityTypeCard.tsx — карточка типа (галерея).
- ✅ FieldEditor.tsx — редактор поля.
- ✅ FieldList.tsx — список полей.
- ✅ EntityTypesPage.tsx — галерея типов.
- ✅ EntityTypeConstructorPage.tsx — конструктор типа.
- ✅ DynamicField.tsx — рендер поля по типу.
- ✅ DynamicTable.tsx — универсальная таблица.
- ✅ EntitiesPage.tsx — записи типа.
- ✅ textarea.tsx (shadcn/ui).
- ✅ Интеграция в ProjectPage.tsx — секция «Типы сущностей» + empty state.
- ✅ Роутинг в App.tsx (4 маршрута).
- ✅ TypeScript — без ошибок.

### Сессия 5.4a (Frontend API-клиенты и хуки для ГОСТ-документов) — ЗАКРЫТ (16.10.2026)

- ✅ documentEnums.ts — 4 enum-типа (DocumentKind, DocPartType, LifecycleStatus, DocumentLinkType).
- ✅ documentTypesApi.ts — 6 методов API.
- ✅ documentsApi.ts — 6 методов API.
- ✅ documentVersionsApi.ts — 6 методов API.
- ✅ documentLinksApi.ts — 4 метода API.
- ✅ useDocumentTypes.ts — 6 хуков.
- ✅ useDocuments.ts — 6 хуков.
- ✅ useDocumentVersions.ts — 6 хуков.
- ✅ useDocumentLinks.ts — 4 хука.
- ✅ TypeScript — без ошибок.
- ✅ **Итого в проекте: 22 хука, 5 API-клиентов.**

### Сессия 5.4b-1 (Frontend DocumentsPage + DocumentCard) — ЗАКРЫТ (16.10.2026)

- ✅ DocumentCard.tsx — карточка документа (название, шифр, тип, статус, вид, секция/марка).
- ✅ DocumentsPage.tsx — страница списка документов (фильтр по lifecycle_status, grid, empty/error/loading states).
- ✅ TypeScript — без ошибок.
- ✅ **Итого в проекте: 22 хука, 5 API-клиентов, 2 новых UI-файла.**

### Уровень 1.5 (ГОСТ-хранение) — ��АКРЫТ (14–15.10.2026)

**Сессия 5.1 (домен + модели):**
- ✅ Домен: Document, DocumentVersion, DocumentLink, DocumentType.
- ✅ Value Objects: 4 Enum (DocumentKind, DocPartType, LifecycleStatus, DocumentLinkType).
- ✅ SQLAlchemy-модели: 4 таблицы.
- ✅ Миграция Alembic c719d9b4537e + сиды document_types (8 записей).
- ✅ Обновление DATABASE.md.

**Сессия 5.2a (порты):**
- ✅ 4 порта репозиториев в domain/ports/repositories.py.
- ✅ Итого портов: 11 (было 7).

**Сессия 5.2b (DTO):**
- ✅ 4 DTO-файла: document_type, document, document_version, document_link.
- ✅ 13 Pydantic-классов (Base/Create/Update/Read).

**Сессия 5.2c-1 (репозитории):**
- ✅ 4 SQLAlchemy-репозитория.
- ✅ Enum-маппинг: конструктор при чтении, .value при записи.
- ✅ set_current: два UPDATE в одной транзакции.
- ✅ Итого репозиториев: 11 (было 7).

**Сессия 5.2c-2 (smoke-тесты маппинга):**
- ✅ 8 smoke-тестов: test_document_mapping.py.
- ✅ Итого тестов pytest: 73 (было 65).

**Сессия 5.2d (сервисы):**
- ✅ 4 сервиса: DocumentType, Document, DocumentVersion, DocumentLink.
- ✅ Валидации: уникальность кода, existence checks, self-link, same project.
- ✅ set_current: 3 валидации + денормализация current_version_id.
- ✅ Итого сервисов: 8 (было 4).

**Сессия 5.2e-1 (DI):**
- ✅ 2 __init__.py + dependencies.py: 4 репо + 4 сервиса.
- ✅ DocumentServiceDep, DocumentVersionServiceDep, DocumentLinkServiceDep.

**Сессия 5.2e-2 (роуты):**
- ✅ 4 роутера: document_types, documents, document_versions, document_links.
- ✅ 22 эндпоинта (6 + 6 + 6 + 4).
- ✅ Порядок эндпоинтов: /by-code ПЕРЕД /{id}, /by-guid ПЕРЕД /{id},
   /versions/current ПЕРЕД /versions.
- ✅ Роуты через ServiceDep (НЕ RepoDep напрямую).
- ✅ PATCH: payload.model_dump(exclude_unset=True, by_alias=False).

**Сессия 5.2e-3 (регистрация):**
- ✅ Регистрация роутеров в main.py (4 include_router).
- ✅ Обновлён routes/__init__.py (+4 импорта).
- ✅ Обновлён docs/context/API.md (+22 эндпоинта).
- ✅ Итого эндпоинтов: 39 (было 17).

**Сессия 5.2f-1 (unit-тесты сервисов, часть 1):**
- ✅ test_document_type_service.py (10 тестов).
- ✅ test_document_service.py (13 тестов).
- ✅ Стиль: AsyncMock, pytest-asyncio, фикстуры.
- ✅ Итого тестов pytest: 96 (было 73).

**Сессия 5.2f-2 (unit-тесты сервисов, часть 2):**
- ✅ test_document_version_service.py (15 тестов).
- ✅ test_document_link_service.py (11 тестов).
- ✅ Стиль: AsyncMock, pytest-asyncio, фикстуры.
- ✅ Итого тестов pytest: 122 (было 96).

---

## 2. В работе (In Progress)

**На 16.10.2026 — задач в работе нет. Сессия 5.4b-1 закрыта.**

---

## 3. Дальше (Next)

### Неделя 3 MVP: Библиотека шаблонов + MinIO

- ⏳ Таблица `entity_type_templates`.
- ⏳ 6 шаблонов: ИД_ПД, ИД_РД, Запросы, Тома, Письма, Протоколы.
- ⏳ Endpoint `GET /api/entity-type-templates`.
- ⏳ Endpoint `POST /api/projects/{id}/entity-types/from-template/{code}`.
- ⏳ UI: `TemplateGallery.tsx`.
- ⏳ Развёртывание MinIO AIStor Free в Docker.
- ⏳ Модель `Document` (метаданные).
- ⏳ API: upload / download / list / delete.
- ⏳ UI: `FileUploader.tsx`, `DocumentList.tsx`.

### Неделя 4 MVP: Auth + Telegram + Деплой

- ⏳ Аутентификация: JWT + Argon2.
- ⏳ Регистрация / логин / logout.
- ⏳ Middleware `current_user`.
- ⏳ Роли: ГИП / Дизайнер / Наблюдатель.
- ⏳ UI: `LoginPage.tsx`, `AuthGuard.tsx`.
- ⏳ Telegram-сводка в проде (digest_worker + cron 09:00).
- ⏳ Привязка Telegram к user (/link).
- ⏳ Деплой на VPS (Timeweb / Aeza / FirstVDS).
- ⏳ Nginx + SSL (Let's Encrypt).
- ⏳ Домен gip-assistant.ru.
- ⏳ GitHub Actions CI (lint + test).

### Неделя 5 MVP: Лендинг + Комплаенс + Пилот

- ⏳ Лендинг Next.js 14.
- ⏳ Форма заявки + чекбокс 152-ФЗ.
- ⏳ Комплаенс 152-ФЗ (уведомление Роскомнадзора, политика).
- ⏳ Пилот (7 дней бесплатно, онбординг-звонок, первый платёж).

### MVP-1.5: XML-формат ПД (2 недели)

- ⏳ Модель `XMLSchema` + таблица `xml_schemas`.
- ⏳ Модель `XMLDocument` + таблица `xml_documents`.
- ⏳ Порт `XMLPort` + адаптер `lxml_adapter.py`.
- ⏳ `SchemaService` (скачивание схем с Минстроя, кэш, обновление).
- ⏳ `XMLService` (генерация, валидация по XSD).
- ⏳ API: `/api/xml-schemas`, `/api/projects/{id}/xml-export`, `/api/xml-documents/{id}`.
- ⏳ UI: `XMLDocumentsPage.tsx`, `XMLExportWizard.tsx`.
- ⏳ 23 новых теста (XMLService, SchemaService, XSD-валидация).

### MVP-2: Расширение (4 недели)

- ⏳ Модуль согласований (РСО, МЧС, экспертиза).
- ⏳ Модуль изменений (РВИ).
- ⏳ Тома — % готовности + итерации.
- ⏳ Финансы — договоры, авансы, остатки.
- ⏳ Дашборд для руководства.
- ⏳ Мультипроектность.
- ⏳ Background-агенты для документации (BugBot, Context-keeper).

### MVP-3: LLM-ассистент (5 недель)

- ⏳ Qwen 2.5 7B локально на VPS (16 GB RAM).
- ⏳ pgvector для эмбеддингов.
- ⏳ RAG по документам проекта.
- ⏳ Генерация писем, отчётов, ТЗ.
- ⏳ Извлечение задач из протоколов.
- ⏳ Чат с проектом.
- ⏳ Sub-агенты: XML-validator, Test-writer, Doc-keeper, Migration-checker.

---

## 4. Блокеры (Blockers)

**На 15.10.2026 — блокеров нет.**

Все запланированные задачи по инфраструктуре выполнены:
- ✅ AI-контекст (docs/context/ — 7 файлов).
- ✅ AGENTS.md (в корне).
- ✅ GigaCode установлен и протестирован.
- ✅ Дорожная карта 6.4, ТЗ 4.4.
- ✅ Уровень 1 (MVP) backend + UI закрыт.
- ✅ 96 тестов pytest.

**Следующие шаги:** Сессия 5.2f-2 (тесты DocumentVersion + DocumentLink).

### Известные ограничения (не блокеры)

- ⚠️ **GigaCode может «перебирать варианты»** — если задача сформулирована двусмысленно. **Решение:** давать явные команды (см. `AGENTS.md`, секция «Готовые команды»).
- ⚠️ **`.gigacode/plans/` создаёт временные файлы** — игнорируются через `.gitignore`.
- ⚠️ **GigaCode Agent не имеет whitelist** — но Auto-Approve пусто, каждое действие требует approve.
- ⚠️ **B027: TaskRepository.get_by_pair без @abstractmethod** — ruff B027.
  Технический долг Этапа 1 (не связан с ГОСТ-моделями). Починить отдельным
  коммитом при случае (одна строка — @abstractmethod над методом).

---

## 5. Журнал (Changelog)

Краткая история — что делали по датам.

### 16.10.2026 (сессия 5.4b-1)

- ✅ Сессия 5.4b-1 закрыта: DocumentsPage + DocumentCard.
- ✅ 2 UI-файла: DocumentCard.tsx, DocumentsPage.tsx.
- ✅ Фильтр по lifecycle_status, grid карточек, empty/error/loading states.
- ✅ TypeScript: без ошибок.

### 16.10.2026 (сессия 5.4a)

- ✅ Сессия 5.4a закрыта: 4 API-клиента + 1 enum-файл + 4 хуковых файла.
- ✅ 22 хука (6 + 6 + 6 + 4): useDocumentTypes, useDocuments, useDocumentVersions, useDocumentLinks.
- ✅ 5 API-клиентов (entityApi + 4 ГОСТ-клиента).
- ✅ TypeScript: без ошибок.

### 15.10.2026 (сессия 5.2f-2)

- ✅ Сессия 5.2f-2 закрыта: unit-тесты DocumentVersionService + DocumentLinkService.
- ✅ 26 тестов (15 + 11): create, get, list, set_current, delete.
- ✅ Стиль: AsyncMock, pytest-asyncio, фикстуры.
- ✅ 122 теста pytest (было 96).
- ✅ Уровень 1.5 backend закрыт полностью.

### 15.10.2026 (сессия 5.2f-1)

- ✅ Сессия 5.2f-1 закрыта: unit-тесты DocumentTypeService + DocumentService.
- ✅ 23 теста (10 + 13): create, get, list, update, delete.
- ✅ Стиль: AsyncMock, pytest-asyncio, фикстуры.
- ✅ 96 тестов pytest (было 73).

### 14.10.2026 (сессия 5.2e-3)

- ✅ Сессия 5.2e-3 закрыта: регистрация роутеров в main.py.
- ✅ 4 include_router (document_types, documents, document_versions, document_links).
- ✅ Обновлён API.md (+22 эндпоинта).
- ✅ 39 эндпоинтов (было 17).

### 14.10.2026 (сессия 5.2e-2)

- ✅ Сессия 5.2e-2 закрыта: 4 роутера для ГОСТ-документов.
- ✅ 22 эндпоинта (6+6+6+4) с правильным порядком для FastAPI.
- ✅ PATCH: `payload.model_dump(exclude_unset=True, by_alias=False)`.
- ✅ 73 теста pytest.

### 14.10.2026 (сессия 5.2e-1)

- ✅ Сессия 5.2e-1 закрыта: DI-инфраструктура для ГОСТ-документов.
- ✅ 2 __init__.py + dependencies.py: 4 репо + 4 сервиса.

### 14.10.2026 (сессия 5.2d)

- ✅ Сессия 5.2d закрыта: 4 сервиса для ГОСТ-документов.
- ✅ Валидации: уникальность кода, existence checks, self-link, same project.
- ✅ set_current: 3 валидации + денормализация current_version_id.
- ✅ 8 сервисов (было 4).

### 14.10.2026 (сессия 5.2c-2)

- ✅ Сессия 5.2c-2 закрыта: 8 smoke-тестов маппинга документов.
- ✅ Покрытие: Enum-маппинг, roundtrip, no timestamps.
- ✅ 73 теста pytest.

### 14.10.2026 (сессия 5.2c-1)

- ✅ Сессия 5.2c-1 закрыта: 4 SQLAlchemy-репозитория для ГОСТ-документов.
- ✅ Enum-маппинг: конструктор при чтении, .value при записи.
- ✅ set_current: два UPDATE в одной транзакции.
- ✅ 65 тестов зелёные.

### 14.10.2026 (сессия 5.2b)

- ✅ Сессия 5.2b закрыта: 4 DTO-файла для ГОСТ-документов.
- ✅ 13 Pydantic-классов: DocumentType, Document, DocumentVersion, DocumentLink.
- ✅ 65 тестов зелёные.

### 14.10.2026 (сессия 5.2a)

- ✅ Сессия 5.2a закрыта: 4 порта репозиториев для ГОСТ-документов.
- ✅ DocumentTypeRepository, DocumentRepository, DocumentVersionRepository,
  DocumentLinkRepository — ABC-классы в domain/ports/repositories.py.
- ✅ Domain чистый, 65 тестов зелёные.
- ✅ Итого портов: 11.

### 13.10.2026 (сессия 5.1)

- ✅ Сессия 5.1 закрыта: домен + модели + миграция для ГОСТ-документов.
- ✅ 4 новые таблицы: document_types, documents, document_versions, document_links.
- ✅ 8 сидов document_types.
- ✅ Обновлены TASKS.md, DATABASE.md.
- ✅ 65 тестов зелёные.

### 13.10.2026 (сессия 5)

- ✅ Обновлён AGENTS.md: правило авто-синхронизации контекста.
- ✅ Создан HANDOFF.md — механизм передачи между сессиями.
- ✅ Обновлено правило про HANDOFF (по запросу человека, не автоматом).
- ⏸ Пауза до Сессии 5.1 (Уровень 1.5 — домен + модели).

### 12.10.2026 (сессия 4)

- ✅ Уровень 1 UI закрыт: 12 файлов (entityApi, хуки, страницы, компоненты).
- ✅ Интеграция в ProjectPage.tsx: секция «Типы сущностей».
- ✅ TypeScript: без ошибок.
- ✅ Все залиты на GitHub.

### 11.10.2026

- ✅ Дорожная карта 6.4 — обновлён раздел 15 (GigaCode + самописный агент).
- ✅ ТЗ 4.4 — обновлены разделы 1.4, 1.5, 2.5, 2.6, 12, 15.
- ✅ `.gitignore` — исключение для `docs/context/`.
- ✅ `CONTEXT.md` — создан, закоммичен на GitHub.
- 🔄 `TASKS.md` — создаётся (этот файл).

### 10.10.2026

- ✅ Уровень 1 backend: EntityType + Entity (26 тестов).
- ✅ Коммит 71de995: universal entities.
- ✅ Обновление `docs/context/CONTEXT.md` (v1.1).
- ✅ Раздел 15 в Дорожной карте (Части 1 и 2).

### 09.10.2026

- ✅ Уровень 1: миграция `78ada0d52056` (entity_types + entities).
- ✅ Репозитории, сервисы, API.
- ✅ Первые тесты (26).

### 08.10.2026

- ✅ Этап 1 закрыт.
- ✅ 39 тестов.

### 07.10.2026

- ✅ initial 7 tables (миграция f9f9bed0be0f).

---

## 6. Метрики проекта

| Метрика | Значение | Цель |
|---------|----------|------|
| Тесты pytest | 122 | 84 (MVP), 107 (MVP-1.5) |
| Таблиц в БД | 14 | 14 (MVP-1.5) |
| Эндпоинтов API | 39 | 30+ (MVP) |
| Покрытие бизнес-логики | Smoke-тесты | 80%+ |
| Клиентов | 0 | 1 пилот |
| MRR | 0 ₽ | 5 000 ₽ (первый платёж) |
| `docs/context/` готовность | 7/7 файлов | 7/7 |
| UI Уровня 1 | 100% | 100% |
| Портов репозиториев | 11 | 11 |
| Репозиториев SQLAlchemy | 11 | 11 |
| Сервисов | 8 | 8 |
| API-клиентов | 5 | 5 |
| Хуков TanStack Query | 22 | 22 |

---

## 7. Как обновлять этот файл

**Правила:**

1. **Перед новым чатом с ИИ** — проверь актуальность.
2. **После завершения крупной задачи** — перенеси её из «В работе» в «Сделано».
3. **Каждый день работы** — добавь запись в «Журнал» (1-2 строки).
4. **Раз в неделю** — проверь блокеры и метрики.
5. **Не удаляй старые записи** из журнала — это история.

**Формат даты:** `DD.MM.YYYY` (например, 12.10.2026).

**Порядок разделов (не меняй):**

1. Что сделано (Done)
2. В работе (In Progress)
3. Дальше (Next)
4. Блокеры (Blockers)
5. Журнал (Changelog)
6. Метрики проекта
7. Как обновлять этот файл

---

**Конец TASKS.md.**
