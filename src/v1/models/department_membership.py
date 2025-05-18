import uuid

from sqlalchemy import Column, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .base import Base


class DepartmentMembershipModel(Base):
  __tablename__ = "department_memberships"

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  staff_id = Column(
      UUID(
          as_uuid=True),
      ForeignKey(
          "staffs.id",
          ondelete="CASCADE"),
      nullable=False)
  department_id = Column(
      UUID(
          as_uuid=True),
      ForeignKey(
          "departments.id",
          ondelete="CASCADE"),
      nullable=False)
  created_at = Column(
      TIMESTAMP(timezone=True),
      server_default=func.now(),
      nullable=False
  )
  updated_at = Column(
      TIMESTAMP(timezone=True),
      server_default=func.now(),
      onupdate=func.now(),
      nullable=True
  )
  deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)

  def __repr__(self) -> str:
    return f"<DepartmentMembershipModel(id='{self.id}', staff_id='{self.staff_id}', department_id='{self.department_id}')>"
