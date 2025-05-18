import uuid

from sqlalchemy import Boolean, Column, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .base import Base


class NursingTaskModel(Base):
  __tablename__ = "nursing_tasks"

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  order_id = Column(
      UUID(
          as_uuid=True),
      ForeignKey(
          "clinical_orders.id",
          ondelete="CASCADE"),
      nullable=False)
  task_type = Column(String(100), nullable=False)
  instructions = Column(Text, nullable=False)
  frequency = Column(String(100), nullable=True)
  status = Column(String(50), nullable=False, default='Pending')
  assigned_to_id = Column(
      UUID(
          as_uuid=True), ForeignKey(
          "staffs.id", ondelete="SET NULL"), nullable=True)
  performed_by_id = Column(
      UUID(
          as_uuid=True), ForeignKey(
          "staffs.id", ondelete="SET NULL"), nullable=True)
  performed_at = Column(TIMESTAMP(timezone=True), nullable=True)
  verification_required = Column(Boolean, nullable=False, default=False)
  verified_by_id = Column(
      UUID(
          as_uuid=True), ForeignKey(
          "staffs.id", ondelete="SET NULL"), nullable=True)
  verified_at = Column(TIMESTAMP(timezone=True), nullable=True)
  result_notes = Column(Text, nullable=True)
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
    return f"<NursingTaskModel(id='{self.id}', order_id='{self.order_id}', task_type='{self.task_type}')>"
