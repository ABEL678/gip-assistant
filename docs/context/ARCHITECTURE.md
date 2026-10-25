# ARCHITECTURE.md — архитектура ГИП-Ассистента

> **Назначение:** описание структуры проекта, слоёв, стека и правил.
> Для ИИ-агентов: что где лежит, куда класть новый код, что нельзя нарушать.

**Версия:** 1.1
**Обновлено:** 25.10.2026

---

## 1. Общая картина

**Гексагональная архитектура** (порты и адаптеры):

    ┌─────────────────────────────────────────────────────────┐
    │                    Adapters (внешний мир)                │
    │  HTTP (FastAPI) │ БД (SQLAlchemy) │ S3 (MinIO) │ Telegram│
    └──────────────────────────┬──────────────────────────────┘
                               ↓ (зависит от ↓)
    ┌─────────────────────────────────────────────────────────┐
    │              Application (use cases, DTO)                │
    └──────────────────────────┬──────────────────────────────┘
                               ↓ (зависит от ↓)
    ┌─────────────────────────────────────────────────────────┐
    │         Domain (сущности, порты, сервисы)                │
    │         Не зависит НИ ОТ ЧЕГО внешнего!                  │
    └─────────────────────────────────────────────────────────┘

**Правило:** зависимости идут **внутрь** (адаптеры → application → domain).
Домен **не знает** про FastAPI, SQLAlchemy, HTTP.

---

## 2. Слои Backend

### 2.1. Domain (`backend/src/domain/`)

**Что:** бизнес-логика, сущности, интерфейсы портов.

**Зависимости:** только `stdlib` + `typing` + `dataclasses`.

**Что нельзя:** импортировать FastAPI, SQLAlchemy, Pydantic, asyncpg.

**Структура:**

    domain/
    ├── entities/           # Dataclass-сущности
    │   ├── project.py
    │   ├── task.py
    │   ├── cross_task.py
    │   ├── entity_type.py
    │   ├── entity.py
    │   ├── document.py 
    │   ├── document_version.py
    │   ├── document_link.py
    │   ├── document_type.py
    │   ├── xml_schema.py
    │   ├── xml_document.py
    │   └── ...
    ├── value_objects/      # Enum'ы, VO
    │   └── enums.py
    ├── ports/              # ABC-интерфейсы
    │   ├── repositories.py # Репозитории (TaskRepository, ...)
    │   ├── ai_port.py      # AI-порт (заглушка)
    │   └── storage_port.py # S3-порт (MinIO)
    └── services/           # Доменные сервисы
        ├── matrix_service.py
        ├── import_service.py
        ├── entity_type_service.py
        └── entity_service.py

**Пример домена:**

    # domain/entities/entity_type.py
    from dataclasses import dataclass, field
    from datetime import datetime
    from typing import Any
    from uuid import UUID, uuid4

    @dataclass
    class EntityType:
        project_id: UUID
        name: str
        icon: str = "📄"
        field_schema: dict[str, Any] = field(default_factory=dict)
        xml_schema_code: str | None = None
        id: UUID = field(default_factory=uuid4)
        created_at: datetime | None = None
        updated_at: datetime | None = None

### 2.2. Application (`backend/src/application/`)

**Что:** use cases, DTO (Pydantic-схемы).

**Зависимости:** Domain, Pydantic.

**Структура:**

    application/
    ├── dto/                # Pydantic-схемы
    │   ├── entity_type.py  # EntityTypeCreate, EntityTypeRead, ...
    │   ├── entity.py
    │   └── task.py
    └── use_cases/          # Оркестрация (пока не используется)

**Пример DTO:**

    # application/dto/entity_type.py
    class EntityTypeBase(BaseModel):
        name: str
        icon: str = "📄"
        schema_: EntityTypeSchema = Field(alias="schema")
        xml_schema_code: str | None = None

### 2.3. Adapters (`backend/src/adapters/`)

**Что:** вся инфраструктура — HTTP, БД, S3, Telegram.

**Зависимости:** Domain, Application + внешние библиотеки.

**Структура:**

    adapters/
    ├── db/                       # Работа с БД
    │   ├── base.py               # Base + TimestampMixin
    │   ├── session.py            # AsyncSessionLocal, engine
    │   ├── models/               # SQLAlchemy-модели
    │   │   ├── task.py
    │   │   ├── entity_type.py
    │   │   └── entity.py
    │   └── repositories/         # Реализации портов
    │       ├── task_repo.py
    │       ├── entity_type_repository.py
    │       └── entity_repository.py
    ├── api/                      # HTTP-слой
    │   ├── dependencies.py       # DI: get_*_repo, get_*_service
    │   └── routes/
    │       ├── tasks.py
    │       ├── matrix.py
    │       ├── entity_types.py
    │       └── ...
    ├── notifications/            # Telegram-бот
    │   ├── telegram_bot.py
    │   ├── handlers.py
    │   └── digest.py
    ├── import_export/            # Excel-парсер
    │   └── excel_parser.py
    ├── storage/                  # MinIO AIStor (MVP)
    ├── xml/                      # XML-генерация (MVP-1.5)
    └── llm/                      # Qwen 2.5 (MVP-3)

**Пример SQLAlchemy-модели:**

    # adapters/db/models/entity_type.py
    class EntityTypeModel(Base, TimestampMixin):
        __tablename__ = "entity_types"

        id: Mapped[uuid.UUID] = mapped_column(
            UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
        )
        project_id: Mapped[uuid.UUID] = mapped_column(
            UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE")
        )
        name: Mapped[str] = mapped_column(String(200), nullable=False)
        schema: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

**Пример репозитория:**

    # adapters/db/repositories/entity_type_repository.py
    class SqlAlchemyEntityTypeRepository(EntityTypeRepository):
        def __init__(self, session: AsyncSession) -> None:
            self._session = session

        async def save(self, entity_type: EntityType) -> EntityType:
            model = self._to_model(entity_type)
            merged = await self._session.merge(model)
            await self._session.flush()
            await self._session.refresh(merged)
            return self._to_domain(merged)

**Пример роута:**

    # adapters/api/routes/entity_types.py
    @router.post(
        "/projects/{project_id}/entity-types",
        response_model=EntityTypeRead,
        status_code=status.HTTP_201_CREATED,
    )
    async def create_entity_type(
        project_id: UUID,
        payload: EntityTypeCreate,
        service: EntityTypeServiceDep,
    ) -> EntityTypeRead:
        try:
            created = await service.create(
                project_id=project_id,
                name=payload.name,
                field_schema=payload.schema_.model_dump(mode="json"),
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        return EntityTypeRead.model_validate(created, from_attributes=True)

---

## 3. DI (Dependency Injection)

**Файл:** `backend/src/adapters/api/dependencies.py`.

**Схема:** Session → Repository → Service → Route.

    # 1. Session (на запрос)
    async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
        async with AsyncSessionLocal() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    DbSession = Annotated[AsyncSession, Depends(get_db_session)]

    # 2. Repository (на запрос)
    def get_entity_type_repo(session: DbSession) -> EntityTypeRepository:
        return SqlAlchemyEntityTypeRepository(session)

    EntityTypeRepoDep = Annotated[EntityTypeRepository, Depends(get_entity_type_repo)]

    # 3. Service (на запрос)
    def get_entity_type_service(
        entity_type_repo: EntityTypeRepoDep,
    ) -> EntityTypeService:
        return EntityTypeService(repo=entity_type_repo)

    EntityTypeServiceDep = Annotated[EntityTypeService, Depends(get_entity_type_service)]

**Правило:** в роутах используем **только** `*ServiceDep` и `*RepoDep`. Никаких прямых импортов классов.

---

## 4. Frontend (`frontend/src/`)

**Стек:** React 18 + Vite + TypeScript + shadcn/ui + TanStack Query + React Router + Axios.

**Структура:**

    frontend/src/
    ├── pages/              # Страницы (роутинг)
    │   ├── ProjectsPage.tsx
    │   ├── ProjectPage.tsx
    │   ├── ImportExcelPage.tsx
    │   ├── MatrixPage.tsx
    │   └── ...
    ├── components/         # Компоненты
    │   ├── ui/             # shadcn/ui
    │   ├── Layout.tsx
    │   ├── TaskList.tsx
    │   ├── MatrixTable.tsx
    │   └── ...
    ├── api/                # HTTP-клиент
    │   ├── client.ts       # Axios + interceptors
    │   ├── tasksApi.ts
    │   ├── entityApi.ts
    │   └── ...
    ├── hooks/              # TanStack Query
    │   ├── useTasks.ts
    │   ├── useMatrix.ts
    │   ├── useEntityTypes.ts
    │   └── ...
    ├── lib/
    │   └── utils.ts        # cn() и helpers
    └── main.tsx

**Правила:**

1. **`verbatimModuleSyntax: true`** — типы через `type X`:

        import { type Task, fetchTasks } from './api/tasksApi'

2. **Server state** — только через TanStack Query (`useQuery`, `useMutation`).
3. **HTTP** — только через `frontend/src/api/client.ts` (Axios).
4. **Стили** — Tailwind + shadcn/ui. Никаких CSS-модулей.

---

## 5. Стек (полный)

### Backend

| Слой | Технология | Версия |
|------|-----------|--------|
| Язык | Python | 3.14+ |
| Web | FastAPI | 0.110+ |
| ORM | SQLAlchemy | 2.0+ async |
| Миграции | Alembic | 1.13+ |
| БД | PostgreSQL | 15+ |
| Валидация | Pydantic | 2.0+ |
| Конфиг | pydantic-settings | — |
| Аутентификация (MVP) | JWT + Argon2 | — |
| Логирование | structlog | — |
| Telegram | aiogram | 3.x |
| Тесты | pytest + pytest-asyncio | — |
| Линтер | ruff | — |
| Форматирование | black + isort | — |
| S3 | aioboto3 | — (MVP) |
| XML | lxml + xmlschema | — (MVP-1.5) |
| LLM | llama-cpp-python | — (MVP-3) |

### Frontend

| Слой | Технология | Версия |
|------|-----------|--------|
| Язык | TypeScript | 5.x+ |
| Framework | React | 18+ |
| Сборка | Vite | 5+ |
| UI-кит | shadcn/ui | — |
| Стили | Tailwind CSS | 3+ |
| Server state | TanStack Query | 5+ |
| Формы | React Hook Form + Zod | — |
| Роутинг | React Router | 6+ |
| HTTP | Axios | — |
| Тесты | Vitest | — |

### Инфраструктура

| Слой | Технология |
|------|-----------|
| Контейнеризация | Docker + Docker Compose |
| Reverse proxy | Nginx |
| CI | GitHub Actions |
| Storage | MinIO AIStor Free (S3) |
| Хостинг | VPS в РФ (Timeweb, Aeza, FirstVDS) |

---

## 6. Правила слоёв (шпаргалка)

| Слой | Можно импортировать | Нельзя импортировать |
|------|---------------------|----------------------|
| **domain** | stdlib, typing, dataclasses | FastAPI, SQLAlchemy, Pydantic, asyncpg |
| **application** | domain, Pydantic | FastAPI, SQLAlchemy |
| **adapters/db** | domain, application, SQLAlchemy, asyncpg | FastAPI |
| **adapters/api** | domain, application, adapters/db, FastAPI | — |
| **adapters/notifications** | domain, application, aiogram | FastAPI |
| **frontend** | — | напрямую backend |

**Проверка:** если в `domain/` появился `import fastapi` — это **ошибка архитектуры**.

---

## 7. Ключевые паттерны

### 7.1. Порты и адаптеры

Порт — это **ABC** в `domain/ports/`. Адаптер — **класс**, реализующий порт в `adapters/`.

    # domain/ports/repositories.py
    class EntityTypeRepository(ABC):
        @abstractmethod
        async def get_by_id(self, entity_type_id: UUID) -> EntityType | None: ...

        @abstractmethod
        async def save(self, entity_type: EntityType) -> EntityType: ...

    # adapters/db/repositories/entity_type_repository.py
    class SqlAlchemyEntityTypeRepository(EntityTypeRepository):
        async def get_by_id(self, entity_type_id: UUID) -> EntityType | None:
            ...

### 7.2. Save через merge

Репозитории используют `session.merge()` — один метод для create + update.

    async def save(self, entity_type: EntityType) -> EntityType:
        model = self._to_model(entity_type)
        merged = await self._session.merge(model)
        await self._session.flush()
        await self._session.refresh(merged)
        return self._to_domain(merged)

### 7.3. Mapping: domain ↔ model

Каждый репозиторий имеет два приватных метода:

    @staticmethod
    def _to_domain(model: EntityTypeModel) -> EntityType: ...

    @staticmethod
    def _to_model(domain: EntityType) -> EntityTypeModel: ...

### 7.4. Валидация

1. **DTO** (Pydantic) — на входе (типы, форматы, длины).
2. **Сервис** — бизнес-правила (`if not entity_type: raise ValueError`).
3. **БД** — FK, NOT NULL, UNIQUE.

---

### 7.5. LLM-адаптеры и админка

**Порт:** `LLMProviderPort` (ABC) — `generate(prompt, system_prompt, project_id)`, `health_check()`.
**Адаптеры:** `QwenAdapter` (локальная Qwen), `OpenAICompatibleAdapter` (provod.ai, Cloud.ru).
**Диспетчер:** `RuntimeLLMAdapter` — читает `llm_settings.is_active` (TTL 60s кэш клиентов), создаёт нужный адаптер, проверяет светофор (`Project.data_security_level`).

**Ключи:** `api_key` — Fernet (ключ `LLM_ENCRYPTION_KEY` в `.env`). В БД — `api_key_encrypted` (ciphertext) + `api_key_last4`. Plaintext — только в памяти.

**Админка:** `/api/admin/llm/status|switch|providers|settings`. UI — `AdminLLMPage`. Смена — без перезапуска backend.

### 7.6. Слой изоляции агентов (Agent Gateway + MCP)

**Принцип:** агент не работает с `AsyncSession`, БД или файловой системой
напрямую. Он работает с узким HTTP-интерфейсом — **Agent Gateway**, который
проверяет права и только потом обращается к существующему API. Внешние
инструменты (файлы, Telegram) агент получает **только** через
контролируемый MCP-сервер.

### Схема

    [Контейнер агента] → MCP → [gip-mcp-gateway] → [Agent Gateway] → [Существующий API] → [БД/MinIO]

### Что делает Agent Gateway

1. **Аутентификация агента** — у каждого агента свой токен (не пользовательский).
2. **Проверка периметра** — какой проект, какая сущность, какое действие разрешено.
3. **Проекция данных** — отдаёт агенту только то, что нужно для задачи
   (например, текст замечаний по разделу КР, без остальных томов).
4. **Аудит** — пишет в `AgentLog`: кто, что, когда, на основе каких данных.

### MCP-сервер как единственный канал доступа

Агент подключается к внешним данным **только** через один
контролируемый MCP-сервер (`gip-mcp-gateway`). Этот сервер:

1. **Реализует MCP-протокол** (Resources, Tools).
2. **Не даёт прямого доступа к БД** — только к заранее определённым
   операциям: «прочитать замечания по разделу», «создать RFI»,
   «отправить уведомление».
3. **Проверяет права** на уровне MCP-сервера (какой агент, какой проект,
   какая операция).
4. **Логирует** каждый вызов в `AgentLog`.

**Почему не готовые MCP-серверы (EvoClaw/Cloud.ru):**
EvoClaw позволяет агенту самому выбирать MCP-серверы. Для промышленной
безопасности это недопустимо: агент не должен решать, к какому серверу
идти. Решение принимает архитектор, фиксируя один MCP-сервер с
ограниченным набором Tools.

### Изоляция контейнера агента

- Запуск в отдельном контейнере, **не** в процессе backend.
- **Read-only root FS** (кроме `/tmp`).
- Минимальный набор Linux capabilities (без `NET_ADMIN`, `SYS_PTRACE`).
- Лимиты CPU/памяти.
- **Запрет `pip install` в рантайме** — образ собирается с фиксированным
  набором библиотек.

### Сетевые политики (egress)

- Агент может ходить **только** к `gip-mcp-gateway` (внутренняя сеть).
- Внешний egress (интернет, сторонние API) **заблокирован** на уровне
  инфраструктуры.
- Если агенту нужен внешний сервис (Telegram, почта) — это делается
  **через `gip-mcp-gateway`**, а не напрямую.

**Референс:** NVIDIA NemoClaw (OpenShell, Network Policies, Sandbox
Hardening, Policy Presets).

## 8. Что нельзя нарушать (чек-лист для ИИ)

- ❌ Не импортировать FastAPI / SQLAlchemy в `domain/`.
- ❌ Не использовать `try/except` для валидации (только Pydantic + доменные правила).
- ❌ Не вызывать `session.commit()` вручную (это делает `get_db_session`).
- ❌ Не коммитить в `main` напрямую.
- ❌ Не добавлять новые зависимости без согласования.
- ❌ Не менять `.env` и секреты.
- ❌ Не переписывать архитектуру без согласования.
- ✅ Использовать `type X` в TS (verbatimModuleSyntax).
- ✅ Запускать Alembic **из `backend/`**, не из корня.
- ✅ Тесты — в стиле проекта (AsyncMock, pytest-asyncio).

---

**Конец ARCHITECTURE.md.**