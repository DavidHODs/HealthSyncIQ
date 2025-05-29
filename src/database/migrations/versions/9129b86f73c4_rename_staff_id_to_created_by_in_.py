"""rename_staff_id_to_created_by_in_clinical_notes

Revision ID: 9129b86f73c4
Revises: 348619693964
Create Date: 2025-05-29 21:46:51.731739

"""
import sqlalchemy as sa
from alembic import op
from typing_extensions import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = '9129b86f73c4'
down_revision: Union[str, None] = '348619693964'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  """Upgrade schema."""
  op.execute(sa.text("""
        ALTER TABLE clinical_notes
        RENAME COLUMN staff_id TO note_author_id;
    """))


def downgrade() -> None:
  """Downgrade schema."""
  op.execute(sa.text("""
        ALTER TABLE clinical_notes
        RENAME COLUMN note_author_id TO staff_id;
    """))
