import uuid
from datetime import date

from pydantic import BaseModel
from typing_extensions import Optional


class PatientSchema(BaseModel):
  id: Optional[uuid.UUID] = None
  registration_number: str
  surname: str
  first_name: str
  last_name: Optional[str] = None
  dob: Optional[date] = None
  genotype: Optional[str] = None
  blood_group: Optional[str] = None
  gender: Optional[str] = None
  contact_information: Optional[str] = None
  emergency_contact: Optional[str] = None

  class Config:
    from_attributes = True
