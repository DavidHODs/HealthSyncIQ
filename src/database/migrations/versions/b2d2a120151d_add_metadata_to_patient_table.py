"""add_metadata_to_patient_table

Revision ID: b2d2a120151d
Revises: 70c9f048bb6b
Create Date: 2025-06-28 22:32:00.899093
"""

from alembic import op
from typing_extensions import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = 'b2d2a120151d'
down_revision: Union[str, None] = '70c9f048bb6b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  """Upgrade schema."""
  op.execute("""
        ALTER TABLE patients
        ADD COLUMN meta JSONB NOT NULL DEFAULT '{}';
    """)


def downgrade() -> None:
  """Downgrade schema."""
  op.execute("""
        ALTER TABLE patients
        DROP COLUMN meta;
    """)
