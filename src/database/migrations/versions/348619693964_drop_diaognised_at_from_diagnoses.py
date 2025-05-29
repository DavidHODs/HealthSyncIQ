"""drop_diaognised_at_from_diagnoses

Revision ID: 348619693964
Revises: c1496d41a5bf
Create Date: 2025-05-29 19:56:14.315157

"""
import sqlalchemy as sa
from alembic import op
from typing_extensions import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = '348619693964'
down_revision: Union[str, None] = 'c1496d41a5bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  """Upgrade schema."""
  op.execute(sa.text("""
        ALTER TABLE diagnoses
        DROP COLUMN diagnosed_at;
    """))


def downgrade() -> None:
  """Downgrade schema."""
  op.execute(sa.text("""
        ALTER TABLE diagnoses
        ADD COLUMN diagnosed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW();
    """))
