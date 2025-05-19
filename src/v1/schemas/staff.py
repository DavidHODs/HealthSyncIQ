import uuid

from pydantic import BaseModel, EmailStr
from typing_extensions import List, Optional


class DepartmentRequestSchema(BaseModel):
  id: uuid.UUID


class StaffDepartmentResponseSchema(BaseModel):
  id: uuid.UUID
  name: str
  description: Optional[str] = None


class StaffCreateRequestSchema(BaseModel):
  email: EmailStr
  title: str
  surname: str
  first_name: str
  last_name: Optional[str] = None
  role: str
  departments: List[DepartmentRequestSchema]

  class Config:
    extra = "forbid"
    json_schema_extra = {
        "example": {
            "email": "jane.doe@example.com",
            "title": "Dr.",
            "surname": "Doe",
            "first_name": "Jane",
            "last_name": "Smith",
            "role": "Pharmacist",
            "departments": [
                {
                    "id": "123e4567-e89b-12d3-a456-426614174000"
                }
            ]
        }
    }


class StaffUpdateRequestSchema(BaseModel):
  email: Optional[EmailStr] = None
  title: Optional[str] = None
  surname: Optional[str] = None
  first_name: Optional[str] = None
  last_name: Optional[str] = None
  role: Optional[str] = None
  departments: Optional[List[DepartmentRequestSchema]] = None

  class Config:
    extra = "forbid"
    json_schema_extra = {
        "example": {
            "email": "jane.doe@example.com",
            "title": "Dr.",
            "surname": "Doe",
            "first_name": "Jane",
            "last_name": "Smith",
            "role": "Pharmacist",
            "departments": [
                {
                    "id": "123e4567-e89b-12d3-a456-426614174000"
                }
            ]
        }
    }


class StaffResponseSchema(BaseModel):
  id: uuid.UUID
  email: EmailStr
  title: str
  surname: str
  first_name: str
  last_name: Optional[str] = None
  role: str
  departments: List[StaffDepartmentResponseSchema]

  class Config:
    extra = "forbid"
    json_schema_extra = {
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
    }
