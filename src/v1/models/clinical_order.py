import datetime
import uuid

from sqlalchemy import ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing_extensions import Optional

from .base import Base
from .clinical_encounter import ClinicalEncounterModel
from .department import DepartmentModel
from .staff import StaffModel


class ClinicalOrderModel(Base):
  __tablename__ = "clinical_orders"

  id: Mapped[uuid.UUID] = mapped_column(
      UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
  )

  encounter_id: Mapped[uuid.UUID] = mapped_column(
      UUID(as_uuid=True),
      ForeignKey("clinical_encounters.id", ondelete="CASCADE"),
      nullable=False
  )
  order_type: Mapped[str] = mapped_column(String(50), nullable=False)
  order_details: Mapped[dict[str, object]
                        ] = mapped_column(JSONB, nullable=False)
  target_department_id: Mapped[uuid.UUID] = mapped_column(
      UUID(as_uuid=True),
      ForeignKey("departments.id", ondelete="SET NULL"),
      nullable=True
  )
  ordered_by_id: Mapped[uuid.UUID] = mapped_column(
      UUID(as_uuid=True),
      ForeignKey("staffs.id", ondelete="CASCADE"),
      nullable=False
  )
  priority: Mapped[str] = mapped_column(
      String(50), nullable=False, default='Routine')
  status: Mapped[str] = mapped_column(
      String(50), nullable=False, default='Pending')
  order_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
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

  encounter: Mapped["ClinicalEncounterModel"] = relationship(
      "ClinicalEncounterModel",
      lazy="selectin",
      uselist=False,
      foreign_keys=[encounter_id],
  )

  target_department: Mapped[Optional["DepartmentModel"]] = relationship(
      "DepartmentModel",
      lazy="selectin",
      uselist=False,
      foreign_keys=[target_department_id],
  )

  ordered_by: Mapped["StaffModel"] = relationship(
      "StaffModel",
      lazy="selectin",
      uselist=False,
      foreign_keys=[ordered_by_id],
  )

  def __repr__(self) -> str:
    return f"<ClinicalOrderModel(id='{self.id}', encounter_id='{self.encounter_id}', order_type='{self.order_type}')>"
