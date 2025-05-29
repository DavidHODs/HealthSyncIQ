import uuid
from datetime import datetime

from pydantic import BaseModel
from typing_extensions import Optional

from .staff import StaffResponseSchema


class PatientIdSchema(BaseModel):
  id: uuid.UUID


class ClinicalEncounterCreateRequestSchema(BaseModel):
  patient: PatientIdSchema
  encounter_type: str
  presenting_complaint: Optional[str] = None
  status: str

  class Config:
    extra = "forbid"
    json_schema_extra = {
        "example": {
            "patient": {
                "id": "123e4567-e89b-12d3-a456-426614174001"
            },
            "encounter_type": "Consultation",
            "presenting_complaint": "Fever and cough",
            "status": "active"
        }
    }


class ClinicalEncounterUpdateRequestSchema(BaseModel):
  encounter_type: Optional[str] = None
  presenting_complaint: Optional[str] = None
  status: Optional[str] = None

  class Config:
    extra = "forbid"
    json_schema_extra = {
        "example": {
            "encounter_type": "Consultation",
            "presenting_complaint": "Fever and cough",
            "status": "active"
        }
    }


class ClinicalEncounterResponseSchema(BaseModel):
  id: uuid.UUID
  encounter_type: str
  presenting_complaint: Optional[str] = None
  start_date: datetime
  end_date: Optional[datetime] = None
  attending_doctor: StaffResponseSchema
  status: str
  created_at: datetime

  class Config:
    from_attributes = True
    json_schema_extra = {
        "example": {
            "id": "123e4567-e89b-12d3-a456-426614174004",
            "encounter_type": "Consultation",
            "presenting_complaint": "Fever and cough",
            "start_date": "2025-05-17T10:00:00Z",
            "end_date": None,
            "attending_doctor": {
                "id": "123e4567-e89b-12d3-a456-426614174001",
                "email": "jane.doe@example.com",
                "title": "Dr.",
                "surname": "Doe",
                "first_name": "Jane",
                "last_name": "Smith",
                "role": "Pharmacist",
                "departments": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "name": "Pharmacy",
                        "description": "Handles all pharmaceutical needs"
                    }
                ]
            },
            "status": "active",
            "created_at": "2025-05-17T10:00:00Z"
        }
    }
