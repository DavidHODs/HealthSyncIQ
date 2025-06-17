"""rename_clinical_order_results_to_laboratory_orders

Revision ID: 8dbd855c6532
Revises: 32479c586003
Create Date: 2025-06-17 13:48:58.950687

"""
import sqlalchemy as sa
from alembic import op
from typing_extensions import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = '8dbd855c6532'
down_revision: Union[str, None] = '32479c586003'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  """Upgrade schema."""
  op.execute(sa.text("""
        ALTER TABLE clinical_order_results
        RENAME TO laboratory_orders;
    """))


def downgrade() -> None:
  """Downgrade schema."""
  op.execute(sa.text("""
        ALTER TABLE laboratory_orders
        RENAME TO clinical_order_results;
    """))
