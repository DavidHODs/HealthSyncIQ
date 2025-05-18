"""create_clinical_notes_table

Revision ID: 455e0e6d2471
Revises: 5c6bffe52708
Create Date: 2025-05-17 19:39:00.053726

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '455e0e6d2471'
down_revision: Union[str, None] = '5c6bffe52708'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  """Upgrade schema."""
  op.execute("""
        CREATE TABLE clinical_notes (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            encounter_id UUID NOT NULL,
            note_type VARCHAR(50) NOT NULL,
            note_content TEXT NOT NULL,
            staff_id UUID NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE,
            deleted_at TIMESTAMP WITH TIME ZONE,

            CONSTRAINT fk_clinical_notes_encounter FOREIGN KEY (encounter_id) REFERENCES clinical_encounters(id) ON DELETE CASCADE,
            CONSTRAINT fk_clinical_notes_staff FOREIGN KEY (id) REFERENCES staffs(id) ON DELETE CASCADE
        );
    """)


def downgrade() -> None:
  """Downgrade schema."""
  op.execute("""
        DROP TABLE clinical_notes;
    """)
