"""create_file_attachemnts_table

Revision ID: 8a810482dc07
Revises: 095d8ee9ccf3
Create Date: 2025-05-17 20:14:47.136807

"""
from alembic import op
from typing_extensions import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = '8a810482dc07'
down_revision: Union[str, None] = '095d8ee9ccf3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  """Upgrade schema."""
  op.execute("""
        CREATE TABLE file_attachments (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            related_entity_type VARCHAR(50) NOT NULL,
            related_entity_id UUID NOT NULL,
            file_name VARCHAR(255) NOT NULL,
            file_path VARCHAR(512) NOT NULL,
            file_type VARCHAR(100) NOT NULL,
            file_size BIGINT NOT NULL,
            uploaded_by_id UUID,
            uploaded_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
            description TEXT,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE,
            deleted_at TIMESTAMP WITH TIME ZONE,

            CONSTRAINT fk_uploaded_by FOREIGN KEY (uploaded_by_id) REFERENCES staffs(id) ON DELETE SET NULL
        );
    """)


def downgrade() -> None:
  """Downgrade schema."""
  op.execute("""
        DROP TABLE file_attachments;
    """)
