""""add_is_complex_to_tasks"

Revision ID: 25cd82ea2cf7
Revises: f9eba6941cdf
Create Date: 2026-10-20 23:18:30.396222

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '25cd82ea2cf7'
down_revision: Union[str, None] = 'f9eba6941cdf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "tasks",
        sa.Column(
            "is_complex",
            sa.Boolean(),
            nullable=False,
            server_default="false",
        ),
    )


def downgrade() -> None:
    op.drop_column("tasks", "is_complex")