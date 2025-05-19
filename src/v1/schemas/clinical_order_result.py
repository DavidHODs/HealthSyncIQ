import uuid
from datetime import datetime

from pydantic import BaseModel
from typing_extensions import Any, Dict, List, Optional

from .clinical_order import ClinicalOrderSchema
from .staff import StaffSchema


class ClinicalOrderResultSchema(BaseModel):
  id: Optional[uuid.UUID] = None
  order: ClinicalOrderSchema
  result_type: str
  result_data: Dict[str, Any]
  result_notes: Optional[str] = None
  file_attachments: Optional[List[Dict[str, Any]]] = None
  performed_by: StaffSchema
  verified_by: StaffSchema
  performed_at: Optional[datetime] = None
  verified_at: Optional[datetime] = None
  created_at: Optional[datetime] = None
  updated_at: Optional[datetime] = None
  deleted_at: Optional[datetime] = None

  class Config:
    from_attributes = True
