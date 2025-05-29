import datetime
import uuid

from sqlalchemy import ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from typing_extensions import Optional

from .base import Base
from .clinical_encounter import ClinicalEncounterModel
from .staff import StaffModel


class DiagnosisModel(Base):
  __tablename__ = "diagnoses"

  id: Mapped[uuid.UUID] = mapped_column(
      UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  encounter_id: Mapped[uuid.UUID] = mapped_column(
      UUID(as_uuid=True),
      ForeignKey("clinical_encounters.id", ondelete="CASCADE"),
      nullable=False
  )
  diagnosis_description: Mapped[str] = mapped_column(Text, nullable=False)
  diagnosed_by_id: Mapped[uuid.UUID | None] = mapped_column(
      UUID(as_uuid=True),
      ForeignKey("staffs.id", ondelete="SET NULL"),
      nullable=True
  )
  notes: Mapped[str | None] = mapped_column(Text, nullable=True)
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

  staff: Mapped["StaffModel"] = relationship(
      "StaffModel",
      lazy="selectin",
      uselist=False,
      foreign_keys=[diagnosed_by_id],
  )
  encounter: Mapped["ClinicalEncounterModel"] = relationship(
      "PatientModel",
      lazy="selectin",
      uselist=False,
      foreign_keys=[encounter_id],
  )

  def __repr__(self) -> str:
    return f"<DiagnosisModel(id='{self.id}', encounter_id='{self.encounter_id}', diagnosis_description='{self.diagnosis_description[:30]}...')>"
