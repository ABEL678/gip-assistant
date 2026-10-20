"""Модель Action (таблица actions)."""

import uuid

from sqlalchemy import Date, Enum, ForeignKey, Index, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.src.adapters.db.base import Base, TimestampMixin
from backend.src.domain.value_objects.enums import ActionState


class ActionModel(Base, TimestampMixin):
    """Действие проекта (веха 2, §5.2.1)."""

    __tablename__ = "actions"
    __table_args__ = (
        Index("idx_actions_task", "task_id"),
        Index("idx_actions_state", "state"),
        Index("idx_actions_deadline", "deadline"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
    )
    formulation: Mapped[str] = mapped_column(String(1000), nullable=False)
    task_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tasks.id", ondelete="SET NULL"),
        nullable=True,
    )
    measurable_result: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    deadline: Mapped[str | None] = mapped_column(Date, nullable=True)
    responsible_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    state: Mapped[str] = mapped_column(
        Enum(ActionState, name="action_state", create_type=False),
        nullable=False,
        default=ActionState.PLAN,
    )
