"""add documents.rfi_id + premises.source_document_id

Revision ID: b76037d5f79c
Revises: c0a9ff2f6038
Create Date: 2026-10-24 15:05:02.527453

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b76037d5f79c'
down_revision: Union[str, None] = 'c0a9ff2f6038'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # documents.rfi_id — FK → tasks (SET NULL)
    op.add_column('documents', sa.Column('rfi_id', sa.UUID(), nullable=True))
    op.create_index('idx_documents_rfi', 'documents', ['rfi_id'])
    op.create_foreign_key(
        'documents_rfi_id_fkey',
        'documents', 'tasks',
        ['rfi_id'], ['id'],
        ondelete='SET NULL'
    )

    # premises.source_document_id — FK → documents (SET NULL)
    op.add_column('premises', sa.Column('source_document_id', sa.UUID(), nullable=True))
    op.create_index('idx_premises_source_document', 'premises', ['source_document_id'])
    op.create_foreign_key(
        'premises_source_document_id_fkey',
        'premises', 'documents',
        ['source_document_id'], ['id'],
        ondelete='SET NULL'
    )


def downgrade() -> None:
    op.drop_constraint('premises_source_document_id_fkey', 'premises', type_='foreignkey')
    op.drop_index('idx_premises_source_document', 'premises')
    op.drop_column('premises', 'source_document_id')

    op.drop_constraint('documents_rfi_id_fkey', 'documents', type_='foreignkey')
    op.drop_index('idx_documents_rfi', 'documents')
    op.drop_column('documents', 'rfi_id')
