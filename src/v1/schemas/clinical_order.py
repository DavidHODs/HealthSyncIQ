import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class ClinicalOrderIdRef(BaseModel):
  id: uuid.UUID

  class Config:
    extra = "forbid"
    json_schema_extra = {
        "example": {"id": "a1b2c3d4-e5f6-7890-1234-567890abcdef"}
    }


class ClinicalOrderStaffDepartmentResponse(BaseModel):
  id: uuid.UUID
  name: str

  class Config:
    extra = "forbid"
    json_schema_extra = {
        "example": {"id": "123e4567-e89b-12d3-a456-426614174000", "name": "Pharmacy"}
    }


class ClinicalOrderOrderedByStaffResponse(BaseModel):
  id: uuid.UUID
  title: str
  name: str
  departments: List[ClinicalOrderStaffDepartmentResponse]

  class Config:
    extra = "forbid"
    json_schema_extra = {
        "example": {
            "id": "fedcba98-7654-3210-fedc-ba9876543210",
            "title": "Dr.",
            "name": "John Doe",
            "departments": [
                {"id": "123e4567-e89b-12d3-a456-426614174000", "name": "Pharmacy"}
            ]
        }
    }


class ClinicalOrderCreateRequestSchema(BaseModel):
  encounter: ClinicalOrderIdRef
  order_type: str
  order_details: Dict[str, Any]
  target_department: ClinicalOrderIdRef
  priority: str
  order_notes: Optional[str] = None

  class Config:
    extra = "forbid"
    json_schema_extra = {
        "examples": [
            {
                "encounter": {"id": "a1b2c3d4-e5f6-7890-1234-567890abcdef"},
                "order_type": "Medication Order",
                "order_details": {"medication": "Amoxicillin", "dosage": "250mg", "frequency": "TID"},
                "target_department": {"id": "123e4567-e89b-12d3-a456-426614174000"},
                "priority": "High",
                "order_notes": "Patient has penicillin allergy, administer with caution."
            }
        ]
    }


class ClinicalOrderUpdateRequestSchema(BaseModel):
  order_type: Optional[str] = None
  order_details: Optional[Dict[str, Any]] = None
  target_department: Optional[ClinicalOrderIdRef] = None
  priority: Optional[str] = None
  status: Optional[str] = None
  order_notes: Optional[str] = None

  class Config:
    extra = "forbid"
    json_schema_extra = {
        "examples": [
            {
                "status": "Completed",
                "order_notes": "Medication dispensed and administered."
            },
            {
                "priority": "Urgent",
                "target_department": {"id": "abcdef12-3456-7890-abcd-ef1234567890"},
                "order_details": {"medication": "Amoxicillin", "dosage": "500mg", "frequency": "BID"}
            }
        ]
    }


class ClinicalOrderResponseSchema(BaseModel):
  id: uuid.UUID
  encounter: ClinicalOrderIdRef
  order_type: str
  order_details: Dict[str, Any]
  target_department: ClinicalOrderIdRef
  ordered_by: ClinicalOrderOrderedByStaffResponse
  priority: str
  status: str
  order_notes: Optional[str] = None
  created_at: datetime
  updated_at: Optional[datetime] = None

  class Config:
    from_attributes = True
    json_schema_extra = {
        "examples": [
            {
                "id": "00000000-0000-0000-0000-000000000001",
                "encounter": {"id": "a1b2c3d4-e5f6-7890-1234-567890abcdef"},
                "order_type": "Medication Order",
                "order_details": {"medication": "Amoxicillin", "dosage": "250mg", "frequency": "TID"},
                "target_department": {"id": "123e4567-e89b-12d3-a456-426614174000"},
                "ordered_by": {
                    "id": "fedcba98-7654-3210-fedc-ba9876543210",
                    "title": "Dr.",
                    "name": "Jane Doe",
                    "departments": [
                        {"id": "123e4567-e89b-12d3-a456-426614174000", "name": "Pharmacy"}
                    ]
                },
                "priority": "High",
                "status": "Pending",
                "order_notes": "Patient has penicillin allergy, administer with caution.",
                "created_at": "2025-06-17T12:34:53Z",
                "updated_at": None
            }
        ]
    }
