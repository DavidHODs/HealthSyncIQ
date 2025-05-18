import uuid

from sqlalchemy import Column, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID  # Import JSONB
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .base import Base


class ClinicalOrderModel(Base):
  __tablename__ = "clinical_orders"

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

  encounter_id = Column(
      UUID(
          as_uuid=True),
      ForeignKey(
          "clinical_encounters.id",
          ondelete="CASCADE"),
      nullable=False)
  order_type = Column(String(50), nullable=False)
  order_details = Column(JSONB, nullable=False)
  ordering_department_id = Column(
      UUID(
          as_uuid=True), ForeignKey(
          "departments.id", ondelete="SET NULL"), nullable=True)
  target_department_id = Column(
      UUID(
          as_uuid=True), ForeignKey(
          "departments.id", ondelete="SET NULL"), nullable=True)
  ordered_by_id = Column(
      UUID(
          as_uuid=True), ForeignKey(
          "staffs.id", ondelete="CASCADE"), nullable=False)
  priority = Column(String(50), nullable=False, default='Routine')
  status = Column(String(50), nullable=False, default='Ordered')
  order_notes = Column(Text, nullable=True)
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
    return f"<ClinicalOrderModel(id='{self.id}', encounter_id='{self.encounter_id}', order_type='{self.order_type}')>"
