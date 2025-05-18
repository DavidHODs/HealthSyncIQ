"""create_department_membership_table

Revision ID: 306c966ede1c
Revises: 8d25742af546
Create Date: 2025-05-17 17:49:38.720126

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '306c966ede1c'
down_revision: Union[str, None] = '8d25742af546'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  """Upgrade schema."""
  op.execute("""
        CREATE TABLE department_memberships (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            staff_id UUID NOT NULL,
            department_id UUID NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE,
            deleted_at TIMESTAMP WITH TIME ZONE,
            FOREIGN KEY (staff_id) REFERENCES staffs (id) ON DELETE CASCADE,
            FOREIGN KEY (department_id) REFERENCES departments (id) ON DELETE CASCADE
        );
    """)


def downgrade() -> None:
  """Downgrade schema."""
  op.execute("""
        DROP TABLE department_memberships;
    """)
