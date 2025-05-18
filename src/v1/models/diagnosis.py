import uuid

from sqlalchemy import Column, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .base import Base


class DiagnosisModel(Base):
  __tablename__ = "diagnoses"

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  encounter_id = Column(
      UUID(
          as_uuid=True),
      ForeignKey(
          "clinical_encounters.id",
          ondelete="CASCADE"),
      nullable=False)
  diagnosis_description = Column(Text, nullable=False)
  diagnosed_by_id = Column(
      UUID(
          as_uuid=True), ForeignKey(
          "staffs.id", ondelete="SET NULL"), nullable=True)
  diagnosed_at = Column(
      TIMESTAMP(timezone=True),
      server_default=func.now(),
      nullable=False
  )
  notes = Column(Text, nullable=True)
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
    return f"<DiagnosisModel(id='{self.id}', encounter_id='{self.encounter_id}', diagnosis_description='{self.diagnosis_description[:30]}...')>"
