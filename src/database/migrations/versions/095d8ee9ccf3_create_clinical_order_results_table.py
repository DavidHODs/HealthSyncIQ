"""create_clinical_order_results_table

Revision ID: 095d8ee9ccf3
Revises: be989d669f2b
Create Date: 2025-05-17 20:01:07.739276

"""
from alembic import op
from typing_extensions import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = '095d8ee9ccf3'
down_revision: Union[str, None] = 'be989d669f2b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  """Upgrade schema."""
  op.execute("""
        CREATE TABLE clinical_order_results (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            order_id UUID NOT NULL,
            result_type VARCHAR(50) NOT NULL,
            result_data JSONB NOT NULL,
            result_notes TEXT,
            file_attachments JSONB,
            performed_by_id UUID,
            verified_by_id UUID,
            performed_at TIMESTAMP WITH TIME ZONE,
            verified_at TIMESTAMP WITH TIME ZONE,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE,
            deleted_at TIMESTAMP WITH TIME ZONE,

            CONSTRAINT fk_order_result_order FOREIGN KEY (order_id) REFERENCES clinical_orders(id) ON DELETE CASCADE,
            CONSTRAINT fk_performed_by FOREIGN KEY (performed_by_id) REFERENCES staffs(id) ON DELETE SET NULL,
            CONSTRAINT fk_verified_by FOREIGN KEY (verified_by_id) REFERENCES staffs(id) ON DELETE SET NULL
        );
    """)


def downgrade() -> None:
  """Downgrade schema."""
  op.execute("""
        DROP TABLE clinical_order_results;
    """)
