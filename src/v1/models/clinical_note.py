import datetime
import uuid

from sqlalchemy import ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from typing_extensions import Optional

from .base import Base
from .staff import StaffModel


class ClinicalNoteModel(Base):
  __tablename__ = "clinical_notes"

  id: Mapped[uuid.UUID] = mapped_column(
      UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  encounter_id: Mapped[uuid.UUID] = mapped_column(
      UUID(as_uuid=True),
      ForeignKey("clinical_encounters.id", ondelete="CASCADE"),
      nullable=False
  )
  note_type: Mapped[str] = mapped_column(String(50), nullable=False)
  note_content: Mapped[str] = mapped_column(Text, nullable=False)
  note_author_id: Mapped[uuid.UUID] = mapped_column(
      UUID(as_uuid=True),
      ForeignKey("staffs.id", ondelete="CASCADE"),
      nullable=False
  )
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
      foreign_keys=[note_author_id],
  )

  def __repr__(self) -> str:
    return f"<ClinicalNoteModel(id='{self.id}', encounter_id='{self.encounter_id}', note_type='{self.note_type}')>"
