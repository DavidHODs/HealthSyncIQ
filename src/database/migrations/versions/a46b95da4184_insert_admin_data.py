"""insert_admin_data

Revision ID: a46b95da4184
Revises: f8a5d306d43c
Create Date: 2025-05-17 20:45:06.514761

"""
import os
import uuid

import bcrypt
import sqlalchemy as sa
from alembic import op
from typing_extensions import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = 'a46b95da4184'
down_revision: Union[str, None] = 'f8a5d306d43c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

admin_staff_uuid = uuid.uuid4()
it_department_uuid = uuid.uuid4()


def upgrade() -> None:
  """"""
  admin_password = os.getenv("ADMIN_PASSWORD")
  admin_surname = os.getenv("ADMIN_SURNAME", "Admin")
  admin_first_name = os.getenv("ADMIN_FIRST_NAME", "Super")
  admin_last_name = os.getenv("ADMIN_LAST_NAME")
  admin_contact = os.getenv("ADMIN_CONTACT")
  admin_title = os.getenv("ADMIN_TITLE", "")
  admin_email = os.getenv("ADMIN_EMAIL", "admin@example.com")

  if not admin_password:
    print("Warning: ADMIN_PASSWORD environment variable not set")
    hashed_password = None
  else:
    hashed_password = bcrypt.hashpw(
        admin_password.encode('utf-8'),
        bcrypt.gensalt()).decode('utf-8')

  op.execute(sa.text(f"""
        INSERT INTO staffs (id, email, password, title, surname, first_name, last_name, contact_information, is_active, created_at)
        VALUES (
            '{admin_staff_uuid}',
            '{admin_email}',
            '{hashed_password}',
            '{admin_title}',
            '{admin_surname}',
            '{admin_first_name}',
            '{admin_last_name}',
            '{admin_contact}',
            TRUE,
            NOW()
        );
    """))

  op.execute(sa.text(f"""
        INSERT INTO departments (id, name, description, created_at)
        VALUES (
            '{it_department_uuid}',
            'Information Technology',
            'Handles IT infrastructure, systems, and support.',
            NOW()
        );
    """))

  op.execute(sa.text(f"""
        INSERT INTO department_memberships (id, staff_id, department_id, created_at)
        VALUES (
            '{uuid.uuid4()}',
            '{admin_staff_uuid}',
            '{it_department_uuid}',
            NOW()
        );
    """))


def downgrade() -> None:
  """"""
  admin_email = os.getenv("ADMIN_EMAIL", "admin@example.com")

  op.execute(sa.text(f"""
        DELETE FROM department_memberships
        WHERE staff_id = (SELECT id FROM staffs WHERE email = '{admin_email}')
          AND department_id = (SELECT id FROM departments WHERE name = 'Information Technology');
    """))

  op.execute(sa.text(f"""
        DELETE FROM staffs
        WHERE email = '{admin_email}';
    """))

  op.execute(sa.text("""
        DELETE FROM departments
        WHERE name = 'Information Technology';
    """))
