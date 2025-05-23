import datetime
import uuid

from sqlalchemy import UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP, String, Text
from typing_extensions import Optional

from .base import Base


class DepartmentModel(Base):
  __tablename__ = "departments"

  __table_args__ = (
      UniqueConstraint("name", name="uq_department_name"),
  )

  id: Mapped[uuid.UUID] = mapped_column(
      UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
  )
  name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
  description: Mapped[str | None] = mapped_column(Text, nullable=True)
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

  staffs = relationship(
      "StaffModel",
      secondary="department_memberships",
      lazy="selectin"
  )

  def __repr__(self) -> str:
    return f"<DepartmentModel(id={self.id}, name='{self.name}')>"
