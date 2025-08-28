"""add content column to post table

Revision ID: 39b21d8095b5
Revises: 12821a92c960
Create Date: 2025-08-28 08:48:20.774429

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '39b21d8095b5'
down_revision: Union[str, Sequence[str], None] = '12821a92c960'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
