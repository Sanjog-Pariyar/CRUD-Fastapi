"""empty message

Revision ID: 4c0eb186c326
Revises: 271ecbe13622
Create Date: 2025-08-28 13:57:39.709619

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4c0eb186c326'
down_revision: Union[str, Sequence[str], None] = '271ecbe13622'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
