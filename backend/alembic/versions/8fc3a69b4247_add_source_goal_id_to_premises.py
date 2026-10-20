"""add source_goal_id to premises

Revision ID: 8fc3a69b4247
Revises: b8f3a1c2d9e0
Create Date: 2026-10-20

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = "8fc3a69b4247"
down_revision: Union[str, None] = "b8f3a1c2d9e0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "premises",
        sa.Column(
            "source_goal_id",
            UUID(as_uuid=True),
            sa.ForeignKey("goals.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )
    op.create_index("idx_premises_source_goal", "premises", ["source_goal_id"])


def downgrade() -> None:
    op.drop_index("idx_premises_source_goal", table_name="premises")
    op.drop_column("premises", "source_goal_id")
