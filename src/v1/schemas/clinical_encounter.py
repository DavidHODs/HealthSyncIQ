import uuid
from datetime import datetime

from pydantic import BaseModel
from typing_extensions import Optional

from .department import DepartmentResponseSchema
from .patient import PatientResponseSchema
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
      "patient": {
        "id": "123e4567-e89b-12d3-a456-426614174001"
      },
      "encounter_type": "Consultation",
      "presenting_complaint": "Fever and cough",
      "status": "active"
    }


class ClinicalEncounterUpdateRequestSchema(BaseModel):
  encounter_type: Optional[str] = None
  presenting_complaint: Optional[str] = None
  status: Optional[str] = None

  class Config:
    extra = "forbid"
    json_schema_extra = {
      "encounter_type": "Consultation",
      "presenting_complaint": "Fever and cough",
      "status": "active"
    }


class ClinicalEncounterResponseSchema(BaseModel):
  id: uuid.UUID
  patient: PatientResponseSchema
  encounter_type: str
  presenting_complaint: Optional[str] = None
  start_date: datetime
  end_date: Optional[datetime] = None
  attending_doctor: StaffResponseSchema
  department: DepartmentResponseSchema
  status: str
  created_at: datetime

  class Config:
    from_attributes = True
    json_schema_extra = {
      "id": "123e4567-e89b-12d3-a456-426614174004",
      "patient": {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "registration_number": "HS123456",
        "surname": "Doe",
        "first_name": "John",
        "last_name": "Smith",
        "dob": "1990-01-01",
        "genotype": "AA",
        "blood_group": "O+",
        "gender": "Male",
        "contact_information": "+1234567890",
        "emergency_contact": "+0987654321",
        "created_at": "2025-05-17T22:22:25+01:00",
        "updated_at": None
      },
      "encounter_type": "Consultation",
      "presenting_complaint": "Fever and cough",
      "start_date": "2025-05-17T10:00:00Z",
      "end_date": None,
      "attending_doctor": {
        "example": {
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
        }
      },
      "status": "active",
      "created_at": "2025-05-17T10:00:00Z"
    }
