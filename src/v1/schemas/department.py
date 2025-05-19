import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

    
class DepartmentCreateRequestSchema(BaseModel):
  name: str
  description: str

  class Config:
    extra = "forbid"
    json_schema_extra = {
        "name": "Pharmacy",
        "description": "Responsible for dispensing drugs"
    }
    
class DepartmentUpdateRequestSchema(BaseModel):
  name: Optional[str] = None
  description: Optional[str] = None

  class Config:
    extra = "forbid"
    json_schema_extra = {
        "name": "Pharmacy",
        "description": "Responsible for dispensing drugs"
    }


class DepartmentResponseSchema(BaseModel):
  id: uuid.UUID
  name: str
  description: Optional[str] = None
  created_at: Optional[datetime] = None
  updated_at: Optional[datetime] = None

  class Config:
    json_schema_extra = {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "name": "Pharmacy",
        "description": "Responsible for dispensing drugs",
        "created_at": "2025-05-17 22:22:25.000 +0100",
        "updated_at": None
    }

    from_attributes = True

