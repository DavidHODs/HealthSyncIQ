import uuid

from sqlalchemy import Column, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .base import Base


class MedicationDispensingModel(Base):
  __tablename__ = "medication_dispensing"

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  order_id = Column(
      UUID(
          as_uuid=True),
      ForeignKey(
          "clinical_orders.id",
          ondelete="CASCADE"),
      nullable=False)
  medication_name = Column(String(255), nullable=False)
  dosage = Column(String(100), nullable=False)
  quantity_ordered = Column(Integer, nullable=False)
  quantity_dispensed = Column(Integer, nullable=True)
  status = Column(String(50), nullable=False, default='Pending')
  dispensed_by_id = Column(
      UUID(
          as_uuid=True), ForeignKey(
          "staffs.id", ondelete="SET NULL"), nullable=True)
  dispensed_at = Column(TIMESTAMP(timezone=True), nullable=True)
  pharmacy_notes = Column(Text, nullable=True)
  patient_instructions = Column(Text, nullable=True)
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
    return f"<MedicationDispensingModel(id='{self.id}', order_id='{self.order_id}', medication='{self.medication_name}')>"
