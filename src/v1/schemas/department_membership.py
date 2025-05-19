import uuid

from pydantic import BaseModel
from typing_extensions import Optional

from .department import DepartmentResponseSchema
from .staff import StaffResponseSchema


class DepartmentMembershipSchema(BaseModel):
  id: Optional[uuid.UUID] = None
  staff_id: StaffResponseSchema
  department: DepartmentResponseSchema

  class Config:
    from_attributes = True
