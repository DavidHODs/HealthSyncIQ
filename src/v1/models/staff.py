import datetime
import uuid

from sqlalchemy import Boolean, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from typing_extensions import List, Optional

from .base import Base
from .department import DepartmentModel


class StaffModel(Base):
  __tablename__ = "staffs"

  __table_args__ = (
      UniqueConstraint("email", name="uq_staffs_email"),
  )

  id: Mapped[uuid.UUID] = mapped_column(
      UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
  password: Mapped[str] = mapped_column(String, nullable=False)
  title: Mapped[str] = mapped_column(String, nullable=False)
  surname: Mapped[str] = mapped_column(String, nullable=False)
  first_name: Mapped[str] = mapped_column(String, nullable=False)
  last_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
  role: Mapped[str] = mapped_column(String, nullable=False)
  contact_information: Mapped[Optional[str]
                              ] = mapped_column(String, nullable=True)
  is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
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
  departments: Mapped[List["DepartmentModel"]] = relationship(
      "DepartmentModel",
      secondary="department_memberships",
      lazy="selectin"
  )

  def __repr__(self) -> str:
    return f"<StaffModel(id='{self.id}', surname='{self.surname}', first_name='{self.first_name}')>"
