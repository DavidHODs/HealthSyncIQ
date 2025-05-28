"""drop_department_id_from_clinical_encounters

Revision ID: 882b303aaf46
Revises: ed69d0f3da67
Create Date: 2025-05-28 14:38:21.195487

"""
from typing_extensions import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '882b303aaf46'
down_revision: Union[str, None] = 'ed69d0f3da67'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(sa.text("""
        ALTER TABLE clinical_encounters
        DROP COLUMN department_id;
    """))


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(sa.text("""
        ALTER TABLE clinical_encounters
        ADD COLUMN department_id UUID,
        
        CONSTRAINT fk_department FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL
    """))