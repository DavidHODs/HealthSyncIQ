import uuid
import datetime
from typing import Optional

from sqlalchemy import ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class ClinicalEncounterModel(Base):
    __tablename__ = "clinical_encounters"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False
    )
    encounter_type: Mapped[str] = mapped_column(String(50), nullable=False)
    presenting_complaint: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    start_date: Mapped[datetime.datetime] = mapped_column(
        nullable=False,
        server_default=func.now()
    )
    end_date: Mapped[Optional[datetime.datetime]] = mapped_column(nullable=True)
    attending_doctor_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("staffs.id", ondelete="SET NULL"),
        nullable=True
    )
    status: Mapped[str] = mapped_column(String(50), nullable=False, default='Active')
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

    def __repr__(self) -> str:
        return f"<ClinicalEncounterModel(id='{self.id}', patient_id='{self.patient}', encounter_type='{self.encounter_type}')>"
