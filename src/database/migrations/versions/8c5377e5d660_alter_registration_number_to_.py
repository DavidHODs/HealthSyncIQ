"""alter_registration_number_to_registration_code

Revision ID: 8c5377e5d660
Revises: 8dc71d21a294
Create Date: 2025-05-28 16:43:46.926802

"""
import sqlalchemy as sa
from alembic import op
from typing_extensions import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = '8c5377e5d660'
down_revision: Union[str, None] = '8dc71d21a294'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  """Upgrade schema."""
  op.execute(sa.text("""
        ALTER TABLE patients
        RENAME COLUMN registration_number TO registration_code;
    """))


def downgrade() -> None:
  """Downgrade schema."""
  op.execute(sa.text("""
        ALTER TABLE patients
        RENAME COLUMN registration_code TO registration_number;
    """))
