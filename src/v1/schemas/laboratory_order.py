import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from .clinical_order import ClinicalOrderIdRef


class LaboratoryStaffDepartmentResponse(BaseModel):
  id: uuid.UUID
  name: str

  class Config:
    extra = "forbid"
    json_schema_extra = {
        "example": {"id": "123e4567-e89b-12d3-a456-426614174000", "name": "Pharmacy"}
    }


class LaboratoryStaffResponse(BaseModel):
  id: uuid.UUID
  title: str
  name: str
  departments: List[LaboratoryStaffDepartmentResponse]

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


class LaboratoryOrderCreateRequestSchema(BaseModel):
  order: ClinicalOrderIdRef
  result_type: str
  result_data: Dict[str, Any]
  result_notes: Optional[str] = None
  file_attachments: Optional[List[Dict[str, Any]]] = None
  performed_at: Optional[datetime] = None

  class Config:
    extra = "forbid"
    json_schema_extra = {
        "example":
            {
                "order": {"id": "00000000-0000-0000-0000-000000000001"},
                "result_type": "Blood Test",
                "result_data": {"test_name": "CBC", "hemoglobin": "14.2 g/dL"},
                "result_notes": "Routine check-up results.",
                "performed_at": "2025-06-17T10:00:00Z"
            }
    }


class LaboratoryOrderUpdateRequestSchema(BaseModel):
  result_type: Optional[str] = None
  result_data: Optional[Dict[str, Any]] = None
  result_notes: Optional[str] = None
  file_attachments: Optional[List[Dict[str, Any]]] = None
  performed_by: Optional[ClinicalOrderIdRef] = None
  performed_at: Optional[datetime] = None
  verified_by: Optional[ClinicalOrderIdRef] = None
  verified_at: Optional[datetime] = None

  class Config:
    extra = "forbid"
    json_schema_extra = {
        "example":
            {
                "result_data": {"test_name": "CBC", "hemoglobin": "14.5 g/dL", "status": "Final"},
                "result_notes": "Updated after re-analysis.",
                "verified_by": {"id": "abcde123-4567-890a-bcde-f12345678902"},
                "verified_at": "2025-06-17T11:30:00Z"
            }

    }


class LaboratoryOrderResponseSchema(BaseModel):
  id: uuid.UUID
  order: ClinicalOrderIdRef
  result_type: str
  result_data: Dict[str, Any]
  result_notes: Optional[str] = None
  file_attachments: Optional[List[Dict[str, Any]]] = None
  performed_by: LaboratoryStaffResponse
  verified_by: Optional[LaboratoryStaffResponse] = None
  performed_at: Optional[datetime] = None
  verified_at: Optional[datetime] = None
  created_at: datetime
  updated_at: Optional[datetime] = None
  deleted_at: Optional[datetime] = None

  class Config:
    from_attributes = True
    json_schema_extra = {
        "example":
            {
                "id": "e0e0e0e0-e0e0-e0e0-e0e0-e0e0e0e0e0e0",
                "order": {"id": "00000000-0000-0000-0000-000000000001"},
                "result_type": "Blood Test",
                "result_data": {"test_name": "CBC", "hemoglobin": "14.2 g/dL", "wbc": "8.5 x10^9/L"},
                "result_notes": "Routine check-up results.",
                "performed_by": {
                    "id": "fedcba98-7654-3210-fedc-ba9876543210",
                    "title": "Lab Tech",
                    "name": "Alice Smith",
                    "departments": [
                        {"id": "789f0123-4567-890a-bcde-f12345678901",
                          "name": "Pathology"}
                    ]
                },
                "verified_by": None,
                "performed_at": "2025-06-17T10:00:00Z",
                "verified_at": None,
                "created_at": "2025-06-17T10:15:00Z",
                "updated_at": None,
                "deleted_at": None
            }
    }
