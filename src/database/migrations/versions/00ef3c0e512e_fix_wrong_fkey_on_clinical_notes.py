"""fix_wrong_fkey_on_clinical_notes

Revision ID: 00ef3c0e512e
Revises: 9129b86f73c4
Create Date: 2025-05-29 23:00:31.206337

"""
from typing_extensions import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00ef3c0e512e'
down_revision: Union[str, None] = '9129b86f73c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(sa.text("""
        ALTER TABLE clinical_notes
        DROP CONSTRAINT fk_clinical_notes_staff;
    """))
    
    op.execute(sa.text("""
        ALTER TABLE clinical_notes
        ADD CONSTRAINT fk_clinical_notes_note_author_id FOREIGN KEY (note_author_id) REFERENCES staffs(id) ON DELETE CASCADE;
    """))


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(sa.text("""
        ALTER TABLE clinical_notes
        DROP CONSTRAINT fk_clinical_notes_note_author_id;
    """))
    
    op.execute(sa.text("""
        ALTER TABLE clinical_notes
        ADD CONSTRAINT fk_clinical_notes_staff FOREIGN KEY (id) REFERENCES staffs(id) ON DELETE CASCADE;
    """))
