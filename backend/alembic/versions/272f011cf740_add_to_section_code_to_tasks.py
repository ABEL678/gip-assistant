"""add to_section_code to tasks

Revision ID: 272f011cf740
Revises: f9f9bed0be0f
Create Date: 2026-10-10 14:08:26.972127

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '272f011cf740'
down_revision: Union[str, None] = 'f9f9bed0be0f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "tasks",
        sa.Column("to_section_code", sa.String(length=50), nullable=True),
    )
    op.create_index(
        "idx_tasks_to_section",
        "tasks",
        ["to_section_code"],
    )


def downgrade() -> None:
    op.drop_index("idx_tasks_to_section", table_name="tasks")
    op.drop_column("tasks", "to_section_code")