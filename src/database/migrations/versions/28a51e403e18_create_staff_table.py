"""create_staff_table

Revision ID: 28a51e403e18
Revises:
Create Date: 2025-05-17 16:56:03.798597

"""
from alembic import op
from typing_extensions import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = '28a51e403e18'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  """Upgrade schema."""
  op.execute("""
        CREATE TABLE staffs (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            title VARCHAR (100) NOT NULL,
            surname VARCHAR(255) NOT NULL,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255),
            contact_information VARCHAR(255),
            is_active BOOLEAN NOT NULL DEFAULT TRUE,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE,
            deleted_at TIMESTAMP WITH TIME ZONE
        );
    """)


def downgrade() -> None:
  """Downgrade schema."""
  op.execute("""
        DROP TABLE staffs; -- Changed table name to staffs
    """)
