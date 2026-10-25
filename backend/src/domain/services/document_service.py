"""DocumentService — бизнес-логика ГОСТ-документов.

Реализация ТЗ 4.4, раздел 16.
"""

import logging
from uuid import UUID

from backend.src.domain.entities.document import Document
from backend.src.domain.ports.repositories import (
    DocumentRepository,
    DocumentTypeRepository,
    TaskRepository,
)
from backend.src.domain.value_objects.document import (
    DocPartType,
    DocumentKind,
    LifecycleStatus,
)

logger = logging.getLogger(__name__)


class DocumentService:
    """Сервис работы с ГОСТ-документами."""

    def __init__(
        self,
        repo: DocumentRepository,
        document_type_repo: DocumentTypeRepository,
        task_repo: TaskRepository,
    ) -> None:
        self._repo = repo
        self._document_type_repo = document_type_repo
        self._task_repo = task_repo

    async def create(
        self,
        project_id: UUID,
        document_type_id: UUID,
        document_name: str,
        cipher: str,
        document_kind: DocumentKind = DocumentKind.PD,
        doc_part_type: DocPartType | None = None,
        section_code: str | None = None,
        mark: str | None = None,
        base_designation: str | None = None,
        entity_id: UUID | None = None,
        task_id: UUID | None = None,
        lifecycle_status: LifecycleStatus = LifecycleStatus.DRAFT,
        version_parent_id: UUID | None = None,
        replaces_id: UUID | None = None,
        replaced_by_id: UUID | None = None,
        rfi_id: UUID | None = None,
        trigger_action_id: UUID | None = None,
    ) -> Document:
        """Создать ГОСТ-документ."""
        document_type = await self._document_type_repo.get_by_id(document_type_id)
        if document_type is None:
            raise ValueError(f"Тип документа {document_type_id} не найден")

        # Валидация rfi_id (спека §2.2)
        if rfi_id is not None:
            task = await self._task_repo.get_by_id(rfi_id)
            if task is None:
                raise ValueError(f"Task {rfi_id} не найден")
            if not task.is_rfi:
                raise ValueError(
                    f"Task {rfi_id} не является RFI (is_rfi=false)"
                )
            if task.project_id != project_id:
                raise ValueError(
                    f"Task {rfi_id} принадлежит другому проекту"
                )

        document = Document(
            project_id=project_id,
            document_type_id=document_type_id,
            document_name=document_name,
            cipher=cipher,
            document_kind=document_kind,
            doc_part_type=doc_part_type,
            section_code=section_code,
            mark=mark,
            base_designation=base_designation,
            entity_id=entity_id,
            task_id=task_id,
            lifecycle_status=lifecycle_status,
            version_parent_id=version_parent_id,
            replaces_id=replaces_id,
            replaced_by_id=replaced_by_id,
            rfi_id=rfi_id,
            trigger_action_id=trigger_action_id,
        )
        return await self._repo.save(document)

    async def get_by_id(self, id: UUID) -> Document | None:
        return await self._repo.get_by_id(id)

    async def get_by_guid(self, guid: UUID) -> Document | None:
        return await self._repo.get_by_guid(guid)

    async def list_by_project(
        self,
        project_id: UUID,
        *,
        lifecycle_status: LifecycleStatus | None = None,
    ) -> list[Document]:
        """Список документов проекта."""
        return await self._repo.list_by_project(project_id, lifecycle_status=lifecycle_status)

    async def update(
        self,
        id: UUID,
        *,
        document_name: str | None = None,
        document_kind: DocumentKind | None = None,
        doc_part_type: DocPartType | None = None,
        section_code: str | None = None,
        mark: str | None = None,
        base_designation: str | None = None,
        lifecycle_status: LifecycleStatus | None = None,
        rfi_id: UUID | None = None,
        trigger_action_id: UUID | None = None,
    ) -> Document | None:
        """Обновить ГОСТ-документ.

        Примечание: None-sentinel — None означает «не менять поле».
        Для очистки rfi_id нужно удалить и создать документ заново.
        """
        document = await self._repo.get_by_id(id)
        if document is None:
            return None

        # Валидация rfi_id (спека §2.2)
        if rfi_id is not None:
            task = await self._task_repo.get_by_id(rfi_id)
            if task is None:
                raise ValueError(f"Task {rfi_id} не найден")
            if not task.is_rfi:
                raise ValueError(
                    f"Task {rfi_id} не является RFI (is_rfi=false)"
                )
            if task.project_id != document.project_id:
                raise ValueError(
                    f"Task {rfi_id} принадлежит другому проекту"
                )

        if document_name is not None:
            document.document_name = document_name
        if document_kind is not None:
            document.document_kind = document_kind
        if doc_part_type is not None:
            document.doc_part_type = doc_part_type
        if section_code is not None:
            document.section_code = section_code
        if mark is not None:
            document.mark = mark
        if base_designation is not None:
            document.base_designation = base_designation
        if lifecycle_status is not None:
            document.lifecycle_status = lifecycle_status
        if rfi_id is not None:
            document.rfi_id = rfi_id
        if trigger_action_id is not None:
            document.trigger_action_id = trigger_action_id

        return await self._repo.save(document)

    async def delete(self, id: UUID) -> bool:
        """Удалить ГОСТ-документ.

        Возвращает True, если удалено. False, если не найдено.
        """
        document = await self._repo.get_by_id(id)
        if document is None:
            return False

        await self._repo.delete(id)
        return True
