# TASKS.md — статус проекта

> **Назначение:** что сделано / в работе / дальше. Обновляется перед каждым
> новым чатом с ИИ. Помогает понять статус проекта без пересказа.

**Версия:** 1.0
**Обновлено:** 11.10.2026
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

---

## 2. В работе (In Progress)

### Уровень 1.5 (ГОСТ-хранение) — Сессия 5.1

- ⏳ Домен: Document, DocumentVersion, DocumentLink, DocumentType.
- ⏳ Value Objects: 4 Enum (DocumentKind, DocPartType, LifecycleStatus, DocumentLinkType).
- ⏳ SQLAlchemy-модели: 4 таблицы.
- ⏳ Миграция Alembic + сиды document_types.
- ⏳ Проверка: 65 старых тестов зелёные.
- ⏳ Обновление DATABASE.md.

### GigaCode (установлен и протестирован)

- ✅ Плагин установлен в PyCharm (Marketplace + Sber ID).
- ✅ Project Context → `docs/context/` подключён.
- ✅ `AGENTS.md` подключён через Rules (apply: always, mode: all).
- ✅ Auto-Approve — пусто (безопасно).
- ✅ Протестирован на 5 сценариях:
  - Ask → чтение `docs/context/CONTEXT.md`.
  - Plan → составление плана для эндпоинта.
  - Agent → создание файла `__init__.py`.
  - Agent → запуск `pytest` (сам активировал `.venv`).
  - Agent → запуск `alembic current` (с явной командой).

**Вывод:** GigaCode заменяет 80% запланированного самописного агента.

### Самописный ИИ-агент (отложен)

- ❌ Не пишем в MVP. Экономия 1-2 дня.
- ⏳ Вернуться, если через 2-4 недели появится задача, которую GigaCode не решает.
- ⏳ Потенциальные задачи: whitelist команд, Plan Mode с обязательным approve, специфичные Alembic-манипуляции.

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

**На 12.10.2026 — блокеров нет.**

Все запланированные задачи по инфраструктуре выполнены:
- ✅ AI-контекст (`docs/context/` — 7 файлов).
- ✅ `AGENTS.md` (в корне).
- ✅ GigaCode установлен и протестирован.
- ✅ Дорожная карта 6.4, ТЗ 4.4.
- ✅ Уровень 1 (MVP) backend + UI закрыт.
- ✅ 65 тестов pytest.

**Следующие шаги:** Неделя 3 MVP — Библиотека шаблонов + MinIO.

### Известные ограничения (не блокеры)

- ⚠️ **GigaCode может «перебирать варианты»** — если задача сформулирована двусмысленно. **Решение:** давать явные команды (см. `AGENTS.md`, секция «Готовые команды»).
- ⚠️ **`.gigacode/plans/` создаёт временные файлы** — игнорируются через `.gitignore`.
- ⚠️ **GigaCode Agent не имеет whitelist** — но Auto-Approve пусто, каждое действие требует approve.

---

## 5. Журнал (Changelog)

Краткая история — что делали по датам.

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
| Тесты pytest | 65 | 84 (MVP), 107 (MVP-1.5) |
| Таблиц в БД | 10 | 14 (MVP-1.5) |
| Эндпоинтов API | 17 | 30+ (MVP) |
| Покрытие бизнес-логики | Smoke-тесты | 80%+ |
| Клиентов | 0 | 1 пилот |
| MRR | 0 ₽ | 5 000 ₽ (первый платёж) |
| `docs/context/` готовность | 7/7 файлов | 7/7 |
| UI Уровня 1 | 100% | 100% |

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