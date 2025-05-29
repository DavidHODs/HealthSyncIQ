import uuid
from datetime import datetime

from pydantic import BaseModel
from typing_extensions import Optional

from .staff import StaffResponseSchema


class ClinicalEncounterIdSchema(BaseModel):
  id: uuid.UUID


class DiagnosisCreateRequestSchema(BaseModel):
  encounter: ClinicalEncounterIdSchema
  diagnosis_description: str
  notes: Optional[str] = None

  class Config:
    extra = "forbid"
    json_schema_extra = {
        "example": {
            "encounter": {
                "id": "123e4567-e89b-12d3-a456-426614174004"
            },
            "diagnosis_description": "Acute bronchitis",
            "notes": "Patient reports persistent cough."
        }
    }


class DiagnosisUpdateRequestSchema(BaseModel):
  diagnosis_description: Optional[str] = None
  notes: Optional[str] = None

  class Config:
    extra = "forbid"
    json_schema_extra = {
        "example": {
            "diagnosis_description": "Acute bronchitis",
            "notes": "Updated notes."
        }
    }


class DiagnosisResponseSchema(BaseModel):
  id: uuid.UUID
  diagnosis_description: str
  diagnosed_by: StaffResponseSchema
  notes: Optional[str] = None
  created_at: datetime
  updated_at: Optional[datetime] = None

  class Config:
    from_attributes = True
    json_schema_extra = {
        "example": {
            "id": "123e4567-e89b-12d3-a456-426614174005",
            "diagnosis_description": "Acute bronchitis",
            "diagnosed_by": {
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
            "notes": "Patient reports persistent cough.",
            "created_at": "2025-05-17T10:00:00Z",
            "updated_at": "2025-05-18T10:00:00Z"
        }
    }
