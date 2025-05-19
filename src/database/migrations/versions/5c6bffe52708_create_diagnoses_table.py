"""create_diagnoses_table

Revision ID: 5c6bffe52708
Revises: e060b0f479d2
Create Date: 2025-05-17 19:28:40.333579

"""
from alembic import op
from typing_extensions import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = '5c6bffe52708'
down_revision: Union[str, None] = 'e060b0f479d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  """Upgrade schema."""
  op.execute("""
        CREATE TABLE diagnoses (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            encounter_id UUID NOT NULL,
            diagnosis_description TEXT NOT NULL,
            diagnosed_by_id UUID,
            diagnosed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
            notes TEXT,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE,
            deleted_at TIMESTAMP WITH TIME ZONE,

            CONSTRAINT fk_encounter FOREIGN KEY (encounter_id) REFERENCES clinical_encounters(id) ON DELETE CASCADE,
            CONSTRAINT fk_diagnosed_by FOREIGN KEY (diagnosed_by_id) REFERENCES staffs(id) ON DELETE SET NULL
        );
    """)


def downgrade() -> None:
  """Downgrade schema."""
  op.execute("""
        DROP TABLE diagnoses;
    """)
