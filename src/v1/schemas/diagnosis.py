import uuid
from datetime import datetime

from pydantic import BaseModel
from typing_extensions import Optional

from .clinical_encounter import ClinicalEncounterSchema
from .staff import StaffSchema


class DiagnosisSchema(BaseModel):
  id: Optional[uuid.UUID] = None
  encounter: ClinicalEncounterSchema
  diagnosis_description: str
  diagnosed_by: StaffSchema
  diagnosed_at: datetime
  notes: str
  created_at: Optional[datetime] = None

  class Config:
    from_attributes = True
