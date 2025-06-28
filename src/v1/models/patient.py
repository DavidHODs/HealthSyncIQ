import datetime
import uuid
from typing import Optional, Any

from sqlalchemy import Date, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .base import Base


class PatientModel(Base):
  __tablename__ = "patients"

  id: Mapped[uuid.UUID] = mapped_column(
      UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  registration_code: Mapped[str] = mapped_column(
      String, nullable=False, unique=True)
  surname: Mapped[str] = mapped_column(String, nullable=False)
  first_name: Mapped[str] = mapped_column(String, nullable=False)
  last_name: Mapped[str | None] = mapped_column(String, nullable=True)
  dob: Mapped[datetime.date | None] = mapped_column(Date, nullable=True)
  genotype: Mapped[str | None] = mapped_column(String, nullable=True)
  blood_group: Mapped[str | None] = mapped_column(String, nullable=True)
  gender: Mapped[str | None] = mapped_column(String, nullable=True)
  contact_information: Mapped[str | None] = mapped_column(String, nullable=True)
  emergency_contact: Mapped[str | None] = mapped_column(String, nullable=True)
  email: Mapped[str] = mapped_column(String, nullable=False)
  phone_number: Mapped[str | None] = mapped_column(String, nullable=True)
  meta: Mapped[dict[str, Any]] = mapped_column(
        JSONB, nullable=False, server_default='{}'
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

  def __repr__(self) -> str:
    return f"<PatientModel(id='{self.id}', surname='{self.surname}', first_name='{self.first_name}')>"
