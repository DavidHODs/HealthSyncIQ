import datetime
import uuid

from sqlalchemy import ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing_extensions import Any, Dict, List, Optional

from .base import Base
from .clinical_order import ClinicalOrderModel
from .staff import StaffModel


class LaboratoryOrderModel(Base):
  __tablename__ = "laboratory_orders"

  id: Mapped[uuid.UUID] = mapped_column(
      UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
  )
  order_id: Mapped[uuid.UUID] = mapped_column(
      UUID(as_uuid=True),
      ForeignKey("clinical_orders.id", ondelete="CASCADE"),
      nullable=False
  )
  result_type: Mapped[str] = mapped_column(String(50), nullable=False)
  result_data: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
  result_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
  file_attachments: Mapped[Optional[List[Dict[str, Any]]]
                           ] = mapped_column(JSONB, nullable=True)
  performed_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
      UUID(as_uuid=True),
      ForeignKey("staffs.id", ondelete="SET NULL"),
      nullable=True
  )
  verified_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
      UUID(as_uuid=True),
      ForeignKey("staffs.id", ondelete="SET NULL"),
      nullable=True
  )
  performed_at: Mapped[Optional[datetime.datetime]
                       ] = mapped_column(nullable=True)
  verified_at: Mapped[Optional[datetime.datetime]
                      ] = mapped_column(nullable=True)
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

  order: Mapped["ClinicalOrderModel"] = relationship(
      "ClinicalOrderModel",
      lazy="selectin",
      uselist=False,
      foreign_keys=[order_id],
  )

  performed_by: Mapped[Optional["StaffModel"]] = relationship(
      "StaffModel",
      lazy="selectin",
      uselist=False,
      foreign_keys=[performed_by_id],
  )

  verified_by: Mapped[Optional["StaffModel"]] = relationship(
      "StaffModel",
      lazy="selectin",
      uselist=False,
      foreign_keys=[verified_by_id],
  )

  def __repr__(self) -> str:
    return f"<LaboratoryOrderModel(id='{self.id}', order_id='{self.order_id}', result_type='{self.result_type}')>"
