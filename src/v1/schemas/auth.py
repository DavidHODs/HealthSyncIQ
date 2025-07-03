import uuid

from pydantic import BaseModel, EmailStr


class AccessRequestCodeSchema(BaseModel):
  email: EmailStr
  password: str

  class Config:
    extra = "forbid"
    json_json_schema_extra = {
        "email": "user@example.com",
        "password": "SecurePassword123!"
    }


class LoginRequestSchema(BaseModel):
  token: str
  code: str

  class Config:
    extra = "forbid"
    json_json_schema_extra = {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "code": "FG@R1STY"
    }



class JWTAccessTokenPayloadResponseSchema(BaseModel):
  id: uuid.UUID
  token: str
  msg: str
  
  class Config:
    from_attributes = True
    json_schema_extra = {
      "example": {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "msg": "Check your email for your access code"
      }
    }

class LoginStaffResponseSchema(BaseModel):
  id: uuid.UUID
  email: EmailStr
  title: str
  surname: str
  role: str

  class Config:
    json_schema_extra = {
      "example": {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "email": "user@example.com",
        "title": "Dr.",
        "surname": "Smith",
        "role": "Doctor"
      }
    }


class LoginResponseSchema(BaseModel):
  auth_token: str
  staff: LoginStaffResponseSchema

  class Config:
    json_schema_extra = {
      "example": {
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
    }

    from_attributes = True

class ChangePasswordRequestSchema(BaseModel):
  email: EmailStr
  old_password: str
  new_password: str
  confirm_password: str

  class Config:
    json_schema_extra = {
      "example": {
        "email": "user@example.com",
        "old_password": "OldPassword123!",
        "new_password": "NewSecurePassword456!",
        "confirm_password": "NewSecurePassword456!"
      }
    }
    
class ForgotPasswordRequestSchema(BaseModel):
  email: EmailStr

  class Config:
    json_schema_extra = {
      "example": {
        "email": "user@example.com",
      }
    }