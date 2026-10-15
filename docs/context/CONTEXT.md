# ГИП-Ассистент — CONTEXT

> **Назначение:** этот файл — «резюме проекта на 2 страницы». Копируй его
> в начало каждого нового чата с ИИ-ассистентом. Он даёт минимальный
> контекст, достаточный для продуктивной работы.

**Версия:** 1.3 (15.10.2026)
**Актуально на:** после 5.2e-3 (регистрация документ-роутов в main.py)
**Стек:** FastAPI + SQLAlchemy 2.0 async + PostgreSQL 15 + React 18 + TS

---

## 1. Что это за продукт

**ГИП-Ассистент** — SaaS для управления проектной разработкой в микро-студиях
и проектных институтах. Целевой пользователь — **ГИП** (главный инженер проекта).

**Ключевая идея:** мы не заставляем менять рабочий процесс. Мы встраиваемся
в существующий Excel ГИПа, превращаем его в удобный интерфейс с универсальными
сущностями и на выходе отдаём документы в XML-формате, требуемом
государственной экспертизой.

**Топ-5 болей ГИПа (из 12 интервью):**

1. Координация смежников (10/12) — матрица + задачи пары
2. Контроль просрочек (9/12) — Telegram-сводка
3. Потеря задач (8/12) — универсальные сущности
4. Согласования (7/12) — MVP-2
5. Изменения / РВИ (6/12) — MVP-2

---

## 2. Три (четыре) уровня продукта

| Уровень | Что | Этап | Статус |
|---------|-----|------|--------|
| 0 | Импорт Excel, матрица, TaskList, Telegram-бот | Прототип | ✅ Сделано |
| 1 | Универсальные сущности (EntityType + Entity) | MVP, нед. 1-2 | ✅ Backend + UI готовы |
| 1.5 | ГОСТ-хранение (Document, Version, Link, Type) | MVP-1.5 | ✅ Backend полностью готов |
| 2 | Библиотека шаблонов (6 типов) | MVP, нед. 3 | ⏳ Не начато |
| 2.5 | XML-формат ПД (ТЗ, ПЗ) + валидация XSD | MVP-1.5, 2 недели | ⏳ Не начато |
| 3 | LLM-ассистент (Qwen 2.5 7B) | MVP-3 | ⏳ Не начато |

---

## 3. Архитектура (кратко)

**Гексагональная:** domain / application / adapters.

- **Backend:** FastAPI + SQLAlchemy 2.0 async + Alembic. Домен чистый,
  не зависит от FastAPI/SQLAlchemy. Все взаимодействия — через порты
  (`domain/ports/repositories.py`).
- **Frontend:** React 18 + Vite + TypeScript + shadcn/ui + TanStack Query.
- **Bot:** aiogram 3.x.
- **Storage:** MinIO AIStor Free (S3).
- **LLM (MVP-3):** Qwen 2.5 7B локально на VPS (16 GB RAM).

**Гибридная модель данных:**

- **Системные сущности** (фиксированные): Project, Task, CrossTask, ImportLog,
  User, Executor, Document, XMLSchema, XMLDocument.
- **Пользовательские сущности** (generic): EntityType + Entity, хранятся
  в JSONB, схема динамическая.

---

## 4. Что сделано (факт)

**Backend (Этап 1 + Уровень 1 + Уровень 1.5):**

- 14 таблиц в PostgreSQL: projects, tasks, cross_tasks, task_status_history,
  executors, users, import_logs, entity_types, entities, alembic_version,
  document_types, documents, document_versions, document_links.
- Миграции Alembic: f9f9bed0be0f (initial 7 tables),
  272f011cf740 (to_section_code), 78ada0d52056 (entity_types + entities),
  d357e719c8bf (indexes + xml_schema_code), c719d9b4537e (gost document model).
- Универсальный Excel-парсер (merged cells, автопоиск шапки, serial-даты).
- 39 эндпоинтов (17 существующих + 22 для ГОСТ-документов).
- **122 теста pytest** (65 существующих + 8 для document mapping + 23 для сервисов + 26 для DocumentVersion + DocumentLink).
- Гексагональная архитектура: domain / application / adapters.
- **11 портов репозиториев** (domain/ports/repositories.py):
  Project, Task, CrossTask, ImportLog, User, EntityType, Entity,
  DocumentType, Document, DocumentVersion, DocumentLink.
- **4 DTO-файла** (application/dto/): document_type, document,
  document_version, document_link — 13 Pydantic-классов.
- **4 SQLAlchemy-репозитория** (adapters/db/repositories/):
  SqlAlchemyDocumentTypeRepository, SqlAlchemyDocumentRepository,
  SqlAlchemyDocumentVersionRepository, SqlAlchemyDocumentLinkRepository.
- **11 портов + 11 репозиториев SQLAlchemy**.
- **8 smoke-тестов маппинга** (test_document_mapping.py): Enum-маппинг,
  roundtrip, no timestamps.
- **4 сервиса** (domain/services/): DocumentTypeService, DocumentService,
  DocumentVersionService, DocumentLinkService.
- **8 сервисов** (было 4: entity_type, entity, import, matrix).
- **26 unit-тестов** (test_document_version_service.py: 15, test_document_link_service.py: 11).
- **DI-инфраструктура**: 2 __init__.py + dependencies.py — агрегация
  4 репозиториев и 4 сервисов через FastAPI Depends.
- **4 роутера** (adapters/api/routes/): document_types.py, documents.py,
  document_versions.py, document_links.py — 22 эндпоинта.
- **Регистрация в main.py**: 4 include_router (document_types, documents,
  document_versions, document_links).

**Frontend (Уровень 1 UI — ЗАКРЫТ):**

- entityApi.ts — API-клиент.
- useEntityTypes.ts, useEntities.ts — TanStack Query хуки.
- EntityTypesPage.tsx — галерея типов.
- EntityTypeConstructorPage.tsx — конструктор.
- EntitiesPage.tsx — записи типа.
- Компоненты: EntityTypeCard, FieldEditor, FieldList, DynamicField, DynamicTable, textarea.
- Интеграция в ProjectPage.tsx (секция «Типы сущностей»).
- Роутинг в App.tsx (4 маршрута).

**Bot:** aiogram 3.x, @gip_assistant_ru_bot, /start /help /link /status.

**Инфра:** Docker Compose (gip_db на 5555), Nginx-конфиг (план).

**AI-контекст и документация:**

- Дорожная карта 6.4 — обновлён раздел 15 (отказ от Cursor / Claude Code,
  GigaCode + самописный агент).
- ТЗ 4.4 — обновлены разделы 1.5, 2.5, 12, 13, 15.
- `docs/context/CONTEXT.md` — создан (этот файл).
- `AGENTS.md` — в работе.
- GigaCode — установлен и протестирован.

---

## 5. Что в работе / следующий шаг

**Сейчас (15.10.2026):**

- ✅ Уровень 1.5 backend закрыт (14–15.10.2026).
- ✅ 122 теста pytest зелёные.
- ✅ 39 эндпоинтов API.
- ✅ 8 сервисов, 11 репозиториев, 14 таблиц.

**Дальше по плану:**

- Сессия 5.4: UI DocumentsPage + DocumentVersionsPage + DocumentLinksPage.
- Сессия 5.4: UI DocumentsPage + DocumentVersionsPage + DocumentLinksPage.
- Неделя 3: Библиотека шаблонов (ИД_ПД, ИД_РД, Запросы, Тома, Письма, Протоколы) + MinIO.
- Неделя 4: Auth (JWT + Argon2) + Telegram-сводка в проде + деплой на VPS.
- Неделя 5: Лендинг (Next.js) + комплаенс 152-ФЗ + пилот.
- MVP-1.5: XML-модуль (ТЗ и ПЗ + валидация XSD).
- MVP-3: LLM-ассистент (Qwen 2.5 7B).

---

## 6. Ключевые документы

- `../Дорожная_карта_6.4.md` / `.docx` — стратегия, roadmap, риски (не коммитится).
- `../ТЗ_4.4.md` / `.docx` — архитектура, модели, API, UI (не коммитится).
- `docs/context/` — AI-контекст (**коммитится**).
  - `CONTEXT.md` — этот файл.
  - `ARCHITECTURE.md` — структура и слои.
  - `DATABASE.md` — схема БД (MVP-2: автогенерация).
  - `API.md` — эндпоинты (MVP-2: автогенерация).
  - `RULES.md` — правила кода.
  - `TASKS.md` — что сделано / в работе / дальше.
  - `README.md` — как пользоваться AI-контекстом.
  - `HANDOFF.md` — эстафета между сессиями.
- `AGENTS.md` (в корне) — правила для ИИ-агентов.

---

## 7. Ключевые принципы

1. Домен чистый (без FastAPI/SQLAlchemy).
2. Порты и адаптеры (гексагональная архитектура).
3. Универсальные сущности — ядро продукта.
4. XML — обязательное требование экспертизы.
5. AI-контекст — часть продукта.
6. ИИ-инструменты — только с поддержкой в РФ: GigaCode (PyCharm). Самописный агент — отложен.
7. Один шаг за раз, с проверками.
8. Тесты для бизнес-логики обязательны.
9. Не коммитить в main напрямую.
10. Не менять `.env` и секреты.

---

## 8. Что НЕ делать (антипаттерны)

- Не использовать Celery, Redis, RabbitMQ (MVP).
- Не использовать публичные облачные LLM.
- Не менять архитектуру без согласования.
- Не использовать `try/except` для валидации (Pydantic).
- Не добавлять новые зависимости без явного разрешения.
- Не смешивать правила кода (RULES.md) и правила текстов ПД (PROMPTS.md).
- Не коммитить в `main` напрямую (только feature-ветки + PR).

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

**Конец CONTEXT.md.**