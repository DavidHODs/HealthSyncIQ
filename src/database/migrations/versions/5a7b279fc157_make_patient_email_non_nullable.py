"""make_patient_email_non_nullable

Revision ID: 5a7b279fc157
Revises: 8c5377e5d660
Create Date: 2025-05-28 18:42:13.750767

"""
import sqlalchemy as sa
from alembic import op
from typing_extensions import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = '5a7b279fc157'
down_revision: Union[str, None] = '8c5377e5d660'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  """Upgrade schema."""
  op.execute(sa.text("""
        ALTER TABLE patients
        ALTER COLUMN email SET NOT NULL;
    """))


def downgrade() -> None:
  """Downgrade schema."""
  op.execute(sa.text("""
        ALTER TABLE patients
        ALTER COLUMN email DROP NOT NULL;
    """))
