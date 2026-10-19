"""add revisions, changes, revision_decisions, stop_flags; premise_id to documents

Revision ID: a1b2c3d4e5f7
Revises: cd056578f798
Create Date: 2026-10-20

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f7'
down_revision: Union[str, None] = 'cd056578f798'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Enums are created implicitly via sa.Enum in column definitions
    # (checkfirst=True prevents duplicates)

    # 1. Create tables (in dependency order)
    op.create_table(
        "revisions",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True, default=sa.func.uuid_generate_v4()),
        sa.Column("document_id", sa.UUID(as_uuid=True),
                  sa.ForeignKey("documents.id", ondelete="CASCADE"), nullable=False),
        sa.Column("version", sa.Integer, nullable=False),
        sa.Column("date", sa.Date, nullable=True),
        sa.Column("source", sa.String(500), nullable=True),
        sa.Column("notified", sa.Boolean, nullable=False, server_default="f"),
        sa.Column("stop_flag", sa.Boolean, nullable=False, server_default="f"),
        sa.Column("created_at", sa.DateTime(timezone=True),
                  server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True),
                  server_default=sa.func.now(), nullable=False),
        sa.Index("idx_revisions_document", "document_id"),
        sa.Index("idx_revisions_date", "date"),
    )

    op.create_table(
        "changes",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True, default=sa.func.uuid_generate_v4()),
        sa.Column("revision_id", sa.UUID(as_uuid=True),
                  sa.ForeignKey("revisions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("field", sa.String(200), nullable=False),
        sa.Column("old_value", sa.String(1000), nullable=True),
        sa.Column("new_value", sa.String(1000), nullable=True),
        sa.Column("status", sa.Enum("added", "removed", "changed", "unchanged", name="change_status"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True),
                  server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True),
                  server_default=sa.func.now(), nullable=False),
        sa.Index("idx_changes_revision", "revision_id"),
        sa.Index("idx_changes_status", "status"),
    )

    op.create_table(
        "revision_decisions",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True, default=sa.func.uuid_generate_v4()),
        sa.Column("change_id", sa.UUID(as_uuid=True),
                  sa.ForeignKey("changes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("decision", sa.Enum("accepted", "accepted_with_frame", "remark", "rejected", "moved", "deadline", name="revision_decision_type"), nullable=False),
        sa.Column("decided_by", sa.UUID(as_uuid=True),
                  sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("deadline", sa.Date, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True),
                  server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True),
                  server_default=sa.func.now(), nullable=False),
        sa.Index("idx_revision_decisions_change", "change_id"),
    )

    op.create_table(
        "stop_flags",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True, default=sa.func.uuid_generate_v4()),
        sa.Column("revision_id", sa.UUID(as_uuid=True),
                  sa.ForeignKey("revisions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("reason", sa.String(1000), nullable=False),
        sa.Column("resolved", sa.Boolean, nullable=False, server_default="f"),
        sa.Column("created_at", sa.DateTime(timezone=True),
                  server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True),
                  server_default=sa.func.now(), nullable=False),
        sa.Index("idx_stop_flags_revision", "revision_id"),
        sa.Index("idx_stop_flags_resolved", "resolved"),
    )

    # 3. Add premise_id to documents
    op.add_column(
        "documents",
        sa.Column(
            "premise_id",
            sa.UUID(as_uuid=True),
            nullable=True,
        ),
    )
    op.create_foreign_key(
        "fk_documents_premise_premises",
        "documents", "premises",
        ["premise_id"], ["id"],
        ondelete="SET NULL",
    )
    op.create_index("idx_documents_premise", "documents", ["premise_id"])


def downgrade() -> None:
    # Drop in reverse dependency order
    op.drop_index("idx_documents_premise", table_name="documents")
    op.drop_constraint("fk_documents_premise_premises", "documents", type_="foreignkey")
    op.drop_column("documents", "premise_id")

    op.drop_table("stop_flags")
    op.drop_table("revision_decisions")
    op.drop_table("changes")
    op.drop_table("revisions")

    # Drop enums
    op.execute("DROP TYPE IF EXISTS revision_decision_type")
    op.execute("DROP TYPE IF EXISTS change_status")
