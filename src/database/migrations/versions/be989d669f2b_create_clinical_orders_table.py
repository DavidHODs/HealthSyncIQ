"""create_clinical_orders_table

Revision ID: be989d669f2b
Revises: 455e0e6d2471
Create Date: 2025-05-17 19:48:18.095204

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'be989d669f2b'
down_revision: Union[str, None] = '455e0e6d2471'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  """Upgrade schema."""
  op.execute("""
        CREATE TABLE clinical_orders (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            encounter_id UUID NOT NULL,
            order_type VARCHAR(50) NOT NULL,
            order_details JSONB NOT NULL,
            ordering_department_id UUID,
            target_department_id UUID,
            ordered_by_id UUID NOT NULL,
            priority VARCHAR(50) DEFAULT 'Routine',
            status VARCHAR(50) NOT NULL DEFAULT 'Ordered',
            order_notes TEXT,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE,
            deleted_at TIMESTAMP WITH TIME ZONE,

            CONSTRAINT fk_clinical_orders_encounter FOREIGN KEY (encounter_id) REFERENCES clinical_encounters(id) ON DELETE CASCADE,
            CONSTRAINT fk_ordering_department FOREIGN KEY (ordering_department_id) REFERENCES departments(id) ON DELETE SET NULL,
            CONSTRAINT fk_target_department FOREIGN KEY (target_department_id) REFERENCES departments(id) ON DELETE SET NULL,
            CONSTRAINT fk_ordered_by FOREIGN KEY (ordered_by_id) REFERENCES staffs(id) ON DELETE CASCADE
        );
    """)


def downgrade() -> None:
  """Downgrade schema."""
  op.execute("""
        DROP TABLE clinical_orders;
    """)
