import datetime
import uuid

from sqlalchemy import Boolean, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import TIMESTAMP
from typing_extensions import Optional

from .base import Base


class StaffModel(Base):
  __tablename__ = "staffs"

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

  def __repr__(self) -> str:
    return f"<StaffModel(id='{self.id}', surname='{self.surname}', first_name='{self.first_name}')>"
