import uuid
from datetime import datetime

from pydantic import BaseModel
from typing_extensions import Any, Dict, Optional

from .clinical_encounter import ClinicalEncounterSchema
from .department import DepartmentResponseSchema
from .staff import StaffResponseSchema


class ClinicalOrderSchema(BaseModel):
  id: Optional[uuid.UUID] = None
  encounter: ClinicalEncounterSchema
  order_type: str
  order_details: Dict[str, Any]
  ordering_department: DepartmentResponseSchema
  target_department: DepartmentResponseSchema
  ordered_by: StaffResponseSchema
  priority: str
  status: str
  order_notes: str
  created_at: Optional[datetime] = None

  class Config:
    from_attributes = True
