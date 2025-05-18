import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .staff import StaffSchema


class FileAttachmentSchema(BaseModel):
  id: Optional[uuid.UUID] = None
  related_entity_type: str
  related_entity_id: uuid.UUID
  file_name: str
  file_path: str
  file_type: str
  file_size: int
  uploaded_by: StaffSchema
  uploaded_at: datetime
  description: Optional[str] = None
  created_at: Optional[datetime] = None
  updated_at: Optional[datetime] = None
  deleted_at: Optional[datetime] = None

  class Config:
    from_attributes = True
