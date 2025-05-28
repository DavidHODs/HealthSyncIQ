import uuid
from datetime import date, datetime

from pydantic import BaseModel, EmailStr
from typing_extensions import Optional


class PatientCreateRequestSchema(BaseModel):
  surname: str
  first_name: str
  last_name: Optional[str] = None
  dob: Optional[date] = None
  genotype: Optional[str] = None
  blood_group: Optional[str] = None
  gender: Optional[str] = None
  contact_information: Optional[str] = None
  emergency_contact: Optional[str] = None
  email: EmailStr
  phone_number: Optional[str] = None

  class Config:
    extra = "forbid"
    json_schema_extra = {
        "example": {
            "surname": "Doe",
            "first_name": "John",
            "last_name": "Smith",
            "dob": "1990-01-01",
            "genotype": "AA",
            "blood_group": "O+",
            "gender": "Male",
            "contact_information": "+1234567890",
            "emergency_contact": "+0987654321",
            "email": "john.doe@example.com",
            "phone_number": "+1122334455"
        }
    }
    from_attributes = True


class PatientUpdateRequestSchema(BaseModel):
  surname: Optional[str] = None
  first_name: Optional[str] = None
  last_name: Optional[str] = None
  dob: Optional[date] = None
  genotype: Optional[str] = None
  blood_group: Optional[str] = None
  gender: Optional[str] = None
  contact_information: Optional[str] = None
  emergency_contact: Optional[str] = None
  email: Optional[EmailStr] = None
  phone_number: Optional[str] = None

  class Config:
    extra = "forbid"
    json_schema_extra = {
        "example": {
            "surname": "Doe",
            "first_name": "John",
            "last_name": "Smith",
            "dob": "1990-01-01",
            "genotype": "AA",
            "blood_group": "O+",
            "gender": "Male",
            "contact_information": "+1234567890",
            "emergency_contact": "+0987654321",
            "email": "john.doe@example.com",
            "phone_number": "+1122334455"
        }
    }
    from_attributes = True


class PatientResponseSchema(BaseModel):
  id: uuid.UUID
  registration_code: str
  surname: str
  first_name: str
  last_name: Optional[str] = None
  dob: Optional[date] = None
  genotype: Optional[str] = None
  blood_group: Optional[str] = None
  gender: Optional[str] = None
  contact_information: Optional[str] = None
  emergency_contact: Optional[str] = None
  email: EmailStr
  phone_number: Optional[str] = None
  created_at: datetime
  updated_at: Optional[datetime] = None

  class Config:
    json_schema_extra = {
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
        "email": "john.doe@example.com",
        "phone_number": "+1122334455",
        "created_at": "2025-05-17T22:22:25+01:00",
        "updated_at": None
    }
    from_attributes = True
