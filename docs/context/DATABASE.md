# DATABASE.md — схема базы данных

> **Назначение:** описание всех таблиц, полей, связей и индексов.
> **Автогенерация:** в MVP-2 файл обновляется автоматически через
> `sqlacodegen` + GitHub Actions. Пока — вручную.

**Версия:** 1.2
**Обновлено:** 18.10.2026
**СУБД:** PostgreSQL 15+
**ORM:** SQLAlchemy 2.0 async
**Текущая миграция:** `8aad8fd713f0`

---

## 1. Обзор

**Всего таблиц:** 20.

| Группа | Таблицы |
|--------|---------|
| Проекты и задачи | projects, tasks, cross_tasks, task_status_history |
| Вводные и цели | premises, goals, goal_premises |
| Пользователи | users, executors |
| Импорт | import_logs |
| Универсальные сущности | entity_types, entities |
| Служебные | alembic_version |

**Всего индексов:** 43 (17 PK + 2 UNIQUE + 24 дополнительных).
Пересчитано после Сессии 5.1 (+17 индексов).
После 6.8a: +3 таблицы (premises, goals, goal_premises) и +1 индекс (idx_goals_verification_status).
После 6.11a: +3 таблицы (decisions, decision_goals, decision_premises) + колонка tasks.decision_id + enum decision_state.

**ГОСТ-документы (MVP-1.5, сессия 5.1):**

| Группа | Таблицы | Этап |
|--------|---------|------|
| Документы (ГОСТ) | document_types, documents, document_versions, document_links | ✅ Сессия 5.1 |
| Шаблоны | entity_type_templates | MVP, нед. 3 |
| XML | xml_schemas, xml_documents | MVP-1.5 |

---

## 2. Таблицы

### 2.1. projects

**Назначение:** проектная разработка (объект).

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| id | UUID | PK, default=uuid4 | ID |
| name | VARCHAR(500) | NOT NULL | Название |
| code | VARCHAR(50) | NOT NULL | Шифр проекта |
| stage | VARCHAR(10) | NOT NULL, default='PD' | Стадия (EP/PP/PD/RD) |
| client | VARCHAR(300) | nullable | Заказчик |
| contract_number | VARCHAR(100) | nullable | № договора |
| created_at | TIMESTAMPTZ | NOT NULL, default=now() | Создано |
| updated_at | TIMESTAMPTZ | NOT NULL, default=now() | Обновлено |

**Индексы:** `projects_pkey` (PK).

**FK (обратные):** от `tasks`, `cross_tasks`, `entity_types`, `entities`, `import_logs`.

### 2.2. tasks

**Назначение:** задачи проекта (участвуют в матрице смежников).

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| id | UUID | PK, default=uuid4 | ID |
| project_id | UUID | FK → projects.id (CASCADE), NOT NULL | Проект |
| title | VARCHAR(500) | NOT NULL | Название |
| description | TEXT | nullable | Описание |
| status | VARCHAR(20) | NOT NULL, default='NOT_STARTED' | Статус |
| assignee_id | UUID | FK → executors.id, nullable | Исполнитель |
| deadline | DATE | nullable | Дедлайн |
| section_code | VARCHAR(50) | nullable | Раздел-источник |
| sort_order | INT | NOT NULL, default=0 | Порядок |
| source | VARCHAR(20) | NOT NULL, default='manual' | Источник |
| created_at | TIMESTAMPTZ | NOT NULL, default=now() | Создано |
| updated_at | TIMESTAMPTZ | NOT NULL, default=now() | Обновлено |
| to_section_code | VARCHAR(50) | nullable | Раздел-получатель |
| decision_id | UUID | FK → decisions.id (SET NULL), nullable | Решение |

**Внимание:** `to_section_code` — **последняя колонка** (добавлена миграцией `272f011cf740`). `decision_id` — добавлена миграцией `8aad8fd713f0`.

**Индексы:**

- `tasks_pkey` (PK)
- `idx_tasks_project` (project_id)
- `idx_tasks_status` (status)
- `idx_tasks_deadline` (deadline)
- `idx_tasks_section` (section_code)
- `idx_tasks_to_section` (to_section_code)
- `idx_tasks_decision` (decision_id)

**FK:**

- `tasks_project_id_fkey` → projects.id (CASCADE)
- `tasks_assignee_id_fkey` → executors.id

### 2.3. cross_tasks

**Назначение:** ячейки матрицы смежников.

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| id | UUID | PK, default=uuid4 | ID |
| project_id | UUID | FK → projects.id (CASCADE), NOT NULL | Проект |
| from_section_code | VARCHAR(50) | NOT NULL | Откуда |
| to_section_code | VARCHAR(50) | NOT NULL | Куда |
| status | VARCHAR(20) | NOT NULL, default='NOT_STARTED' | Статус |
| description | TEXT | nullable | Описание |
| created_at | TIMESTAMPTZ | NOT NULL | Создано |
| updated_at | TIMESTAMPTZ | NOT NULL | Обновлено |

**Индексы:**

- `cross_tasks_pkey` (PK)
- `uq_cross_task_project_sections` (UNIQUE по project_id, from_section_code, to_section_code)

**FK:** `cross_tasks_project_id_fkey` → projects.id (CASCADE).

### 2.4. task_status_history

**Назначение:** история изменений статусов задач.

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| id | UUID | PK, default=uuid4 | ID |
| task_id | UUID | FK → tasks.id (CASCADE), NOT NULL | Задача |
| old_status | VARCHAR(20) | nullable | Старый статус |
| new_status | VARCHAR(20) | NOT NULL | Новый статус |
| changed_by | UUID | FK → users.id, nullable | Кто изменил |
| changed_at | TIMESTAMPTZ | NOT NULL, default=now() | Когда |

**Индексы:** `task_status_history_pkey` (PK).

**FK:**

- `task_status_history_task_id_fkey` → tasks.id (CASCADE)
- `task_status_history_changed_by_fkey` → users.id

### 2.5. executors

**Назначение:** исполнители (штат, подрядчики).

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| id | UUID | PK, default=uuid4 | ID |
| name | VARCHAR(300) | NOT NULL | Имя |
| type | VARCHAR(10) | NOT NULL, default='STAFF' | STAFF / CONTRACTOR |
| position | VARCHAR(200) | nullable | Должность |
| created_at | TIMESTAMPTZ | NOT NULL | Создано |

**Индексы:** `executors_pkey` (PK).

### 2.6. users

**Назначение:** пользователи системы.

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| id | UUID | PK, default=uuid4 | ID |
| name | VARCHAR(300) | NOT NULL | Имя |
| email | VARCHAR(200) | UNIQUE, nullable | Email |
| password_hash | VARCHAR(255) | nullable | Argon2-хеш |
| telegram_id | BIGINT | UNIQUE, nullable | Telegram ID |
| role | VARCHAR(10) | NOT NULL, default='DESIGNER' | GIP / DESIGNER / OBSERVER |
| is_active | BOOLEAN | NOT NULL, default=true | Активен |
| created_at | TIMESTAMPTZ | NOT NULL | Создано |

**Индексы:** `users_pkey` (PK).

### 2.7. import_logs

**Назначение:** логи импорта Excel.

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| id | UUID | PK, default=uuid4 | ID |
| project_id | UUID | FK → projects.id, NOT NULL | Проект |
| filename | VARCHAR(500) | nullable | Имя файла |
| rows_imported | INT | NOT NULL, default=0 | Строк импортировано |
| rows_failed | INT | NOT NULL, default=0 | Строк с ошибками |
| status | VARCHAR(20) | NOT NULL, default='SUCCESS' | SUCCESS / PARTIAL / FAILED |
| column_mapping | JSONB | nullable | Маппинг колонок |
| error_details | JSONB | nullable | Детали ошибок |
| imported_at | TIMESTAMPTZ | NOT NULL, default=now() | Когда |

**Индексы:**

- `import_logs_pkey` (PK)
- `idx_import_logs_project` (project_id)

**FK:** `import_logs_project_id_fkey` → projects.id.

**Особенность:** нет `created_at`/`updated_at` — вместо них `imported_at`.

### 2.8. entity_types

**Назначение:** типы универсальных сущностей (ИД, Запросы, Тома).

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| id | UUID | PK, default=uuid4 | ID |
| project_id | UUID | FK → projects.id (CASCADE), NOT NULL | Проект |
| name | VARCHAR(200) | NOT NULL | Название |
| icon | VARCHAR(50) | NOT NULL, default='📄' | Иконка |
| color | VARCHAR(20) | NOT NULL, default='gray' | Цвет |
| description | TEXT | nullable | Описание |
| schema | JSONB | NOT NULL, default='{}' | Схема полей |
| is_system | BOOLEAN | NOT NULL, default=false | Системный? |
| sort_order | INT | NOT NULL, default=0 | Порядок |
| created_at | TIMESTAMPTZ | NOT NULL | Создано |
| updated_at | TIMESTAMPTZ | NOT NULL | Обновлено |
| xml_schema_code | VARCHAR(50) | nullable | Код схемы Минстроя (PZ/TZ) |

**Внимание:** `xml_schema_code` — **последняя колонка** (добавлена миграцией `d357e719c8bf`).

**Индексы:**

- `entity_types_pkey` (PK)
- `idx_entity_types_project` (project_id)

**FK:** `entity_types_project_id_fkey` → projects.id (CASCADE).

### 2.9. entities

**Назначение:** экземпляры универсальных сущностей.

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| id | UUID | PK, default=uuid4 | ID |
| project_id | UUID | FK → projects.id (CASCADE), NOT NULL | Проект |
| entity_type_id | UUID | FK → entity_types.id (CASCADE), NOT NULL | Тип |
| data | JSONB | NOT NULL, default='{}' | Данные |
| sort_order | INT | NOT NULL, default=0 | Порядок |
| created_at | TIMESTAMPTZ | NOT NULL | Создано |
| updated_at | TIMESTAMPTZ | NOT NULL | Обновлено |

**Индексы:**

- `entities_pkey` (PK)
- `idx_entities_project` (project_id)
- `idx_entities_type` (entity_type_id)
- `idx_entities_data_gin` (GIN по data) — **для поиска по JSONB**

**FK:**

- `entities_project_id_fkey` → projects.id (CASCADE)
- `entities_entity_type_id_fkey` → entity_types.id (CASCADE)

### 2.10. premises

**Назначение:** вводные проекта (договор, ТЗ, требования, ИД, нормы, НПА, бюрократия, внутренние).

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| id | UUID | PK, default=uuid4 | ID |
| project_id | UUID | FK → projects.id (CASCADE), NOT NULL | Проект |
| category | ENUM(premise_category) | NOT NULL | Категория |
| name | VARCHAR(500) | NOT NULL | Название |
| source | VARCHAR(500) | nullable | Откуда пришла |
| date | DATE | nullable | Вступила в силу |
| actual | BOOLEAN | NOT NULL, default=true | Актуальна |
| mandatory | BOOLEAN | NOT NULL, default=true | Обязательна |
| link | VARCHAR(1000) | nullable | Ссылка на источник |
| valid_until | DATE | nullable | Срок действия |
| data | JSONB | NOT NULL, default='{}' | Типизированные поля |
| schema | JSONB | NOT NULL, default='{}' | Схема полей |
| created_at | TIMESTAMPTZ | NOT NULL, default=now() | Создано |
| updated_at | TIMESTAMPTZ | NOT NULL, default=now() | Обновлено |

**Индексы:**

- `premises_pkey` (PK)
- `idx_premises_project` (project_id)
- `idx_premises_category` (category)
- `idx_premises_actual` (actual)

**FK:** `premises_project_id_fkey` → projects.id (CASCADE).

### 2.11. goals

**Назначение:** цели управления проектом (выводятся из вводных).

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| id | UUID | PK, default=uuid4 | ID |
| project_id | UUID | FK → projects.id (CASCADE), NOT NULL | Проект |
| formulation | VARCHAR(1000) | NOT NULL | Формулировка |
| deadline | DATE | nullable | Срок |
| responsible_id | UUID | FK → users.id (SET NULL), nullable | Ответственный |
| priority | INT | nullable | Приоритет (1–5) |
| state | ENUM(goal_state) | NOT NULL, default='plan' | Состояние |
| verification_status | ENUM(verification_status) | NOT NULL, default='requires_check' | Статус проверки |
| created_by | UUID | FK → users.id (SET NULL), nullable | Кто создал |
| created_at | TIMESTAMPTZ | NOT NULL, default=now() | Создано |
| updated_at | TIMESTAMPTZ | NOT NULL, default=now() | Обновлено |

**Индексы:**

- `goals_pkey` (PK)
- `idx_goals_project` (project_id)
- `idx_goals_state` (state)
- `idx_goals_deadline` (deadline)
- `idx_goals_verification_status` (verification_status)

**FK:** projects (CASCADE), users (SET NULL).

### 2.12. goal_premises

**Назначение:** связь Goal ↔ Premise (M:N).

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| goal_id | UUID | PK, FK → goals.id (CASCADE) | Цель |
| premise_id | UUID | PK, FK → premises.id (CASCADE) | Вводная |
| created_at | TIMESTAMPTZ | NOT NULL, default=now() | Создано |

**Индексы:** `goal_premises_pkey` (PK, composite: goal_id, premise_id).

**FK:**

- `goal_premises_goal_id_fkey` → goals.id (CASCADE)
- `goal_premises_premise_id_fkey` → premises.id (CASCADE)

### 2.13. alembic_version

**Назначение:** служебная таблица Alembic.

| Поле | Тип | Ограничения |
|------|-----|-------------|
| version_num | VARCHAR(32) | PK |

**Текущая версия:** `8aad8fd713f0` (add decisions + decision_goals + decision_premises + tasks.decision_id).

### 2.14. decisions

**Назначение:** решения управления проектом.

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| id | UUID | PK, default=uuid4 | ID |
| project_id | UUID | FK → projects.id (CASCADE), NOT NULL | Проект |
| formulation | VARCHAR(500) | NOT NULL | Формулировка |
| rationale | TEXT | nullable | Обоснование |
| context | TEXT | nullable | Контекст |
| deadline | DATE | nullable | Срок |
| state | ENUM(decision_state) | NOT NULL, default='plan' | Состояние |
| created_by | UUID | FK → users.id (SET NULL), nullable | Кто создал |
| created_at | TIMESTAMPTZ | NOT NULL, default=now() | Создано |
| updated_at | TIMESTAMPTZ | NOT NULL, default=now() | Обновлено |

**Индексы:**

- `decisions_pkey` (PK)
- `idx_decisions_project` (project_id)
- `idx_decisions_state` (state)
- `idx_decisions_deadline` (deadline)

**FK:** projects (CASCADE), users (SET NULL).

### 2.15. decision_goals

**Назначение:** связь Decision ↔ Goal (M:N).

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| decision_id | UUID | PK, FK → decisions.id (CASCADE) | Решение |
| goal_id | UUID | PK, FK → goals.id (CASCADE) | Цель |
| created_at | TIMESTAMPTZ | NOT NULL, default=now() | Создано |

**Индексы:** `decision_goals_pkey` (PK, composite), `idx_decision_goals_decision`, `idx_decision_goals_goal`.

### 2.16. decision_premises

**Назначение:** связь Decision ↔ Premise (M:N).

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| decision_id | UUID | PK, FK → decisions.id (CASCADE) | Решение |
| premise_id | UUID | PK, FK → premises.id (CASCADE) | Вводная |
| created_at | TIMESTAMPTZ | NOT NULL, default=now() | Создано |

**Индексы:** `decision_premises_pkey` (PK, composite), `idx_decision_premises_decision`, `idx_decision_premises_premise`.

### 2.14. document_types

**Назначение:** справочник типов ГОСТ-документов.

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| id | UUID | PK, default=uuid4 | ID |
| code | VARCHAR(50) | NOT NULL, UNIQUE | Код типа (drawing, scheme, ...) |
| name | VARCHAR(200) | NOT NULL | Название |
| description | TEXT | nullable | Описание |
| gost_code | VARCHAR(50) | nullable | Код по ГОСТ (ПЗ, ТЗ, УЛ) |
| created_at | TIMESTAMPTZ | NOT NULL, default=now() | Создано |

**Индексы:** `document_types_pkey` (PK), `uq_document_types_code` (UNIQUE).

### 2.15. documents

**Назначение:** карточка ГОСТ-документа (ГОСТ Р 21.101-2026).

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| id | UUID | PK, default=uuid4 | ID |
| guid | UUID | NOT NULL, UNIQUE | GUID документа (ГОСТ Р 21.101-2026, 4.1.2.2) |
| project_id | UUID | FK → projects.id (CASCADE), NOT NULL | Проект |
| entity_id | UUID | FK → entities.id (SET NULL), nullable | Сущность |
| task_id | UUID | FK → tasks.id (SET NULL), nullable | Задача |
| cipher | VARCHAR(500) | NOT NULL | Обозначение (АБЗ-XXX-XX ЭД) |
| base_designation | VARCHAR(200) | nullable | Базовое обозначение |
| section_code | VARCHAR(50) | nullable | Код раздела |
| document_kind | VARCHAR(10) | NOT NULL, default='ПД' | ПД / РД |
| mark | VARCHAR(50) | nullable | Марка |
| doc_part_type | VARCHAR(10) | nullable | ТЧ / ГЧ |
| document_name | VARCHAR(500) | NOT NULL | Наименование |
| document_type_id | UUID | FK → document_types.id, NOT NULL | Тип |
| current_version_id | UUID | nullable, НЕ FK | Текущая версия |
| version_parent_id | UUID | FK → documents.id, nullable | Родитель |
| replaces_id | UUID | FK → documents.id, nullable | Заменяемый |
| replaced_by_id | UUID | FK → documents.id, nullable | Заменяющий |
| lifecycle_status | VARCHAR(20) | NOT NULL, default='DRAFT' | Статус |
| signed_by | UUID | FK → users.id, nullable | Кто подписал |
| signed_at | TIMESTAMPTZ | nullable | Когда подписал |
| signature_hash | VARCHAR(255) | nullable | Хеш ЭП |
| signature_status | VARCHAR(50) | nullable | Статус ЭП |
| created_by | UUID | FK → users.id, nullable | Кто создал |
| created_at | TIMESTAMPTZ | NOT NULL, default=now() | Создано |
| updated_at | TIMESTAMPTZ | NOT NULL, default=now() | Обновлено |

**Индексы:** `documents_pkey` (PK), `uq_documents_guid` (UNIQUE), `idx_documents_project`, `idx_documents_entity`, `idx_documents_task`, `idx_documents_type`, `idx_documents_status`.

**FK:** projects, entities (SET NULL), tasks (SET NULL), document_types, documents (само-рекурсия), users.

### 2.16. document_versions

**Назначение:** версия файла ГОСТ-документа.

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| id | UUID | PK, default=uuid4 | ID |
| document_id | UUID | FK → documents.id (CASCADE), NOT NULL | Документ |
| version | VARCHAR(20) | NOT NULL | Номер версии (v1.0, v1.1) |
| change_number | INT | nullable | Номер изменения |
| file_path | VARCHAR(1000) | NOT NULL | Путь к файлу |
| file_name | VARCHAR(500) | NOT NULL | Имя файла |
| hash_sha256 | VARCHAR(64) | NOT NULL | Хеш SHA-256 |
| format_original | VARCHAR(20) | NOT NULL | Формат (dwg, docx, pdf) |
| format_archive | VARCHAR(20) | nullable | Архивный формат |
| size_bytes | BIGINT | NOT NULL | Размер в байтах |
| is_current | BOOLEAN | NOT NULL, default=False | Текущая версия |
| uploaded_by | UUID | FK → users.id, nullable | Загрузил |
| uploaded_at | TIMESTAMPTZ | NOT NULL, default=now() | Загружено |

**Ограничения:** UniqueConstraint(document_id, version).

**Индексы:** `document_versions_pkey` (PK), `idx_document_versions_document`, `idx_document_versions_current` (partial: WHERE is_current = TRUE).

### 2.17. document_links

**Назначение:** связь между ГОСТ-документами.

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| id | UUID | PK, default=uuid4 | ID |
| source_document_id | UUID | FK → documents.id (CASCADE), NOT NULL | Источник |
| target_document_id | UUID | FK → documents.id (CASCADE), NOT NULL | Цель |
| link_type | VARCHAR(30) | NOT NULL, default='reference' | Тип связи |
| created_at | TIMESTAMPTZ | NOT NULL, default=now() | Создано |

**Ограничения:** UniqueConstraint(source_document_id, target_document_id, link_type).

**Индексы:** `document_links_pkey` (PK), `idx_document_links_source`, `idx_document_links_target`.

---

## 3. Enum'ы (значения)

| Enum | Значения | Где используется |
|------|----------|------------------|
| StageType | EP, PP, PD, RD | projects.stage |
| TaskStatus | NOT_STARTED, IN_PROGRESS, REVIEW, REWORK, DONE, CANCELLED | tasks.status |
| CrossTaskStatus | NOT_STARTED, IN_PROGRESS, WAITING_INFO, DONE, OVERDUE | cross_tasks.status |
| ExecutorType | STAFF, CONTRACTOR | executors.type |
| UserRole | GIP, DESIGNER, OBSERVER | users.role |
| ImportStatus | SUCCESS, PARTIAL, FAILED | import_logs.status |
| PremiseCategory | contract, tz, customer_requirement, source_data, norm, npa, bureaucracy, internal | premises.category |
| GoalState | plan, in_progress, achieved, cancelled | goals.state |
| DecisionState | plan, in_progress, accepted, cancelled, replaced | decisions.state |
| VerificationStatus | confirmed, not_confirmed, requires_check, no_data | goals.verification_status |
| XMLDocumentStatus | DRAFT, GENERATED, VALIDATED, INVALID, EXPORTED | xml_documents (план) |
| DocumentKind | ПД, РД | домен (value_objects/document.py) |
| DocPartType | ТЧ, ГЧ | домен (value_objects/document.py) |
| LifecycleStatus | DRAFT, IN_REVIEW, NORMOCONTROL, APPROVED, ARCHIVED, ANNULLED, REPLACED | домен (value_objects/document.py) |
| DocumentLinkType | appendix, reference, replaces, version_of | домен (value_objects/document.py) |

---

## 4. Миграции Alembic

**Текущая цепочка:**

| Rev | Описание | Дата |
|-----|----------|------|
| `f9f9bed0be0f` | initial: 7 tables | 2026-10-07 |
| `272f011cf740` | add to_section_code to tasks | 2026-10-08 |
| `78ada0d52056` | add entity_types and entities tables | 2026-10-10 |
| `d357e719c8bf` | add indexes and xml_schema_code | 2026-10-11 |
| `c719d9b4537e` | add gost document model | 2026-10-13 |
| `de7ac71d9ae0` | goal_premise_links_relationship | 2026-10-17 |
| `686491cea3fd` | add_premises_and_goals | 2026-10-16 |
| `cd056578f798` | add verification_status to goals | 2026-10-18 |
| `8aad8fd713f0` | add decisions + decision_goals + decision_premises + tasks.decision_id | 2026-10-22 |

**Команды:**

    cd /d C:\Users\abelo\GIP-Assistant\gip-assistant\backend
    alembic current
    alembic upgrade head
    alembic downgrade -1
    alembic revision --autogenerate -m "описание"

**Правила:**

1. Alembic запускается **из `backend/`**, не из корня.
2. `alembic.ini` — в `backend/alembic.ini`.
3. Все миграции — с осмысленным сообщением.

---

## 5. Подключение к БД

**Локально (Docker Compose):**

- Хост: `localhost`
- Порт: `5555` (gip_db)
- БД: `gip_assistant`
- Пользователь: `gip`

**DATABASE_URL (`.env`):**

    DATABASE_URL=postgresql+asyncpg://gip:<пароль>@localhost:5555/gip_assistant

**Команды:**

    docker start gip_db
    docker exec -it gip_db psql -U gip -d gip_assistant -c "\dt"
    docker exec -it gip_db psql -U gip -d gip_assistant -c "\di"
    docker exec -it gip_db psql -U gip -d gip_assistant -c "\d+ tasks"

---

## 6. Автогенерация (MVP-2)

**План:** GitHub Actions обновляет `DATABASE.md` при изменении моделей.

**Триггер:** изменение `backend/src/adapters/db/models/**`.

**Инструмент:** `sqlacodegen`.

**Workflow:** `.github/workflows/sync-ai-context.yml`.

**Статус:** пока не реализовано. В MVP — вручную.

---

**Конец DATABASE.md.**