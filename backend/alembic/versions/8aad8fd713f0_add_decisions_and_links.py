"""add decisions + decision_goals + decision_premises + tasks.decision_id.

Revision ID: 8aad8fd713f0
Revises: 25cd82ea2cf7
Create Date: 2026-10-22 21:59:48.129195
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '8aad8fd713f0'
down_revision: Union[str, None] = '25cd82ea2cf7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- decisions ---
    op.create_table('decisions',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('project_id', sa.UUID(), nullable=False),
    sa.Column('formulation', sa.String(length=500), nullable=False),
    sa.Column('rationale', sa.Text(), nullable=True),
    sa.Column('context', sa.Text(), nullable=True),
    sa.Column('deadline', sa.Date(), nullable=True),
    sa.Column('state', sa.Enum('PLAN', 'IN_PROGRESS', 'ACCEPTED', 'CANCELLED', 'REPLACED', name='decision_state'), nullable=False),
    sa.Column('created_by', sa.UUID(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_decisions_deadline', 'decisions', ['deadline'], unique=False)
    op.create_index('idx_decisions_project', 'decisions', ['project_id'], unique=False)
    op.create_index('idx_decisions_state', 'decisions', ['state'], unique=False)

    # --- decision_goals ---
    op.create_table('decision_goals',
    sa.Column('decision_id', sa.UUID(), nullable=False),
    sa.Column('goal_id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['decision_id'], ['decisions.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['goal_id'], ['goals.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('decision_id', 'goal_id')
    )
    op.create_index('idx_decision_goals_decision', 'decision_goals', ['decision_id'], unique=False)
    op.create_index('idx_decision_goals_goal', 'decision_goals', ['goal_id'], unique=False)

    # --- decision_premises ---
    op.create_table('decision_premises',
    sa.Column('decision_id', sa.UUID(), nullable=False),
    sa.Column('premise_id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['decision_id'], ['decisions.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['premise_id'], ['premises.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('decision_id', 'premise_id')
    )
    op.create_index('idx_decision_premises_decision', 'decision_premises', ['decision_id'], unique=False)
    op.create_index('idx_decision_premises_premise', 'decision_premises', ['premise_id'], unique=False)

    # --- tasks.decision_id ---
    op.add_column('tasks', sa.Column('decision_id', sa.UUID(), nullable=True))
    op.create_index('idx_tasks_decision', 'tasks', ['decision_id'], unique=False)
    op.create_foreign_key(
        'fk_tasks_decision_id_decisions',
        'tasks', 'decisions',
        ['decision_id'], ['id'],
        ondelete='SET NULL'
    )


def downgrade() -> None:
    # --- tasks.decision_id ---
    op.drop_constraint('fk_tasks_decision_id_decisions', 'tasks', type_='foreignkey')
    op.drop_index('idx_tasks_decision', table_name='tasks')
    op.drop_column('tasks', 'decision_id')

    # --- tables (reverse order) ---
    op.drop_index('idx_decision_premises_premise', table_name='decision_premises')
    op.drop_index('idx_decision_premises_decision', table_name='decision_premises')
    op.drop_table('decision_premises')

    op.drop_index('idx_decision_goals_goal', table_name='decision_goals')
    op.drop_index('idx_decision_goals_decision', table_name='decision_goals')
    op.drop_table('decision_goals')

    op.drop_index('idx_decisions_state', table_name='decisions')
    op.drop_index('idx_decisions_project', table_name='decisions')
    op.drop_index('idx_decisions_deadline', table_name='decisions')
    op.drop_table('decisions')

    # --- enum ---
    op.execute('DROP TYPE decision_state')
