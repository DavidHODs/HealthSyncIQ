"""add_phone_number_and_email_to_patients_table

Revision ID: 8dc71d21a294
Revises: 882b303aaf46
Create Date: 2025-05-28 15:09:41.817737

"""
import sqlalchemy as sa
from alembic import op
from typing_extensions import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = '8dc71d21a294'
down_revision: Union[str, None] = '882b303aaf46'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  """Upgrade schema."""
  op.execute(sa.text("""
        ALTER TABLE patients
        ADD COLUMN IF NOT EXISTS phone_number VARCHAR(15) NULL,
        ADD COLUMN IF NOT EXISTS email VARCHAR(255) NULL;
    """))


def downgrade() -> None:
  """Downgrade schema."""
  op.execute(sa.text("""
        ALTER TABLE patients
        DROP COLUMN IF EXISTS phone_number,
        DROP COLUMN IF EXISTS email;
    """))
