"""drop_nursing_and_dispensing_tables

Revision ID: 70c9f048bb6b
Revises: 8dbd855c6532
Create Date: 2025-06-17 15:44:00.408437

"""
from typing_extensions import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '70c9f048bb6b'
down_revision: Union[str, None] = '8dbd855c6532'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(sa.text("DROP TABLE nursing_tasks;"))
    op.execute(sa.text("DROP TABLE medication_dispensing;"))


def downgrade() -> None:
    """Downgrade schema."""
    pass