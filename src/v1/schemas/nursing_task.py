import uuid
from datetime import datetime

from pydantic import BaseModel
from typing_extensions import Optional

from .clinical_order import ClinicalOrderSchema
from .staff import StaffResponseSchema


class NursingTaskSchema(BaseModel):
  id: Optional[uuid.UUID] = None
  order: ClinicalOrderSchema
  task_type: str
  instructions: str
  frequency: str
  status: str
  assigned_to: StaffResponseSchema
  performed_by: StaffResponseSchema
  performed_at: datetime
  verification_required: bool
  verified_by: StaffResponseSchema
  verified_at: Optional[datetime] = None
  result_notes: Optional[str] = None
  created_at: Optional[datetime] = None
  updated_at: Optional[datetime] = None
  deleted_at: Optional[datetime] = None

  class Config:
    from_attributes = True
