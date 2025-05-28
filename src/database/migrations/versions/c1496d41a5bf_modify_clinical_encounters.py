"""modify_clinical_encounters

Revision ID: c1496d41a5bf
Revises: e3fa77dfe263
Create Date: 2025-05-28 21:15:37.619454

"""
import sqlalchemy as sa
from alembic import op
from typing_extensions import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = 'c1496d41a5bf'
down_revision: Union[str, None] = 'e3fa77dfe263'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  """Upgrade schema."""
  op.execute(sa.text("""
        ALTER TABLE clinical_encounters
        ALTER COLUMN attending_doctor_id SET NOT NULL
    """))


def downgrade() -> None:
  """Downgrade schema."""
  op.execute(sa.text("""
        ALTER TABLE clinical_encounters
        ALTER COLUMN attending_doctor_id DROP NOT NULL
    """))
