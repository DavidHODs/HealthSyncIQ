import uuid

from pydantic import BaseModel
from typing_extensions import Optional

from .department import DepartmentResponseSchema
from .staff import StaffSchema


class DepartmentMembershipSchema(BaseModel):
  id: Optional[uuid.UUID] = None
  staff_id: StaffSchema
  department: DepartmentResponseSchema

  class Config:
    from_attributes = True
