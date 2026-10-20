"""add result, project_standard, result_goals, standard_goals

Revision ID: b8f3a1c2d9e0
Revises: a1b2c3d4e5f7
Create Date: 2026-10-20
"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'b8f3a1c2d9e0'
down_revision: str | None = 'a1b2c3d4e5f7'


def upgrade() -> None:
    # 1. Create enum
    sa.Enum(
        "deadline", "composition", "format", name="project_standard_type"
    ).create(op.get_bind(), checkfirst=True)

    # 2. Create tables
    op.create_table(
        "results",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column(
            "project_id",
            sa.Uuid(as_uuid=True),
            sa.ForeignKey("projects.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("formulation", sa.String(1000), nullable=False),
        sa.Column("source", sa.String(500), nullable=True),
        sa.Column(
            "approved_by",
            sa.Uuid(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("idx_results_project", "results", ["project_id"])
    op.create_index("idx_results_approved_by", "results", ["approved_by"])

    op.create_table(
        "result_goals",
        sa.Column(
            "result_id",
            sa.Uuid(as_uuid=True),
            sa.ForeignKey("results.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "goal_id",
            sa.Uuid(as_uuid=True),
            sa.ForeignKey("goals.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )

    op.create_table(
        "project_standards",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column(
            "premise_id",
            sa.Uuid(as_uuid=True),
            sa.ForeignKey("premises.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "type",
            sa.Enum(
                "deadline",
                "composition",
                "format",
                name="project_standard_type",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column("value", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column(
            "approved_by",
            sa.Uuid(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index(
        "idx_project_standards_premise", "project_standards", ["premise_id"]
    )
    op.create_index(
        "idx_project_standards_type", "project_standards", ["type"]
    )

    op.create_table(
        "standard_goals",
        sa.Column(
            "standard_id",
            sa.Uuid(as_uuid=True),
            sa.ForeignKey("project_standards.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "goal_id",
            sa.Uuid(as_uuid=True),
            sa.ForeignKey("goals.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("standard_goals")
    op.drop_table("project_standards")
    op.drop_table("result_goals")
    op.drop_table("results")
    sa.Enum(name="project_standard_type").drop(op.get_bind(), checkfirst=True)
