"""create_clinical_encounters_table

Revision ID: e060b0f479d2
Revises: ac9443929d29
Create Date: 2025-05-17 19:12:58.707189

"""
from alembic import op
from typing_extensions import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = 'e060b0f479d2'
down_revision: Union[str, None] = 'ac9443929d29'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  """Upgrade schema."""
  op.execute("""
        CREATE TABLE clinical_encounters (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            patient_id UUID NOT NULL,
            encounter_type VARCHAR(50) NOT NULL,
            presenting_complaint TEXT,
            start_date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
            end_date TIMESTAMP WITH TIME ZONE,
            attending_doctor_id UUID,
            department_id UUID,
            status VARCHAR(50) NOT NULL DEFAULT 'Active',
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE,
            deleted_at TIMESTAMP WITH TIME ZONE,

            CONSTRAINT fk_patient FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
            CONSTRAINT fk_attending_doctor FOREIGN KEY (attending_doctor_id) REFERENCES staffs(id) ON DELETE SET NULL,
            CONSTRAINT fk_department FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL
        );
    """)


def downgrade() -> None:
  """Downgrade schema."""
  op.execute("""
        DROP TABLE clinical_encounters;
    """)
