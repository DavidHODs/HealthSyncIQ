"""create_patient_table

Revision ID: ac9443929d29
Revises: 306c966ede1c
Create Date: 2025-05-17 18:12:01.107585

"""
from alembic import op
from typing_extensions import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = 'ac9443929d29'
down_revision: Union[str, None] = '306c966ede1c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  """Upgrade schema."""

  op.execute("""
        CREATE TABLE patients (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            registration_number VARCHAR(255) NOT NULL UNIQUE,
            surname VARCHAR(255) NOT NULL,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255),
            dob DATE,
            gender VARCHAR(50),
            genotype VARCHAR(50),
            blood_group VARCHAR(50),
            contact_information VARCHAR(255),
            emergency_contact VARCHAR(255),
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE,
            deleted_at TIMESTAMP WITH TIME ZONE
        );
    """)


def downgrade() -> None:
  """Downgrade schema."""
  op.execute("""
        DROP TABLE patients;
    """)
