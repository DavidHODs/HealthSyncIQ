import uuid

from pydantic import BaseModel, EmailStr


class StaffSchema(BaseModel):
  id: uuid.UUID
  email: EmailStr
  title: str
  surname: str
  role: str

  class Config:
    from_attributes = True
