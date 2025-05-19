"""create_medication_dispensing_table

Revision ID: 5bccdffa84d4
Revises: 8a810482dc07
Create Date: 2025-05-17 20:27:04.287515

"""
from alembic import op
from typing_extensions import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = '5bccdffa84d4'
down_revision: Union[str, None] = '8a810482dc07'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  """Upgrade schema."""
  op.execute("""
        CREATE TABLE medication_dispensing (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            order_id UUID NOT NULL,
            medication_name VARCHAR(255) NOT NULL,
            dosage VARCHAR(100) NOT NULL,
            quantity_ordered INTEGER NOT NULL,
            quantity_dispensed INTEGER,
            status VARCHAR(50) NOT NULL DEFAULT 'Pending',
            dispensed_by_id UUID,
            dispensed_at TIMESTAMP WITH TIME ZONE,
            pharmacy_notes TEXT,
            patient_instructions TEXT,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE,
            deleted_at TIMESTAMP WITH TIME ZONE,

            CONSTRAINT fk_med_dispensing_order FOREIGN KEY (order_id) REFERENCES clinical_orders(id) ON DELETE CASCADE,
            CONSTRAINT fk_dispensed_by FOREIGN KEY (dispensed_by_id) REFERENCES staffs(id) ON DELETE SET NULL
        );
    """)


def downgrade() -> None:
  """Downgrade schema."""
  op.execute("""
        DROP TABLE medication_dispensing;
    """)
