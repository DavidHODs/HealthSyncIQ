"""drop_ordering_department_from_clinical_order

Revision ID: 32479c586003
Revises: 00ef3c0e512e
Create Date: 2025-06-17 13:40:07.232245

"""
import sqlalchemy as sa
from alembic import op
from typing_extensions import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = '32479c586003'
down_revision: Union[str, None] = '00ef3c0e512e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  """Upgrade schema."""
  op.execute(sa.text("""
        ALTER TABLE clinical_orders
        DROP CONSTRAINT fk_ordering_department;
    """))
  op.execute(sa.text("""
        ALTER TABLE clinical_orders
        DROP COLUMN ordering_department_id;
    """))


def downgrade() -> None:
  """Downgrade schema."""
  op.execute(sa.text("""
        ALTER TABLE clinical_orders
        ADD COLUMN ordering_department_id VARCHAR;
    """))
  op.execute(sa.text("""
        ALTER TABLE clinical_orders
        ADD CONSTRAINT fk_ordering_department
        FOREIGN KEY (ordering_department_id) REFERENCES departments(id) ON DELETE SET NULL;
    """))
