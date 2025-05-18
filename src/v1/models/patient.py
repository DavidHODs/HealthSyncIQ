import uuid

from sqlalchemy import Column, Date, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .base import Base


class PatientModel(Base):
  __tablename__ = "patients"

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  registration_number = Column(String, nullable=False, unique=True)
  surname = Column(String, nullable=False)
  first_name = Column(String, nullable=False)
  last_name = Column(String, nullable=True)
  dob = Column(Date, nullable=True)
  genotype = Column(String, nullable=True)
  blood_group = Column(String, nullable=True)
  gender = Column(String, nullable=True)
  contact_information = Column(String, nullable=True)
  emergency_contact = Column(String, nullable=True)
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
    return f"<PatientModel(id='{self.id}', surname='{self.surname}', first_name='{self.first_name}')>"
