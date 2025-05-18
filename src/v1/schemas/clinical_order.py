import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel

from .clinical_encounter import ClinicalEncounterSchema
from .department import DepartmentSchema
from .staff import StaffSchema


class ClinicalOrderSchema(BaseModel):
  id: Optional[uuid.UUID] = None
  encounter: ClinicalEncounterSchema
  order_type: str
  order_details: Dict[str, Any]
  ordering_department: DepartmentSchema
  target_department: DepartmentSchema
  ordered_by: StaffSchema
  priority: str
  status: str
  order_notes: str
  created_at: Optional[datetime] = None

  class Config:
    from_attributes = True
