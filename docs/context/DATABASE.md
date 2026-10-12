# DATABASE.md — схема базы данных

> **Назначение:** описание всех таблиц, полей, связей и индексов.
> **Автогенерация:** в MVP-2 файл обновляется автоматически через
> `sqlacodegen` + GitHub Actions. Пока — вручную.

**Версия:** 1.1
**Обновлено:** 11.10.2026
**СУБД:** PostgreSQL 15+
**ORM:** SQLAlchemy 2.0 async
**Текущая миграция:** `d357e719c8bf`

---

## 1. Обзор

**Всего таблиц:** 10.

| Группа | Таблицы |
|--------|---------|
| Проекты и задачи | projects, tasks, cross_tasks, task_status_history |
| Пользователи | users, executors |
| Импорт | import_logs |
| Универсальные сущности | entity_types, entities |
| Служебные | alembic_version |

**Всего индексов:** 21 (10 PK + 1 UNIQUE + 10 дополнительных).

**Планируются:**

| Группа | Таблицы | Этап |
|--------|---------|------|
| Документы (ГОСТ) | document_types, documents, document_versions, document_links | MVP, нед. 3 |
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

**Внимание:** `to_section_code` — **последняя колонка** (добавлена миграцией `272f011cf740`).

**Индексы:**

- `tasks_pkey` (PK)
- `idx_tasks_project` (project_id)
- `idx_tasks_status` (status)
- `idx_tasks_deadline` (deadline)
- `idx_tasks_section` (section_code)
- `idx_tasks_to_section` (to_section_code)

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

### 2.10. alembic_version

**Назначение:** служебная таблица Alembic.

| Поле | Тип | Ограничения |
|------|-----|-------------|
| version_num | VARCHAR(32) | PK |

**Текущая версия:** `d357e719c8bf` (add indexes and xml_schema_code).

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
| DocumentStatus | UPLOADING, READY, FAILED | documents (план) |
| XMLDocumentStatus | DRAFT, GENERATED, VALIDATED, INVALID, EXPORTED | xml_documents (план) |

---

## 4. Миграции Alembic

**Текущая цепочка:**

| Rev | Описание | Дата |
|-----|----------|------|
| `f9f9bed0be0f` | initial: 7 tables | 2026-10-07 |
| `272f011cf740` | add to_section_code to tasks | 2026-10-08 |
| `78ada0d52056` | add entity_types and entities tables | 2026-10-10 |
| `d357e719c8bf` | add indexes and xml_schema_code | 2026-10-11 |

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