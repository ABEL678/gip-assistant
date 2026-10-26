"""add llm_settings and data_security_level

Revision ID: 65999c8dbf97
Revises: b76037d5f79c
Create Date: 2026-10-27 00:30:56.121798

"""
from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '65999c8dbf97'
down_revision: str | None = 'b76037d5f79c'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute(
        """
        DO $$ BEGIN
            CREATE TYPE llm_provider AS ENUM ('qwen', 'openai_compatible');
        EXCEPTION WHEN duplicate_object THEN NULL;
        END $$;
        """
    )
    op.execute(
        """
        DO $$ BEGIN
            CREATE TYPE data_security_level AS ENUM ('green', 'yellow', 'red');
        EXCEPTION WHEN duplicate_object THEN NULL;
        END $$;
        """
    )

    op.add_column(
        'projects',
        sa.Column(
            'data_security_level',
            sa.Enum(
                'green', 'yellow', 'red',
                name='data_security_level',
                create_type=False,
            ),
            nullable=False,
            server_default=sa.text("'green'"),
        ),
    )

    op.create_table(
        'llm_settings',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column(
            'provider',
            sa.Enum(
                'qwen', 'openai_compatible',
                name='llm_provider',
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column('model_name', sa.String(length=100), nullable=False),
        sa.Column('base_url', sa.String(length=500), nullable=True),
        sa.Column('api_key_encrypted', sa.LargeBinary(), nullable=True),
        sa.Column('api_key_last4', sa.String(length=4), nullable=True),
        sa.Column(
            'params',
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column(
            'is_active',
            sa.Boolean(),
            nullable=False,
            server_default=sa.text('false'),
        ),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.CheckConstraint(
            '(api_key_encrypted IS NULL) = (api_key_last4 IS NULL)',
            name='ck_llm_settings_key_pair',
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        'idx_llm_settings_active',
        'llm_settings',
        ['is_active'],
        unique=True,
        postgresql_where=sa.text('is_active = true'),
    )


def downgrade() -> None:
    op.drop_index('idx_llm_settings_active', table_name='llm_settings')
    op.drop_table('llm_settings')
    op.drop_column('projects', 'data_security_level')
    op.execute('DROP TYPE IF EXISTS data_security_level')
    op.execute('DROP TYPE IF EXISTS llm_provider')
