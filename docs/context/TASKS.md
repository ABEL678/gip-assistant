# TASKS.md — статус проекта

> **Назначение:** что сделано / в работе / дальше. Обновляется перед каждым
> новым чатом с ИИ. Помогает понять статус проекта без пересказа.
>
> **Главный документ проекта — `DOMAIN.md`.** TASKS.md — статус.
> Если противоречие между TASKS.md и DOMAIN.md — верен DOMAIN.md.

**Версия:** 2.3
**Обновлено:** 17.10.2026
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

## 2. В работе (In Progress)

**На 18.10.2026:**

- 🔄 Сессия 6.9: минимальный граф целей (React Flow, 8 узлов, 9 связей).

## 3. Дальше (Next)

### Ось времени (план-график)

- ⏳ Ось времени — план-график.
- ⏳ Просрочки — красным.
- ⏳ Критический путь — жирным.

### Веха 2 — Action + Task-адаптация

- ⏳ Action как сущность.
- ⏳ Адаптация Task/CrossTask.

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

## 5. Журнал (Changelog)

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
| Тесты pytest (backend) | 193 | — |
| Тесты (frontend) | 0 | — (UI сброшен) |
| Таблиц в БД | 17 | — |
| Эндпоинтов API | 51 | — |
| Клиентов | 0 | 1 пилот |
| MRR | 0 ₽ | 5 000 ₽ |
| `docs/context/` готовность | 8/8 файлов | 8/8 |
| UI Уровня 1 | 100% | — |
| UI Уровня 1.5 | 100% | — |
| Портов репозиториев | 11 | — |
| Репозиториев SQLAlchemy | 11 | — |
| Сервисов | 8 | — |
| API-клиентов | 5 | — |
| Хуков TanStack Query | 22 | — |
| **DOMAIN.md** | **v1.1** | — |
| **React Flow страницы** | **3** (canvas-demo, timeline-demo, skeleton-demo) | — |
| **Новых сущностей (Goal/Decision/Action/Norm/RFI)** | **0** | **5** |
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

**Конец TASKS.md v2.3.**