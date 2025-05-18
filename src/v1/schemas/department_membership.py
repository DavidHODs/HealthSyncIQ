import uuid
from typing import Optional

from pydantic import BaseModel

from .department import DepartmentSchema
from .staff import StaffSchema


class DepartmentMembershipSchema(BaseModel):
  id: Optional[uuid.UUID] = None
  staff_id: StaffSchema
  department: DepartmentSchema

  class Config:
    from_attributes = True
