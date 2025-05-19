import uuid

from pydantic import BaseModel, EmailStr


class LoginRequestSchema(BaseModel):
  email: EmailStr
  password: str

  class Config:
    extra = "forbid"
    json_schema_extra = {
        "email": "user@example.com",
        "password": "SecurePassword123!"
    }


class LoginStaffResponseSchema(BaseModel):
  id: uuid.UUID
  email: EmailStr
  title: str
  surname: str
  role: str

  class Config:
    json_schema_extra = {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "email": "user@example.com",
        "title": "Dr.",
        "surname": "Smith",
        "role": "Doctor"
    }


class LoginResponseSchema(BaseModel):
  auth_token: str
  staff: LoginStaffResponseSchema

  class Config:
    json_schema_extra = {
        "auth_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "staff": {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "email": "user@example.com",
            "title": "Dr.",
            "surname": "Smith",
            "first_name": "John",
            "last_name": "Dome",
            "role": "Doctor"
        }
    }

    from_attributes = True
