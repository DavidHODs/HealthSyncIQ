import uuid
from datetime import datetime

from pydantic import BaseModel
from typing_extensions import Optional

from .department import DepartmentResponseSchema
from .patient import PatientSchema
from .staff import StaffSchema


class ClinicalEncounterSchema(BaseModel):
  id: Optional[uuid.UUID] = None
  patient: PatientSchema
  encounter_type: str
  presenting_complaint: Optional[str] = None
  start_date: datetime
  end_date: Optional[datetime] = None
  attending_doctor: StaffSchema
  department: DepartmentResponseSchema
  status: str
  created_at: Optional[datetime] = None

  class Config:
    from_attributes = True
