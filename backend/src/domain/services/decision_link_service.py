"""DecisionLinkService — бизнес-логика связей между решениями."""

import logging
from uuid import UUID

from backend.src.domain.entities.decision_link import DecisionLink
from backend.src.domain.ports.repositories import (
    DecisionLinkRepository,
    DecisionRepository,
)
from backend.src.domain.value_objects.enums import DecisionLinkType

logger = logging.getLogger(__name__)


class DecisionLinkService:
    """Сервис работы со связями решений (DecisionLink)."""

    def __init__(
        self,
        repo: DecisionLinkRepository,
        decision_repo: DecisionRepository,
    ) -> None:
        self._repo = repo
        self._decision_repo = decision_repo

    async def create(
        self,
        project_id: UUID,
        from_decision_id: UUID,
        to_decision_id: UUID,
        link_type: DecisionLinkType,
    ) -> DecisionLink:
        """Создать связь между решениями.

        Raises:
            ValueError: если from == to, решения не найдены,
                из разных проектов или связь уже существует.
        """
        # Валидация 1: не связывать решение с самим собой
        if from_decision_id == to_decision_id:
            raise ValueError("Решение не может быть связано само с собой")

        # Валидация 2: from существует
        from_decision = await self._decision_repo.get_by_id(from_decision_id)
        if from_decision is None:
            raise ValueError(f"Решение {from_decision_id} не найдено")

        # Валидация 3: to существует
        to_decision = await self._decision_repo.get_by_id(to_decision_id)
        if to_decision is None:
            raise ValueError(f"Решение {to_decision_id} не найдено")

        # Валидация 4: оба решения из одного проекта (совпадает с project_id)
        if (
            UUID(str(from_decision.project_id)) != UUID(str(project_id))
            or UUID(str(to_decision.project_id)) != UUID(str(project_id))
        ):
            raise ValueError(
                f"Нельзя связать решения из разных проектов: "
                f"{from_decision.project_id} vs {to_decision.project_id}"
            )

        # Валидация 5: одна связь одного типа между парой решений
        existing_links = await self._repo.list_by_project(project_id)
        for link in existing_links:
            if (
                link.from_decision_id == from_decision_id
                and link.to_decision_id == to_decision_id
                and link.link_type == link_type
            ):
                raise ValueError(
                    f"Связь {from_decision_id} -> {to_decision_id} "
                    f"({link_type.value}) уже существует"
                )

        link = DecisionLink(
            project_id=project_id,
            from_decision_id=from_decision_id,
            to_decision_id=to_decision_id,
            link_type=link_type,
        )
        return await self._repo.save(link)

    async def get_by_id(self, link_id: UUID) -> DecisionLink | None:
        return await self._repo.get_by_id(link_id)

    async def list_by_decision(self, decision_id: UUID) -> list[DecisionLink]:
        return await self._repo.list_by_decision(decision_id)

    async def list_by_project(self, project_id: UUID) -> list[DecisionLink]:
        return await self._repo.list_by_project(project_id)

    async def delete(self, link_id: UUID) -> bool:
        """Удалить связь решений.

        Возвращает True, если удалено. False, если не найдено.
        """
        link = await self._repo.get_by_id(link_id)
        if link is None:
            return False

        await self._repo.delete(link_id)
        return True
