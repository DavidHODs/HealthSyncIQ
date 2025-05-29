import uuid
from datetime import datetime

from pydantic import BaseModel
from typing_extensions import Optional

from .staff import StaffResponseSchema


class ClinicalEncounterIdSchema(BaseModel):
  id: uuid.UUID


class ClinicalNoteCreateRequestSchema(BaseModel):
  encounter: ClinicalEncounterIdSchema
  note_type: str
  note_content: str

  class Config:
    extra = "forbid"
    json_schema_extra = {
        "example": {
            "encounter": {
                "id": "123e4567-e89b-12d3-a456-426614174004"
            },
            "note_type": "Progress Note",
            "note_content": "Patient is recovering well post-surgery."
        }
    }


class ClinicalNoteUpdateRequestSchema(BaseModel):
  note_type: Optional[str] = None
  note_content: Optional[str] = None

  class Config:
    extra = "forbid"
    json_schema_extra = {
        "example": {
            "note_type": "Discharge Summary",
            "note_content": "Patient discharged in stable condition."
        }
    }


class ClinicalNoteResponseSchema(BaseModel):
  id: uuid.UUID
  note_type: str
  note_content: str
  note_author: StaffResponseSchema
  created_at: datetime
  updated_at: Optional[datetime] = None

  class Config:
    from_attributes = True
    json_schema_extra = {
        "example": {
            "id": "123e4567-e89b-12d3-a456-426614174006",
            "note_type": "Progress Note",
            "note_content": "Patient is recovering well post-surgery.",
            "note_author": {
                "id": "123e4567-e89b-12d3-a456-426614174001",
                "email": "jane.doe@example.com",
                "title": "Dr.",
                "surname": "Doe",
                "first_name": "Jane",
                "last_name": "Smith",
                "role": "Doctor",
                "departments": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "name": "General Medicine",
                        "description": "Handles general medical cases"
                    }
                ]
            },
            "created_at": "2025-05-17T10:00:00Z",
            "updated_at": "2025-05-18T10:00:00Z"
        }
    }
