"""create_nursing_tasks_table

Revision ID: f8a5d306d43c
Revises: 5bccdffa84d4
Create Date: 2025-05-17 20:35:30.070063

"""
from alembic import op
from typing_extensions import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = 'f8a5d306d43c'
down_revision: Union[str, None] = '5bccdffa84d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  """Upgrade schema."""
  op.execute("""
        CREATE TABLE nursing_tasks (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            order_id UUID NOT NULL,
            task_type VARCHAR(100) NOT NULL,
            instructions TEXT NOT NULL,
            frequency VARCHAR(100),
            status VARCHAR(50) NOT NULL DEFAULT 'Pending',
            assigned_to_id UUID,
            performed_by_id UUID,
            performed_at TIMESTAMP WITH TIME ZONE,
            verification_required BOOLEAN DEFAULT FALSE,
            verified_by_id UUID,
            verified_at TIMESTAMP WITH TIME ZONE,
            result_notes TEXT,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE,
            deleted_at TIMESTAMP WITH TIME ZONE,

            CONSTRAINT fk_nursing_task_order FOREIGN KEY (order_id) REFERENCES clinical_orders(id) ON DELETE CASCADE,
            CONSTRAINT fk_assigned_to FOREIGN KEY (assigned_to_id) REFERENCES staffs(id) ON DELETE SET NULL,
            CONSTRAINT fk_performed_by_staff FOREIGN KEY (performed_by_id) REFERENCES staffs(id) ON DELETE SET NULL,
            CONSTRAINT fk_verified_by_staff FOREIGN KEY (verified_by_id) REFERENCES staffs(id) ON DELETE SET NULL
        );
    """)


def downgrade() -> None:
  """Downgrade schema."""
  op.execute("""
        DROP TABLE nursing_tasks;
    """)
