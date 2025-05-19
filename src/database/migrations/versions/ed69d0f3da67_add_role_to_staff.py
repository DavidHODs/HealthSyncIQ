"""add_role_to_staff

Revision ID: ed69d0f3da67
Revises: a46b95da4184
Create Date: 2025-05-18 19:01:11.456749

"""
import sqlalchemy as sa
from alembic import op
from typing_extensions import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = 'ed69d0f3da67'
down_revision: Union[str, None] = 'a46b95da4184'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  """"""
  op.execute(sa.text("""
        ALTER TABLE staffs
        ADD COLUMN role VARCHAR(50) NOT NULL DEFAULT 'Admin';
    """))

  op.execute(sa.text("""
        ALTER TABLE staffs
        ALTER COLUMN role DROP DEFAULT;
    """))


def downgrade() -> None:
  """"""
  op.execute(sa.text("""
        ALTER TABLE staffs
        DROP COLUMN role;
    """))
