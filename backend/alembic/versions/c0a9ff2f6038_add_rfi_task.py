"""add Task.is_rfi + Document-Action links

Revision ID: c0a9ff2f6038
Revises: c52a3c176d47
Create Date: 2026-10-24 11:58:06.719639

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c0a9ff2f6038'
down_revision: Union[str, None] = 'c52a3c176d47'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create rfi_state enum type (create_type=False in model, so manual CREATE)
    op.execute("CREATE TYPE rfi_state AS ENUM ('open', 'sent', 'answered', 'registered', 'closed', 'escalated')")

    # --- actions ---
    op.add_column('actions', sa.Column('result_document_id', sa.UUID(), nullable=True))
    op.create_index('idx_actions_result_document', 'actions', ['result_document_id'], unique=False)
    op.create_foreign_key(
        'fk_actions_result_document', 'actions', 'documents',
        ['result_document_id'], ['id'], ondelete='SET NULL'
    )

    # --- documents ---
    op.add_column('documents', sa.Column('trigger_action_id', sa.UUID(), nullable=True))
    op.create_index('idx_documents_trigger_action', 'documents', ['trigger_action_id'], unique=False)
    op.create_foreign_key(
        'fk_documents_trigger_action', 'documents', 'actions',
        ['trigger_action_id'], ['id'], ondelete='SET NULL'
    )

    # --- tasks ---
    op.add_column('tasks', sa.Column('is_rfi', sa.Boolean(), server_default='false', nullable=False))
    op.add_column('tasks', sa.Column('rfi_cause_decision_id', sa.UUID(), nullable=True))
    op.add_column('tasks', sa.Column('rfi_cause_goal_id', sa.UUID(), nullable=True))
    op.add_column('tasks', sa.Column('rfi_due_date', sa.Date(), nullable=True))
    op.add_column('tasks', sa.Column(
        'rfi_state',
        sa.Enum('open', 'sent', 'answered', 'registered', 'closed', 'escalated', name='rfi_state', create_type=False),
        nullable=True
    ))
    op.create_index(
        'idx_tasks_is_rfi', 'tasks', ['is_rfi'],
        unique=False, postgresql_where=sa.text('is_rfi = true')
    )
    op.create_index(
        'idx_tasks_rfi_cause_decision', 'tasks', ['rfi_cause_decision_id'],
        unique=False, postgresql_where=sa.text('is_rfi = true')
    )
    op.create_index(
        'idx_tasks_rfi_cause_goal', 'tasks', ['rfi_cause_goal_id'],
        unique=False, postgresql_where=sa.text('is_rfi = true')
    )
    op.create_index(
        'idx_tasks_rfi_due_date', 'tasks', ['rfi_due_date'],
        unique=False, postgresql_where=sa.text('is_rfi = true')
    )
    op.create_foreign_key(
        'fk_tasks_rfi_cause_goal', 'tasks', 'goals',
        ['rfi_cause_goal_id'], ['id'], ondelete='SET NULL'
    )
    op.create_foreign_key(
        'fk_tasks_rfi_cause_decision', 'tasks', 'decisions',
        ['rfi_cause_decision_id'], ['id'], ondelete='SET NULL'
    )
    op.create_check_constraint(
        'ck_tasks_rfi_cause', 'tasks',
        '(is_rfi = false) OR (rfi_cause_decision_id IS NOT NULL OR rfi_cause_goal_id IS NOT NULL)'
    )
    op.create_check_constraint(
        'ck_tasks_rfi_state', 'tasks',
        '(is_rfi = false AND rfi_state IS NULL) OR (is_rfi = true AND rfi_state IS NOT NULL)'
    )


def downgrade() -> None:
    # Drop in reverse order
    op.drop_constraint('ck_tasks_rfi_state', 'tasks', type_='check')
    op.drop_constraint('ck_tasks_rfi_cause', 'tasks', type_='check')
    op.drop_constraint('fk_tasks_rfi_cause_decision', 'tasks', type_='foreignkey')
    op.drop_constraint('fk_tasks_rfi_cause_goal', 'tasks', type_='foreignkey')
    op.drop_index('idx_tasks_rfi_due_date', table_name='tasks')
    op.drop_index('idx_tasks_rfi_cause_goal', table_name='tasks')
    op.drop_index('idx_tasks_rfi_cause_decision', table_name='tasks')
    op.drop_index('idx_tasks_is_rfi', table_name='tasks')
    op.drop_column('tasks', 'rfi_state')
    op.drop_column('tasks', 'rfi_due_date')
    op.drop_column('tasks', 'rfi_cause_goal_id')
    op.drop_column('tasks', 'rfi_cause_decision_id')
    op.drop_column('tasks', 'is_rfi')
    op.drop_constraint('fk_documents_trigger_action', 'documents', type_='foreignkey')
    op.drop_index('idx_documents_trigger_action', table_name='documents')
    op.drop_column('documents', 'trigger_action_id')
    op.drop_constraint('fk_actions_result_document', 'actions', type_='foreignkey')
    op.drop_index('idx_actions_result_document', table_name='actions')
    op.drop_column('actions', 'result_document_id')
    op.execute("DROP TYPE IF EXISTS rfi_state")
