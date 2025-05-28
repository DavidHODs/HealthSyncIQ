"""drop_varchar_limits_in_patients_table

Revision ID: e3fa77dfe263
Revises: 5a7b279fc157
Create Date: 2025-05-28 18:45:18.925101

"""
import sqlalchemy as sa
from alembic import op
from typing_extensions import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = 'e3fa77dfe263'
down_revision: Union[str, None] = '5a7b279fc157'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  """Upgrade schema."""
  op.execute(sa.text("""
        ALTER TABLE patients
            ALTER COLUMN registration_code TYPE TEXT,
            ALTER COLUMN surname TYPE TEXT,
            ALTER COLUMN first_name TYPE TEXT,
            ALTER COLUMN last_name TYPE TEXT,
            ALTER COLUMN gender TYPE TEXT,
            ALTER COLUMN genotype TYPE TEXT,
            ALTER COLUMN blood_group TYPE TEXT,
            ALTER COLUMN contact_information TYPE TEXT,
            ALTER COLUMN emergency_contact TYPE TEXT,
            ALTER COLUMN phone_number TYPE TEXT,
            ALTER COLUMN email TYPE TEXT
    """))


def downgrade() -> None:
  """Downgrade schema."""
  op.execute(sa.text("""
        ALTER TABLE patients
            ALTER COLUMN registration_code TYPE VARCHAR(255),
            ALTER COLUMN surname TYPE VARCHAR(255),
            ALTER COLUMN first_name TYPE VARCHAR(255),
            ALTER COLUMN last_name TYPE VARCHAR(255),
            ALTER COLUMN gender TYPE VARCHAR(50),
            ALTER COLUMN genotype TYPE VARCHAR(50),
            ALTER COLUMN blood_group TYPE VARCHAR(50),
            ALTER COLUMN contact_information TYPE VARCHAR(255),
            ALTER COLUMN emergency_contact TYPE VARCHAR(255),
            ALTER COLUMN phone_number TYPE VARCHAR(15),
            ALTER COLUMN email TYPE VARCHAR(255)
    """))
