import uuid
from datetime import datetime

from pydantic import BaseModel
from typing_extensions import Optional

from .clinical_encounter import ClinicalEncounterResponseSchema
from .staff import StaffResponseSchema


class DiagnosisSchema(BaseModel):
  id: Optional[uuid.UUID] = None
  encounter: ClinicalEncounterResponseSchema
  diagnosis_description: str
  diagnosed_by: StaffResponseSchema
  diagnosed_at: datetime
  notes: str
  created_at: datetime

  class Config:
    from_attributes = True
