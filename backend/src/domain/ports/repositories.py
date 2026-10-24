"""Абстрактные интерфейсы репозиториев (порты).

Домен общается с БД через эти интерфейсы.
Реализации — в backend.src.adapters.db.repositories.
"""

from abc import ABC, abstractmethod
from datetime import date
from uuid import UUID

from backend.src.domain.entities.action import Action
from backend.src.domain.entities.change import Change
from backend.src.domain.entities.cross_task import CrossTask
from backend.src.domain.entities.decision import Decision
from backend.src.domain.entities.decision_link import DecisionLink
from backend.src.domain.entities.document import Document
from backend.src.domain.entities.document_link import DocumentLink
from backend.src.domain.entities.document_type import DocumentType
from backend.src.domain.entities.document_version import DocumentVersion
from backend.src.domain.entities.entity import Entity
from backend.src.domain.entities.entity_type import EntityType
from backend.src.domain.entities.goal import Goal
from backend.src.domain.entities.import_log import ImportLog
from backend.src.domain.entities.norm import Norm
from backend.src.domain.entities.premise import Premise
from backend.src.domain.entities.project import Project
from backend.src.domain.entities.project_standard import ProjectStandard
from backend.src.domain.entities.result import Result
from backend.src.domain.entities.revision import Revision
from backend.src.domain.entities.revision_decision import RevisionDecision
from backend.src.domain.entities.stop_flag import StopFlag
from backend.src.domain.entities.task import Task
from backend.src.domain.entities.user import User
from backend.src.domain.value_objects.document import LifecycleStatus
from backend.src.domain.value_objects.enums import ProjectStandardType


class ProjectRepository(ABC):
    """Репозиторий проектов."""

    @abstractmethod
    async def get_by_id(self, project_id: UUID) -> Project | None: ...

    @abstractmethod
    async def get_all(self, limit: int = 100, offset: int = 0) -> list[Project]: ...

    @abstractmethod
    async def save(self, project: Project) -> Project: ...

    @abstractmethod
    async def delete(self, project_id: UUID) -> None: ...


class TaskRepository(ABC):
    """Репозиторий задач."""

    @abstractmethod
    async def get_by_id(self, task_id: UUID) -> Task | None: ...

    @abstractmethod
    async def get_by_project(
        self, project_id: UUID, limit: int = 500, offset: int = 0
    ) -> list[Task]: ...

    @abstractmethod
    async def get_overdue(self, as_of: date | None = None) -> list[Task]: ...

    @abstractmethod
    async def get_upcoming(self, days: int = 3) -> list[Task]: ...

    @abstractmethod
    async def save(self, task: Task) -> Task: ...

    @abstractmethod
    async def bulk_save(self, tasks: list[Task]) -> list[Task]: ...

    @abstractmethod
    async def delete(self, task_id: UUID) -> None: ...

    async def get_by_pair(
        self,
        project_id: UUID,
        from_section: str,
        to_section: str,
    ) -> list[Task]:
        """Задачи конкретной пары разделов."""
        ...


class CrossTaskRepository(ABC):
    """Репозиторий заданий смежникам (ячейки матрицы)."""

    @abstractmethod
    async def get_by_id(self, cross_task_id: UUID) -> CrossTask | None: ...

    @abstractmethod
    async def get_by_project(self, project_id: UUID) -> list[CrossTask]: ...

    @abstractmethod
    async def find(
        self,
        project_id: UUID,
        from_section_code: str,
        to_section_code: str,
    ) -> CrossTask | None: ...

    @abstractmethod
    async def save(self, cross_task: CrossTask) -> CrossTask: ...


class ImportLogRepository(ABC):
    """Репозиторий логов импорта Excel."""

    @abstractmethod
    async def get_by_id(self, log_id: UUID) -> ImportLog | None: ...

    @abstractmethod
    async def get_by_project(self, project_id: UUID) -> list[ImportLog]: ...

    @abstractmethod
    async def get_pending(self) -> ImportLog | None:
        """Взять первый лог со статусом 'parsing' для воркера."""
        ...

    @abstractmethod
    async def save(self, log: ImportLog) -> ImportLog: ...


class UserRepository(ABC):
    """Репозиторий пользователей."""

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User | None: ...

    @abstractmethod
    async def get_by_telegram_id(self, telegram_id: int) -> User | None: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    async def get_all_with_telegram(self) -> list[User]:
        """Все активные пользователи с привязанным Telegram."""
        ...

    @abstractmethod
    async def save(self, user: User) -> User: ...


class EntityTypeRepository(ABC):
    """Репозиторий типов пользовательских сущностей."""

    @abstractmethod
    async def get_by_id(self, entity_type_id: UUID) -> EntityType | None: ...

    @abstractmethod
    async def list_by_project(self, project_id: UUID) -> list[EntityType]: ...

    @abstractmethod
    async def save(self, entity_type: EntityType) -> EntityType: ...

    @abstractmethod
    async def delete(self, entity_type_id: UUID) -> None: ...


class EntityRepository(ABC):
    """Репозиторий экземпляров пользовательских сущностей."""

    @abstractmethod
    async def get_by_id(self, entity_id: UUID) -> Entity | None: ...

    @abstractmethod
    async def list_by_type(self, entity_type_id: UUID) -> list[Entity]: ...

    @abstractmethod
    async def save(self, entity: Entity) -> Entity: ...

    @abstractmethod
    async def delete(self, entity_id: UUID) -> None: ...


class DocumentTypeRepository(ABC):
    """Порт репозитория типов ГОСТ-документов (справочник)."""

    @abstractmethod
    async def get_by_id(self, id: UUID) -> DocumentType | None:
        """Найти тип по ID."""

    @abstractmethod
    async def get_by_code(self, code: str) -> DocumentType | None:
        """Найти тип по коду (drawing, scheme, ...)."""

    @abstractmethod
    async def list_all(self) -> list[DocumentType]:
        """Все типы, сортировка по code."""


class DocumentRepository(ABC):
    """Порт репозитория ГОСТ-документов."""

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Document | None:
        """Найти документ по ID."""

    @abstractmethod
    async def get_by_guid(self, guid: UUID) -> Document | None:
        """Найти документ по GUID (ГОСТ Р 21.101-2026, 4.1.2.2)."""

    @abstractmethod
    async def list_by_project(
        self,
        project_id: UUID,
        *,
        lifecycle_status: LifecycleStatus | None = None,
    ) -> list[Document]:
        """Документы проекта, опционально — фильтр по статусу жизненного цикла."""

    @abstractmethod
    async def save(self, document: Document) -> Document:
        """Создать или обновить документ (merge по id)."""

    @abstractmethod
    async def delete(self, id: UUID) -> None:
        """Удалить документ по ID (CASCADE на версии и связи)."""


class DocumentVersionRepository(ABC):
    """Порт репозитория версий ГОСТ-документов."""

    @abstractmethod
    async def get_by_id(self, id: UUID) -> DocumentVersion | None:
        """Найти версию по ID."""

    @abstractmethod
    async def list_by_document(self, document_id: UUID) -> list[DocumentVersion]:
        """Все версии документа, сортировка по uploaded_at DESC."""

    @abstractmethod
    async def get_current(self, document_id: UUID) -> DocumentVersion | None:
        """Текущая версия документа (is_current = TRUE)."""

    @abstractmethod
    async def save(self, version: DocumentVersion) -> DocumentVersion:
        """Создать или обновить версию."""

    @abstractmethod
    async def set_current(self, document_id: UUID, version_id: UUID) -> None:
        """Сделать version_id текущей для document_id.
        Атомарно: сбросить is_current у прежней текущей, установить у новой."""


class DocumentLinkRepository(ABC):
    """Порт репозитория связей между ГОСТ-документами."""

    @abstractmethod
    async def get_by_id(self, id: UUID) -> DocumentLink | None:
        """Найти связь по ID."""

    @abstractmethod
    async def list_by_source(self, document_id: UUID) -> list[DocumentLink]:
        """Связи, где document_id — источник."""

    @abstractmethod
    async def list_by_target(self, document_id: UUID) -> list[DocumentLink]:
        """Связи, где document_id — цель."""

    @abstractmethod
    async def save(self, link: DocumentLink) -> DocumentLink:
        """Создать или обновить связь."""

    @abstractmethod
    async def delete(self, id: UUID) -> None:
        """Удалить связь по ID."""


class PremiseRepository(ABC):
    """Порт репозитория вводных (Premise)."""

    @abstractmethod
    async def get_by_id(self, premise_id: UUID) -> Premise | None:
        """Найти вводную по ID."""

    @abstractmethod
    async def list_by_project(self, project_id: UUID) -> list[Premise]:
        """Вводные проекта, сортировка по created_at DESC."""

    @abstractmethod
    async def list_by_source_goal(self, goal_id: UUID) -> list[Premise]:
        """Вводные, где goal_id — source_goal_id."""

    @abstractmethod
    async def save(self, premise: Premise) -> Premise:
        """Создать или обновить вводную (merge по id)."""

    @abstractmethod
    async def delete(self, premise_id: UUID) -> None:
        """Удалить вводную по ID."""


class GoalRepository(ABC):
    """Порт репозитория целей (Goal)."""

    @abstractmethod
    async def get_by_id(self, goal_id: UUID) -> Goal | None:
        """Найти цель по ID."""

    @abstractmethod
    async def list_by_project(self, project_id: UUID) -> list[Goal]:
        """Цели проекта, сортировка по created_at DESC."""

    @abstractmethod
    async def save(self, goal: Goal) -> Goal:
        """Создать или обновить цель (merge по id)."""

    @abstractmethod
    async def delete(self, goal_id: UUID) -> None:
        """Удалить цель по ID."""


class DecisionRepository(ABC):
    """Порт репозитория решений (Decision)."""

    @abstractmethod
    async def get_by_id(self, decision_id: UUID) -> Decision | None:
        """Найти решение по ID."""

    @abstractmethod
    async def list_by_project(self, project_id: UUID) -> list[Decision]:
        """Решения проекта, сортировка по created_at DESC."""

    @abstractmethod
    async def save(self, decision: Decision) -> Decision:
        """Создать или обновить решение (merge по id)."""

    @abstractmethod
    async def delete(self, decision_id: UUID) -> None:
        """Удалить решение по ID."""


class NormRepository(ABC):
    """Порт репозитория нормативных документов (Norm)."""

    @abstractmethod
    async def get_by_id(self, norm_id: UUID) -> Norm | None:
        """Найти норму по ID."""

    @abstractmethod
    async def get_by_code(self, project_id: UUID, code: str) -> Norm | None:
        """Найти норму по обозначению (уникально в проекте)."""

    @abstractmethod
    async def list_by_project(self, project_id: UUID) -> list[Norm]:
        """Нормы проекта, сортировка по created_at DESC."""

    @abstractmethod
    async def save(self, norm: Norm) -> Norm:
        """Создать или обновить норму (merge по id)."""

    @abstractmethod
    async def delete(self, norm_id: UUID) -> None:
        """Удалить норму по ID."""


class DecisionLinkRepository(ABC):
    """Порт репозитория связей решений (DecisionLink)."""

    @abstractmethod
    async def get_by_id(self, link_id: UUID) -> DecisionLink | None:
        """Найти связь по ID."""

    @abstractmethod
    async def list_by_decision(self, decision_id: UUID) -> list[DecisionLink]:
        """Связи, где decision_id — from или to."""

    @abstractmethod
    async def list_by_project(self, project_id: UUID) -> list[DecisionLink]:
        """Связи проекта, сортировка по created_at DESC."""

    @abstractmethod
    async def save(self, link: DecisionLink) -> DecisionLink:
        """Создать или обновить связь (merge по id)."""

    @abstractmethod
    async def delete(self, link_id: UUID) -> None:
        """Удалить связь по ID."""


class DecisionNormRepository(ABC):
    """Порт репозитория связи Decision ↔ Norm (M:N)."""

    @abstractmethod
    async def list_norms_by_decision(self, decision_id: UUID) -> list[UUID]:
        """UUID норм, связанных с решением."""

    @abstractmethod
    async def list_decisions_by_norm(self, norm_id: UUID) -> list[UUID]:
        """UUID решений, связанных с нормой."""

    @abstractmethod
    async def link(self, decision_id: UUID, norm_id: UUID) -> None:
        """Связать решение с нормой (идемпотентно)."""

    @abstractmethod
    async def unlink(self, decision_id: UUID, norm_id: UUID) -> None:
        """Разорвать связь решения с нормой."""


class RfiRepository(ABC):
    """Порт репозитория RFI (Task с is_rfi=true)."""

    @abstractmethod
    async def list_rfis_by_project(self, project_id: UUID) -> list[Task]: ...

    @abstractmethod
    async def get_rfi_by_id(self, id: UUID) -> Task | None: ...

    @abstractmethod
    async def list_by_cause_decision(self, decision_id: UUID) -> list[Task]: ...

    @abstractmethod
    async def list_by_cause_goal(self, goal_id: UUID) -> list[Task]: ...

    @abstractmethod
    async def list_overdue(
        self, today: date, project_id: UUID
    ) -> list[Task]: ...


class RevisionRepository(ABC):
    """Порт репозитория Revision."""

    @abstractmethod
    async def get_by_id(self, revision_id: UUID) -> Revision | None:
        """Найти ревизию по ID."""

    @abstractmethod
    async def list_by_document(
        self,
        document_id: UUID,
    ) -> list[Revision]:
        """Ревизии документа, сортировка по version DESC."""

    @abstractmethod
    async def save(self, revision: Revision) -> Revision:
        """Создать или обновить ревизию (merge по id)."""

    @abstractmethod
    async def delete(self, revision_id: UUID) -> None:
        """Удалить ревизию по ID."""


class ChangeRepository(ABC):
    """Порт репозитория Change."""

    @abstractmethod
    async def get_by_id(self, change_id: UUID) -> Change | None:
        """Найти изменение по ID."""

    @abstractmethod
    async def list_by_revision(self, revision_id: UUID) -> list[Change]:
        """Изменения ревизии, сортировка по field."""

    @abstractmethod
    async def save(self, change: Change) -> Change:
        """Создать или обновить изменение (merge по id)."""

    @abstractmethod
    async def delete(self, change_id: UUID) -> None:
        """Удалить изменение по ID."""


class RevisionDecisionRepository(ABC):
    """Порт репозитория RevisionDecision."""

    @abstractmethod
    async def get_by_id(self, decision_id: UUID) -> RevisionDecision | None:
        """Найти решение по ID."""

    @abstractmethod
    async def list_by_change(
        self,
        change_id: UUID,
    ) -> list[RevisionDecision]:
        """Решения по изменению, сортировка по created_at."""

    @abstractmethod
    async def save(self, decision: RevisionDecision) -> RevisionDecision:
        """Создать или обновить решение (merge по id)."""

    @abstractmethod
    async def delete(self, decision_id: UUID) -> None:
        """Удалить решение по ID."""


class StopFlagRepository(ABC):
    """Порт репозитория StopFlag."""

    @abstractmethod
    async def get_by_id(self, stop_flag_id: UUID) -> StopFlag | None:
        """Найти стоп-сигнал по ID."""

    @abstractmethod
    async def list_by_revision(self, revision_id: UUID) -> list[StopFlag]:
        """Стоп-сигналы ревизии, сортировка по created_at."""

    @abstractmethod
    async def save(self, stop_flag: StopFlag) -> StopFlag:
        """Создать или обновить стоп-сигнал (merge по id)."""

    @abstractmethod
    async def delete(self, stop_flag_id: UUID) -> None:
        """Удалить стоп-сигнал по ID."""


class ResultRepository(ABC):
    """Порт репозитория Result."""

    @abstractmethod
    async def get_by_id(self, result_id: UUID) -> Result | None:
        """Найти результат по ID."""

    @abstractmethod
    async def list_by_project(self, project_id: UUID) -> list[Result]:
        """Результаты проекта."""

    @abstractmethod
    async def list_by_goal(self, goal_id: UUID) -> list[Result]:
        """Результаты, связанные с целью."""

    @abstractmethod
    async def save(self, result: Result) -> Result:
        """Создать или обновить результат (merge по id)."""

    @abstractmethod
    async def delete(self, result_id: UUID) -> None:
        """Удалить результат по ID."""


class ProjectStandardRepository(ABC):
    """Порт репозитория ProjectStandard."""

    @abstractmethod
    async def get_by_id(self, standard_id: UUID) -> ProjectStandard | None:
        """Найти стандарт по ID."""

    @abstractmethod
    async def list_by_premise(self, premise_id: UUID) -> list[ProjectStandard]:
        """Стандарты вводной."""

    @abstractmethod
    async def list_by_type(self, type: ProjectStandardType) -> list[ProjectStandard]:
        """Стандарты типа."""

    @abstractmethod
    async def list_by_goal(self, goal_id: UUID) -> list[ProjectStandard]:
        """Стандарты, связанные с целью."""

    @abstractmethod
    async def save(self, standard: ProjectStandard) -> ProjectStandard:
        """Создать или обновить стандарт (merge по id)."""

    @abstractmethod
    async def delete(self, standard_id: UUID) -> None:
        """Удалить стандарт по ID."""


class ActionRepository(ABC):
    """Порт репозитория действий (Action)."""

    @abstractmethod
    async def get_by_id(self, action_id: UUID) -> Action | None:
        """Найти действие по ID."""

    @abstractmethod
    async def list_by_task(self, task_id: UUID) -> list[Action]:
        """Действия задачи."""

    @abstractmethod
    async def list_by_project(self, project_id: UUID) -> list[Action]:
        """Действия проекта."""

    @abstractmethod
    async def save(self, action: Action) -> Action:
        """Создать или обновить действие (merge по id)."""

    @abstractmethod
    async def delete(self, action_id: UUID) -> None:
        """Удалить действие по ID."""
