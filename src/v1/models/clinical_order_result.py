import uuid

from sqlalchemy import Column, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .base import Base


class ClinicalOrderResultModel(Base):
  __tablename__ = "clinical_order_results"

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  order_id = Column(
      UUID(
          as_uuid=True),
      ForeignKey(
          "clinical_orders.id",
          ondelete="CASCADE"),
      nullable=False)
  result_type = Column(String(50), nullable=False)
  result_data = Column(JSONB, nullable=False)
  result_notes = Column(Text, nullable=True)
  file_attachments = Column(JSONB, nullable=True)
  performed_by_id = Column(
      UUID(
          as_uuid=True), ForeignKey(
          "staffs.id", ondelete="SET NULL"), nullable=True)
  verified_by_id = Column(
      UUID(
          as_uuid=True), ForeignKey(
          "staffs.id", ondelete="SET NULL"), nullable=True)
  performed_at = Column(TIMESTAMP(timezone=True), nullable=True)
  verified_at = Column(TIMESTAMP(timezone=True), nullable=True)
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
    return f"<ClinicalOrderResultModel(id='{self.id}', order_id='{self.order_id}', result_type='{self.result_type}')>"
