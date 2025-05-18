import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .clinical_order import ClinicalOrderSchema
from .staff import StaffSchema


class MedicationDispensingSchema(BaseModel):
  id: Optional[uuid.UUID] = None
  order: ClinicalOrderSchema
  medication_name: str
  dosage: str
  quantity_ordered: int
  quantity_dispensed: Optional[int] = None
  status: str
  dispensed_by: StaffSchema
  dispensed_at: Optional[datetime] = None
  pharmacy_notes: Optional[str] = None
  patient_instructions: Optional[str] = None
  created_at: Optional[datetime] = None
  updated_at: Optional[datetime] = None
  deleted_at: Optional[datetime] = None

  class Config:
    from_attributes = True
