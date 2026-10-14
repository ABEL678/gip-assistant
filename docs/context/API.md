# API.md — список эндпоинтов

> **Назначение:** все HTTP-эндпоинты ГИП-Ассистента.
> **Автогенерация:** в MVP-2 файл обновляется автоматически из OpenAPI
> (`/openapi.json`). Пока — вручную.

**Версия:** 1.0
**Обновлено:** 11.10.2026
**Base URL:** `http://localhost:8000`
**Документация:** `http://localhost:8000/api/docs` (Swagger UI)

---

## 1. Обзор

**Всего эндпоинтов:** 39 + системные.

**Группы:**

| Группа | Кол-во | Префикс |
|--------|--------|---------|
| Projects | 4 | `/api/projects` |
| Tasks | 4 | `/api/tasks`, `/api/projects/{id}/tasks` |
| Matrix | 5 | `/api/projects/{id}/matrix`, `/api/cross-tasks` |
| Import | 3 | `/api/projects/{id}/import-*` |
| EntityTypes | 5 | `/api/projects/{id}/entity-types`, `/api/entity-types` |
| Entities | 5 | `/api/entity-types/{id}/entities`, `/api/entities` |
| DocumentTypes | 6 | `/api/document-types` |
| Documents | 6 | `/api/projects/{id}/documents`, `/api/documents` |
| DocumentVersions | 6 | `/api/documents/{id}/versions`, `/api/document-versions` |
| DocumentLinks | 4 | `/api/documents/{id}/links`, `/api/document-links` |
| System | 3 | `/api/health`, `/api/version`, `/api/ai/ping` |

---

## 2. Projects

### GET /api/projects

**Описание:** список всех проектов.

**Query параметры:**
- `limit` (int, default=100) — максимум записей.
- `offset` (int, default=0) — смещение.

**Ответ 200:**
    [
      {
        "id": "uuid",
        "name": "Объект X",
        "code": "P-001",
        "stage": "PD",
        "client": "Заказчик",
        "contract_number": "Д-001",
        "created_at": "2026-10-11T...",
        "updated_at": "2026-10-11T..."
      }
    ]

### POST /api/projects

**Описание:** создать проект.

**Body:**
    {
      "name": "Объект X",
      "code": "P-001",
      "stage": "PD",
      "client": "Заказчик",
      "contract_number": "Д-001"
    }

**Ответ 201:** созданный проект (см. GET).

### GET /api/projects/{project_id}

**Описание:** проект по ID.

**Ответ 200:** проект.

**Ошибка 404:** проект не найден.

### PATCH /api/projects/{project_id}

**Описание:** обновить проект.

**Body:** любое подмножество полей.

**Ответ 200:** обновлённый проект.

---

## 3. Tasks

### GET /api/projects/{project_id}/tasks

**Описание:** список задач проекта.

**Query:**
- `limit` (int, default=500).
- `offset` (int, default=0).

**Ответ 200:**
    [
      {
        "id": "uuid",
        "project_id": "uuid",
        "title": "Разработка ОВ",
        "description": "...",
        "status": "IN_PROGRESS",
        "assignee_id": "uuid | null",
        "deadline": "2026-10-20",
        "section_code": "АР",
        "to_section_code": "ОВ",
        "sort_order": 0,
        "source": "manual",
        "created_at": "...",
        "updated_at": "..."
      }
    ]

### GET /api/tasks/{task_id}

**Описание:** задача по ID.

**Ответ 200:** задача.

**Ошибка 404:** не найдена.

### PATCH /api/tasks/{task_id}

**Описание:** inline-редактирование задачи.

**Body:** любое подмножество полей (например, `{"status": "DONE"}`).

**Ответ 200:** обновлённая задача.

### GET /api/cross-tasks/{cross_task_id}/tasks

**Описание:** все задачи пары разделов (ячейки матрицы).

**Ответ 200:**
    [
      {
        "id": "uuid",
        "title": "...",
        "status": "IN_PROGRESS",
        "overdue_days": 5,
        "days_until_deadline": -5,
        ...
      }
    ]

---

## 4. Matrix

### GET /api/projects/{project_id}/matrix

**Описание:** матрица смежников проекта.

**Ответ 200:**
    {
      "sections": ["АР", "КР", "ОВ", "ВК"],
      "cells": [
        {
          "id": "uuid",
          "from_section_code": "АР",
          "to_section_code": "ОВ",
          "status": "IN_PROGRESS",
          "description": "Задач: 5, просрочено: 2, готово: 1"
        }
      ]
    }

### POST /api/projects/{project_id}/matrix/generate

**Описание:** автогенерация матрицы на основе задач.

**Ответ 200:**
    {
      "created": 14,
      "updated": 0
    }

### GET /api/cross-tasks/{cross_task_id}

**Описание:** ячейка матрицы по ID.

**Ответ 200:** cross_task.

**Ошибка 404:** не найдена.

### PATCH /api/cross-tasks/{cross_task_id}

**Описание:** обновить ячейку (статус, описание).

**Body:** `{"status": "DONE", "description": "..."}`.

**Ответ 200:** обновлённая ячейка.

---

## 5. Import (Excel)

### POST /api/projects/{project_id}/import-excel

**Описание:** загрузить Excel, получить preview + suggested_mapping.

**Content-Type:** `multipart/form-data`.

**Body:**
- `file` (file, обязательный).
- `header_row` (int, опциональный) — номер строки-шапки.

**Ответ 200:**
    {
      "import_log_id": "uuid",
      "filename": "реестр.xlsx",
      "header_row": 3,
      "columns": ["Наименование", "Раздел", "Срок", ...],
      "preview_rows_raw": [[...], [...]],
      "suggested_mapping": {
        "title": "Наименование",
        "section_code": "Раздел",
        "deadline": "Срок"
      }
    }

### GET /api/projects/{project_id}/import-logs

**Описание:** история импортов.

**Ответ 200:**
    [
      {
        "id": "uuid",
        "filename": "реестр.xlsx",
        "rows_imported": 585,
        "rows_failed": 0,
        "status": "SUCCESS",
        "column_mapping": {...},
        "imported_at": "2026-10-10T..."
      }
    ]

### POST /api/projects/{project_id}/import-confirm

**Описание:** подтвердить маппинг, создать задачи.

**Body:**
    {
      "import_log_id": "uuid",
      "column_mapping": {
        "title": "Наименование",
        "section_code": "Раздел",
        "to_section_code": "Кому",
        "deadline": "Срок",
        "description": "Описание"
      }
    }

**Ответ 200:** `{"imported": 585, "failed": 0}`.

---

## 6. EntityTypes

### POST /api/projects/{project_id}/entity-types

**Описание:** создать тип сущности.

**Body:**
    {
      "name": "Исходные данные",
      "icon": "📄",
      "color": "blue",
      "description": "...",
      "schema": {
        "fields": [
          {"key": "title", "label": "Наименование", "type": "text", "required": true},
          {"key": "status", "label": "Статус", "type": "select", "options": ["Да", "Нет"]}
        ]
      },
      "xml_schema_code": "PZ",
      "sort_order": 0
    }

**Ответ 201:** созданный тип.

### GET /api/projects/{project_id}/entity-types

**Описание:** список типов проекта.

**Ответ 200:** `[EntityType, ...]`.

### GET /api/entity-types/{entity_type_id}

**Описание:** тип по ID.

**Ответ 200:** тип.

**Ошибка 404:** не найден.

### PATCH /api/entity-types/{entity_type_id}

**Описание:** обновить тип.

**Body:** любое подмножество полей.

**Ответ 200:** обновлённый тип.

### DELETE /api/entity-types/{entity_type_id}

**Описание:** удалить тип (только пользовательский, `is_system=false`).

**Ответ 204:** пусто.

**Ошибка 400:** попытка удалить системный тип.

---

## 7. Entities

### POST /api/entity-types/{entity_type_id}/entities

**Описание:** создать запись в типе.

**Body:**
    {
      "project_id": "uuid",
      "data": {"title": "ТУ на водоснабжение", "status": "Да"},
      "sort_order": 0
    }

**Ответ 201:** созданная запись.

**Ошибка 400:** обязательные поля не заполнены.

### GET /api/entity-types/{entity_type_id}/entities

**Описание:** список записей типа.

**Ответ 200:** `[Entity, ...]`.

### GET /api/entities/{entity_id}

**Описание:** запись по ID.

**Ответ 200:** запись.

### PATCH /api/entities/{entity_id}

**Описание:** обновить запись.

**Body:** `{"data": {...}, "sort_order": 0}`.

**Ответ 200:** обновлённая запись.

### DELETE /api/entities/{entity_id}

**Описание:** удалить запись.

**Ответ 204:** пусто.

---

## 8. Document Types

### POST /api/document-types

**Описание:** создать тип ГОСТ-документа.

**Body:**
    {
      "code": "EXT",
      "name": "Внешний документ",
      "description": "Описание",
      "gost_code": "ГОСТ Р 1234-2024"
    }

**Ответ 201:** созданный тип.

### GET /api/document-types

**Описание:** список типов ГОСТ-документов.

**Ответ 200:** `[DocumentType, ...]`.

### GET /api/document-types/by-code/{code}

**Описание:** тип ГОСТ-документа по коду.

**Ответ 200:** тип.

**Ошибка 404:** тип с таким кодом не найден.

### GET /api/document-types/{document_type_id}

**Описание:** тип ГОСТ-документа по ID.

**Ответ 200:** тип.

**Ошибка 404:** не найден.

### PATCH /api/document-types/{document_type_id}

**Описание:** обновить тип ГОСТ-документа.

**Body:** любое подмножество полей (`name`, `description`, `gost_code`).

**Ответ 200:** обновлённый тип.

### DELETE /api/document-types/{document_type_id}

**Описание:** удалить тип ГОСТ-документа.

**Ответ 204:** пусто.

**Ошибка 404:** не найден.

---

## 9. Documents

### POST /api/projects/{project_id}/documents

**Описание:** создать ГОСТ-документ в проекте.

**Body:**
    {
      "document_type_id": "uuid",
      "document_name": "ПЗ",
      "cipher": "1234-2024",
      "document_kind": "PD",
      "doc_part_type": "TEXT",
      "section_code": "ПЗ",
      "mark": "Лист 1",
      "base_designation": "АБВГ.1234567.890-24",
      "entity_id": "uuid | null",
      "task_id": "uuid | null",
      "lifecycle_status": "DRAFT",
      "version_parent_id": "uuid | null",
      "replaces_id": "uuid | null",
      "replaced_by_id": "uuid | null"
    }

**Ответ 201:** созданный документ.

**Ошибка 400:** тип документа не найден.

### GET /api/projects/{project_id}/documents

**Описание:** список документов проекта.

**Query параметры:**
- `lifecycle_status` (LifecycleStatus | null) — фильтр по статусу.

**Ответ 200:** `[Document, ...]`.

### GET /api/documents/by-guid/{guid}

**Описание:** ГОСТ-документ по GUID.

**Ответ 200:** документ.

**Ошибка 404:** не найден.

### GET /api/documents/{document_id}

**Описание:** ГОСТ-документ по ID.

**Ответ 200:** документ.

**Ошибка 404:** не найден.

### PATCH /api/documents/{document_id}

**Описание:** обновить ГОСТ-документ.

**Body:** любое подмножество полей (`document_name`, `document_kind`, `doc_part_type`, `section_code`, `mark`, `base_designation`, `lifecycle_status`).

**Ответ 200:** обновлённый документ.

### DELETE /api/documents/{document_id}

**Описание:** удалить ГОСТ-документ.

**Ответ 204:** пусто.

**Ошибка 404:** не найден.

---

## 10. Document Versions

### POST /api/documents/{document_id}/versions

**Описание:** создать версию ГОСТ-документа.

**Body:**
    {
      "version": "1.0",
      "file_path": "/storage/docs/123.pdf",
      "file_name": "ПЗ.pdf",
      "hash_sha256": "abc123...",
      "format_original": "pdf",
      "size_bytes": 1048576,
      "change_number": 1,
      "format_archive": "zip"
    }

**Ответ 201:** созданная версия.

**Ошибка 400:** документ не найден.

### GET /api/documents/{document_id}/versions/current

**Описание:** текущая версия ГОСТ-документа.

**Ответ 200:** версия.

**Ошибка 404:** текущая версия не найдена.

### GET /api/documents/{document_id}/versions

**Описание:** список версий ГОСТ-документа.

**Ответ 200:** `[DocumentVersion, ...]`.

### GET /api/document-versions/{version_id}

**Описание:** версия ГОСТ-документа по ID.

**Ответ 200:** версия.

**Ошибка 404:** не найдена.

### PATCH /api/documents/{document_id}/versions/{version_id}/set-current

**Описание:** сделать версию текущей.

**Ответ 204:** пусто.

**Ошибка 400:** документ/версия не найдены, или версия не принадлежит документу.

### DELETE /api/document-versions/{version_id}

**Описание:** удалить версию ГОСТ-документа.

**Ответ 204:** пусто.

**Ошибка 404:** не найдена.

---

## 11. Document Links

### POST /api/documents/{document_id}/links

**Описание:** создать связь ГОСТ-документов.

**Body:**
    {
      "target_document_id": "uuid",
      "link_type": "REFERENCES"
    }

**Ответ 201:** созданная связь.

**Ошибка 400:** само-связь, документы не найдены, или из разных проектов.

### GET /api/documents/{document_id}/links

**Описание:** исходящие связи ГОСТ-документа.

**Ответ 200:** `[DocumentLink, ...]`.

### GET /api/documents/{document_id}/links/incoming

**Описание:** входящие связи ГОСТ-документа.

**Ответ 200:** `[DocumentLink, ...]`.

### DELETE /api/document-links/{link_id}

**Описание:** удалить связь ГОСТ-документов.

**Ответ 204:** пусто.

**Ошибка 404:** не найдена.

---

## 12. System

### GET /api/health

**Описание:** health-check.

**Ответ 200:**
    {"status": "ok", "app": "gip-assistant", "env": "dev"}

### GET /api/version

**Описание:** версия API.

**Ответ 200:**
    {"version": "0.1.0", "stage": "skeleton"}

### GET /api/ai/ping

**Описание:** проверка AI-порта (заглушка).

**Ответ 200:**
    {"ai_stub_response": "..."}

---

## 9. Коды ошибок

| Код | Когда | Тело |
|-----|-------|------|
| 200 | Успех (GET/PATCH) | объект/список |
| 201 | Создано (POST) | объект |
| 204 | Удалено (DELETE) | пусто |
| 400 | Bad Request | `{"detail": "..."}` |
| 404 | Not Found | `{"detail": "... not found"}` |
| 422 | Validation Error | `{"detail": [{...}]}` — от Pydantic |
| 500 | Internal Server Error | `{"detail": "Internal Server Error"}` |

**Валидация:**
- **422** — Pydantic (неверный формат тела, отсутствуют обязательные поля).
- **400** — доменные правила (например, «Тип сущности принадлежит другому проекту»).
- **404** — не найдено.

---

## 10. Аутентификация

**В MVP:** пока нет.

**В MVP (нед. 4):**
- JWT + Argon2.
- Регистрация / логин / logout.
- `Authorization: Bearer <token>`.
- Изоляция данных по `user_id`.
- Роли: ГИП / Дизайнер / Наблюдатель.

**Сейчас все эндпоинты — публичные.**

---

## 13. Эндпоинты в планах

### MVP (нед. 3) — Шаблоны
- GET `/api/entity-type-templates`
- GET `/api/entity-type-templates/{code}`
- POST `/api/projects/{id}/entity-types/from-template/{code}`

### MVP-1.5 — XML
- GET `/api/xml-schemas`
- GET `/api/xml-schemas/{code}`
- POST `/api/xml-schemas/sync`
- POST `/api/projects/{id}/xml-export`
- GET `/api/xml-documents/{id}`
- GET `/api/xml-documents/{id}/download`
- DELETE `/api/xml-documents/{id}`

---

## 12. Автогенерация (MVP-2)

**План:** GitHub Actions обновляет `API.md` из OpenAPI-схемы.

**Триггер:** изменение `backend/src/adapters/api/routes/**`.

**Инструмент:** `curl /openapi.json` + конвертация в Markdown.

**Workflow:** `.github/workflows/sync-ai-context.yml`.

**Статус:** пока не реализовано.

---

**Конец API.md.**