# RULES.md — правила кода

> **Назначение:** единые правила для всего кода проекта.
> Читают: человек-разработчик, GigaCode, самописный ИИ-агент, Code Review.

**Версия:** 1.0
**Обновлено:** 11.10.2026
**Автогенерация:** в MVP-2 файл обновляется из pyproject.toml (ruff).

---

## 1. Общие принципы

1. **Домен чистый.** Domain не знает о FastAPI, SQLAlchemy, Pydantic.
2. **Порты и адаптеры.** Всё внешнее — через ABC-порты.
3. **Тесты для бизнес-логики.** Без них — не мержим.
4. **Один шаг за раз.** Маленькие коммиты, понятные сообщения.
5. **Никаких сюрпризов.** Если меняешь архитектуру — предупреди.

---

## 2. Python

### 2.1. Стиль

- **Python 3.14+.**
- **Строки:** `ruff format` + `ruff check --fix`.
- **Длина строки:** 100 символов (настроено в `pyproject.toml`).
- **Кавычки:** двойные `"..."`.
- **Запятые:** trailing comma в многострочных структурах.

### 2.2. Именование

| Что | Стиль | Пример |
|-----|-------|--------|
| Переменные | snake_case | `entity_type` |
| Функции | snake_case | `get_by_id` |
| Классы | PascalCase | `EntityTypeService` |
| Константы | UPPER_SNAKE | `MAX_ITERATIONS` |
| Приватные | _snake_case | `_session` |

### 2.3. Типизация

- **Все функции аннотированы.**
- **`from __future__ import annotations`** — не нужен (Python 3.14).
- **`X | None`** вместо `Optional[X]`.
- **`list[X]`** вместо `List[X]`.

Пример:

    async def get_by_id(self, entity_id: UUID) -> Entity | None:
        ...

### 2.4. Докстринги

- **Модуль** — короткое описание.
- **Класс** — назначение + пример.
- **Публичный метод** — что делает, что принимает, что возвращает.

Формат — **Google-style**:

    async def create(self, project_id: UUID, name: str) -> EntityType:
        """Создать тип сущности.

        Args:
            project_id: UUID проекта.
            name: Название типа.

        Returns:
            Созданный EntityType.
        """

### 2.5. Исключения

- **Не использовать `try/except` для валидации.** Валидация — Pydantic + доменные правила.
- **Домен** кидает `ValueError` с понятным сообщением.
- **Роуты** ловят `ValueError` → `HTTPException(400)`.
- **Не глотать исключения.** Если ловишь — обрабатывай или логируй.

Пример:

    # domain/services/entity_service.py
    if entity_type.project_id != project_id:
        raise ValueError(
            f"Тип {entity_type_id} принадлежит другому проекту"
        )

    # adapters/api/routes/entity_types.py
    try:
        created = await service.create(...)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

---

## 3. SQLAlchemy

### 3.1. Модели

- **Наследовать** от `Base` + `TimestampMixin` (для полей `created_at`/`updated_at`).
- **Тип `Mapped[...]`** — обязательно.
- **`default=`** — Python-дефолт (например, `default="PD"`).
- **`server_default=`** — SQL-дефолт (например, `server_default=func.now()`).
- **Не объявлять `created_at`/`updated_at`** — они в миксине.

Пример:

    class EntityTypeModel(Base, TimestampMixin):
        __tablename__ = "entity_types"
        __table_args__ = (
            Index("idx_entity_types_project", "project_id"),
        )

        id: Mapped[uuid.UUID] = mapped_column(
            UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
        )
        project_id: Mapped[uuid.UUID] = mapped_column(
            UUID(as_uuid=True),
            ForeignKey("projects.id", ondelete="CASCADE"),
            nullable=False,
        )
        name: Mapped[str] = mapped_column(String(200), nullable=False)

### 3.2. Репозитории

- **Наследуются** от ABC-портов (`EntityTypeRepository`).
- **Метод `save`** — через `session.merge()` (create + update в одном).
- **Mapping:** `_to_domain` и `_to_model`.
- **`session.flush()`** после операций. **НЕ** `commit()` — это делает `get_db_session`.

Пример:

    class SqlAlchemyEntityTypeRepository(EntityTypeRepository):
        def __init__(self, session: AsyncSession) -> None:
            self._session = session

        async def save(self, entity_type: EntityType) -> EntityType:
            model = self._to_model(entity_type)
            merged = await self._session.merge(model)
            await self._session.flush()
            await self._session.refresh(merged)
            return self._to_domain(merged)

### 3.3. Индексы

- **Объявлять в `__table_args__`** — чтобы Alembic их видел.
- **GIN для JSONB:** `Index("...", "data", postgresql_using="gin")`.
- **Все индексы — с осмысленным именем** (`idx_<table>_<field>`).

---

## 4. Pydantic

### 4.1. DTO

- **`BaseModel`** для всех DTO.
- **`Field(...)`** для валидации (min_length, max_length, ...).
- **`ConfigDict(from_attributes=True)`** — для чтения из domain-объектов.
- **`alias="..."`** — если имя поля в JSON отличается от Python.

Пример:

    class EntityTypeBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=200)
        schema_: EntityTypeSchema = Field(alias="schema")

        model_config = ConfigDict(populate_by_name=True)

### 4.2. Алиасы (Pydantic v2)

- **`alias`** — для input + output.
- **`validation_alias`** — только input (или from_attributes).
- **`serialization_alias`** — только output.
- **`AliasChoices("schema", "field_schema")`** — если нужно принять оба имени.

---

## 5. FastAPI

### 5.1. Роуты

- **Тонкие.** Только вызов сервиса + обработка ошибок.
- **`response_model=`** — обязательно.
- **`status_code=`** — для POST (201), DELETE (204).
- **`tags=`** — группировка в Swagger.
- **Ловить `ValueError` → `HTTPException(400)`**.

### 5.2. DI

- **Всё через `Depends`.**
- **В роутах — только `*ServiceDep` и `*RepoDep`.**
- **Никаких прямых импортов классов сервисов/репозиториев в роутах.**

Пример:

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
            created = await service.create(...)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        return EntityTypeRead.model_validate(created, from_attributes=True)

---

## 6. Alembic

### 6.1. Запуск

- **Из папки `backend/`.** Не из корня.
- **`alembic.ini`** — в `backend/alembic.ini`.

### 6.2. Миграции

- **Всегда** с осмысленным сообщением.
- **Проверять** сгенерированный файл **перед** применением.
- **Пустые миграции — удалять.**

Команды:

    alembic revision --autogenerate -m "описание"
    alembic upgrade head
    alembic downgrade -1

### 6.3. Autogenerate

- **Работает**, если модели и БД согласованы.
- **Не увидит** индексы, если их нет в `__table_args__`.
- **Не увидит** server_default, если их нет в модели.
- **Всегда проверяй** сгенерированный файл.

---

## 7. Тесты (pytest)

### 7.1. Общие

- **`pytest + pytest-asyncio`.**
- **Моки — `AsyncMock`.**
- **Именование:** `test_<что>_<условие>`.
- **Один assert — одна проверка** (в идеале).
- **Комментарий-докстринг** в каждом тесте.

### 7.2. Структура

    @pytest.fixture
    def repo():
        return AsyncMock()

    @pytest.mark.asyncio
    async def test_create_minimal(repo, service, project_id):
        """Создание типа с минимальным набором полей."""
        repo.save.side_effect = lambda et: et

        result = await service.create(
            project_id=project_id, name="Исходные данные"
        )

        assert result.name == "Исходные данные"
        repo.save.assert_called_once()

### 7.3. Покрытие

- **Smoke-тесты** — обязательны.
- **80%** — цель, но не гоняться.
- **Всегда** для: сервисов, репозиториев, парсеров.

---

## 8. Git

### 8.1. Ветки

- **`main`** — стабильная.
- **Feature-ветки** — от `main`.
- **Название:** `feat/xxx`, `fix/xxx`, `docs/xxx`.

### 8.2. Коммиты

Формат:

    <type>(<scope>): <короткое описание>

    <опциональное длинное описание>

**Типы:** `feat`, `fix`, `docs`, `refactor`, `test`, `chore`.

Примеры:

    feat(db): add performance indexes
    fix(gitignore): stop ignoring db models
    docs(context): add ARCHITECTURE.md

### 8.3. Push

- **Не коммитить в `main` напрямую** (по плану — через PR, но на начальном этапе допустимо).
- **`git push`** только после успешного `pytest`.

---

## 9. Окружение

### 9.1. Терминал

- **CMD (Windows).**
- **Из корня проекта** (`C:\Users\abelo\GIP-Assistant\gip-assistant`).
- **`.venv` активирован.**

### 9.2. Переменные окружения

- **`.env`** — не коммитится.
- **`.env.example`** — коммитится (шаблон без секретов).
- **Не менять `.env`** без согласования.

### 9.3. Пути

- **Все пути — через `pathlib.Path`** (не `os.path`).
- **Абсолютные — только в конфиге.**

---

## 10. Что НЕ делать

- ❌ Импортировать FastAPI/SQLAlchemy в `domain/`.
- ❌ Использовать `try/except` для валидации.
- ❌ Вызывать `session.commit()` вручную.
- ❌ Коммитить в `main` напрямую.
- ❌ Добавлять зависимости без согласования.
- ❌ Менять `.env` и секреты.
- ❌ Переписывать архитектуру без согласования.
- ❌ Оставлять `TODO` без задачи в `TASKS.md`.
- ❌ Оставлять `print(...)` в коде (использовать `logging`).

---

## 11. Что делать

- ✅ Один шаг за раз, с проверками.
- ✅ Тесты для бизнес-логики.
- ✅ Docstrings для публичных методов.
- ✅ Типизация везде.
- ✅ Маленькие коммиты.
- ✅ Осмысленные сообщения коммитов.
- ✅ `ruff format` + `ruff check --fix` перед коммитом.

---

## 12. Конкретные примеры

### 12.1. Плохо

    # try/except для валидации
    try:
        if not name:
            raise ValueError("Name required")
    except ValueError:
        return None

    # print в коде
    print(f"Creating entity: {name}")

    # Optional вместо X | None
    from typing import Optional
    def f(x: Optional[int]) -> Optional[str]: ...

### 12.2. Хорошо

    # Pydantic + доменные правила
    if not name:
        raise ValueError("Name required")

    # logging
    logger = logging.getLogger(__name__)
    logger.info("Creating entity", extra={"name": name})

    # X | None
    def f(x: int | None) -> str | None: ...

## 13. Работа с документами (ГОСТ Р 21.101-2026)

- GUID — `uuid4()` в приложении, не в БД.
- GUID не меняется при выпуске новых версий.
- `is_current` — только одна версия TRUE для документа.
- Удаление документа — каскадное (ON DELETE CASCADE).

---

**Конец RULES.md.**