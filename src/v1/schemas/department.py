import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DepartmentSchema(BaseModel):
  id: Optional[uuid.UUID] = None
  name: str
  description: Optional[str] = None
  created_at: Optional[datetime] = None
  updated_at: Optional[datetime] = None
  deleted_at: Optional[datetime] = None

  class Config:
    from_attributes = True
