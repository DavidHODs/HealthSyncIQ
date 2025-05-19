import uuid
from datetime import datetime

from pydantic import BaseModel
from typing_extensions import Optional

from .clinical_encounter import ClinicalEncounterSchema
from .staff import StaffResponseSchema


class ClinicalNoteSchema(BaseModel):
  id: Optional[uuid.UUID] = None
  encounter: ClinicalEncounterSchema
  note_type: str
  note_content: str
  staff: StaffResponseSchema
  created_at: Optional[datetime] = None
  updated_at: Optional[datetime] = None
  deleted_at: Optional[datetime] = None

  class Config:
    from_attributes = True
