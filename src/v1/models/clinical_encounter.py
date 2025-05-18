import uuid

from sqlalchemy import Column, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .base import Base


class ClinicalEncounterModel(Base):
  __tablename__ = "clinical_encounters"

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  patient = Column(
      UUID(
          as_uuid=True),
      ForeignKey(
          "patients.id",
          ondelete="CASCADE"),
      nullable=False)
  encounter_type = Column(String(50), nullable=False)
  presenting_complaint = Column(Text, nullable=True)
  start_date = Column(
      TIMESTAMP(timezone=True),
      server_default=func.now(),
      nullable=False
  )
  end_date = Column(TIMESTAMP(timezone=True), nullable=True)
  attending_doctor_id = Column(
      UUID(
          as_uuid=True), ForeignKey(
          "staffs.id", ondelete="SET NULL"), nullable=True)
  department_id = Column(
      UUID(
          as_uuid=True),
      ForeignKey(
          "departments.id",
          ondelete="SET NULL"),
      nullable=True)
  status = Column(String(50), nullable=False, default='Active')
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
    return f"<ClinicalEncounterModel(id='{self.id}', patient_id='{self.id}', encounter_type='{self.encounter_type}')>"
