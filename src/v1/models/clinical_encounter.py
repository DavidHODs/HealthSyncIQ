import datetime
import uuid

from sqlalchemy import ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing_extensions import Optional

from .base import Base
from .patient import PatientModel
from .staff import StaffModel


class ClinicalEncounterModel(Base):
  __tablename__ = "clinical_encounters"

  id: Mapped[uuid.UUID] = mapped_column(
      UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  patient_id: Mapped[uuid.UUID] = mapped_column(
      UUID(as_uuid=True),
      ForeignKey("patients.id", ondelete="CASCADE"),
      nullable=False
  )
  encounter_type: Mapped[str] = mapped_column(String(50), nullable=False)
  presenting_complaint: Mapped[Optional[str]
                               ] = mapped_column(Text, nullable=True)
  start_date: Mapped[datetime.datetime] = mapped_column(
      nullable=False,
      server_default=func.now()
  )
  end_date: Mapped[Optional[datetime.datetime]] = mapped_column(nullable=True)
  attending_doctor_id: Mapped[uuid.UUID] = mapped_column(
      UUID(as_uuid=True),
      ForeignKey("staffs.id", ondelete="RESTRICT"),
      nullable=False
  )
  status: Mapped[str] = mapped_column(
      String(50), nullable=False, default='Active')
  created_at: Mapped[datetime.datetime] = mapped_column(
      nullable=False,
      server_default=func.now()
  )
  updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(
      nullable=True,
      server_default=func.now(),
      onupdate=func.now()
  )
  deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(nullable=True)

  staff: Mapped["StaffModel"] = relationship(
      "StaffModel",
      lazy="selectin",
      uselist=False,
      foreign_keys=[attending_doctor_id],
  )
  patient: Mapped["PatientModel"] = relationship(
      "PatientModel",
      lazy="selectin",
      uselist=False,
      foreign_keys=[patient_id],
  )

  def __repr__(self) -> str:
    return f"<ClinicalEncounterModel(id='{self.id}', patient_id='{self.patient_id}', encounter_type='{self.encounter_type}')>"
