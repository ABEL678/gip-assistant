"""add_actions_table

Revision ID: f9eba6941cdf
Revises: 8fc3a69b4247
Create Date: 2026-10-20

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f9eba6941cdf"
down_revision: str | None = "8fc3a69b4247"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    sa.Enum("plan", "in_progress", "done", "overdue", "cancelled", name="action_state").create(
        bind=op.get_bind(), checkfirst=True
    )

    op.create_table(
        "actions",
        sa.Column(
            "id",
            sa.Uuid(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "project_id",
            sa.Uuid(as_uuid=True),
            sa.ForeignKey("projects.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("formulation", sa.String(1000), nullable=False),
        sa.Column(
            "task_id",
            sa.Uuid(as_uuid=True),
            sa.ForeignKey("tasks.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("measurable_result", sa.String(1000), nullable=True),
        sa.Column("deadline", sa.Date(), nullable=True),
        sa.Column(
            "responsible_id",
            sa.Uuid(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "state",
            sa.Enum(
                "plan",
                "in_progress",
                "done",
                "overdue",
                "cancelled",
                name="action_state",
                create_type=False,
            ),
            nullable=False,
            server_default="plan",
        ),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )

    op.create_index("idx_actions_task", "actions", ["task_id"])
    op.create_index("idx_actions_state", "actions", ["state"])
    op.create_index("idx_actions_deadline", "actions", ["deadline"])


def downgrade() -> None:
    op.drop_table("actions")
    sa.Enum("action_state").drop(bind=op.get_bind(), checkfirst=True)
