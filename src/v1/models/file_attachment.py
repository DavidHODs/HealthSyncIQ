import uuid

from sqlalchemy import BigInteger, Column, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .base import Base


class FileAttachmentModel(Base):
  __tablename__ = "file_attachments"
  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  related_entity_type = Column(String(50), nullable=False)
  related_entity_id = Column(UUID(as_uuid=True), nullable=False)
  file_name = Column(String(255), nullable=False)
  file_path = Column(String(512), nullable=False)
  file_type = Column(String(100), nullable=False)
  file_size = Column(BigInteger, nullable=False)

  uploaded_by_id = Column(
      UUID(
          as_uuid=True), ForeignKey(
          "staffs.id", ondelete="SET NULL"), nullable=True)

  uploaded_at = Column(
      TIMESTAMP(timezone=True),
      server_default=func.now(),
      nullable=False
  )
  description = Column(Text, nullable=True)

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
    return f"<FileAttachmentModel(id='{self.id}', file_name='{self.file_name}', related_entity_type='{self.related_entity_type}')>"
