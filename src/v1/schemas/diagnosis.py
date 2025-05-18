import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

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
