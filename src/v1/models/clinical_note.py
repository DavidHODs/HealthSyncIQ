import uuid

from sqlalchemy import Column, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .base import Base


class ClinicalNoteModel(Base):
  __tablename__ = "clinical_notes"

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  encounter_id = Column(
      UUID(
          as_uuid=True),
      ForeignKey(
          "clinical_encounters.id",
          ondelete="CASCADE"),
      nullable=False)
  note_type = Column(String(50), nullable=False)
  note_content = Column(Text, nullable=False)
  staff_id = Column(
      UUID(
          as_uuid=True),
      ForeignKey(
          "staffs.id",
          ondelete="CASCADE"),
      nullable=False)
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
    return f"<ClinicalNoteModel(id='{self.id}', encounter_id='{self.encounter_id}', note_type='{self.note_type}')>"
