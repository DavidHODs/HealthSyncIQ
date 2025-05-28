import uuid
from datetime import datetime

from pydantic import BaseModel
from typing_extensions import Optional

from .clinical_encounter import ClinicalEncounterResponseSchema
from .staff import StaffResponseSchema


class ClinicalNoteSchema(BaseModel):
  id: Optional[uuid.UUID] = None
  encounter: ClinicalEncounterResponseSchema
  note_type: str
  note_content: str
  staff: StaffResponseSchema
  created_at: datetime
  updated_at: Optional[datetime] = None
  deleted_at: Optional[datetime] = None

  class Config:
    from_attributes = True
