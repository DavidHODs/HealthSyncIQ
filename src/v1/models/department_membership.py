import datetime
import uuid

from sqlalchemy import ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from typing_extensions import Optional

from .base import Base


class DepartmentMembershipModel(Base):
  __tablename__ = "department_memberships"

  id: Mapped[uuid.UUID] = mapped_column(
      UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  staff_id: Mapped[uuid.UUID] = mapped_column(
      UUID(as_uuid=True),
      ForeignKey("staffs.id", ondelete="CASCADE"),
      nullable=False
  )
  department_id: Mapped[uuid.UUID] = mapped_column(
      UUID(as_uuid=True),
      ForeignKey("departments.id", ondelete="CASCADE"),
      nullable=False
  )
  created_at: Mapped[datetime.datetime] = mapped_column(
      TIMESTAMP(timezone=True),
      server_default=func.now(),
      nullable=False
  )
  updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(
      TIMESTAMP(timezone=True),
      server_default=func.now(),
      onupdate=func.now(),
      nullable=True
  )
  deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(
      TIMESTAMP(timezone=True), nullable=True)

  staff = relationship(
      "StaffModel",
      backref="department_memberships",
      uselist=False)
  department = relationship(
      "DepartmentModel",
      backref="staff_memberships",
      uselist=False)

  def __repr__(self) -> str:
    return (
        f"<DepartmentMembershipModel(id='{self.id}', staff_id='{self.staff_id}', department_id='{self.department_id}')>"
    )
