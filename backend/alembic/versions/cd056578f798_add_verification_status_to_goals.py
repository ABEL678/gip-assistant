"""add_verification_status_to_goals

Revision ID: cd056578f798
Revises: de7ac71d9ae0
Create Date: 2026-10-18 22:10:30.719693

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd056578f798'
down_revision: Union[str, None] = 'de7ac71d9ae0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    verification_status_enum = sa.Enum(
        "confirmed", "not_confirmed", "requires_check", "no_data",
        name="verification_status",
    )
    verification_status_enum.create(op.get_bind(), checkfirst=True)
    op.add_column(
        "goals",
        sa.Column(
            "verification_status",
            verification_status_enum,
            nullable=False,
            server_default="requires_check",
        ),
    )
    op.create_index(
        "idx_goals_verification_status", "goals", ["verification_status"]
    )


def downgrade() -> None:
    op.drop_index("idx_goals_verification_status", table_name="goals")
    op.drop_column("goals", "verification_status")
    verification_status_enum = sa.Enum(
        "confirmed", "not_confirmed", "requires_check", "no_data",
        name="verification_status",
    )
    verification_status_enum.drop(op.get_bind(), checkfirst=True)