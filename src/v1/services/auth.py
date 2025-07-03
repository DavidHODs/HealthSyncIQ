
import bcrypt
from sqlalchemy.orm import Session
import uuid

from v1.errors import AppException
from v1.models import StaffModel
from v1.schemas import (
  LoginRequestSchema,
  LoginResponseSchema,
  LoginStaffResponseSchema,
  JWTAccessTokenPayloadResponseSchema,
  AccessRequestCodeSchema
)
from v1.services.general.email import EmailService
from v1.type_defs import APIResponse, ErrorTypeEnum, JWTAccessTokenPayload

from .general.jwt import jwt_service_instance
from .general.redis import redis_service_instance


class AuthService:
  def __init__(self) -> None:
    self.jwt_service = jwt_service_instance()
    self.redis_service = redis_service_instance()
    
  def get_access_token(self, access_code_data: AccessRequestCodeSchema, db: Session) -> APIResponse[JWTAccessTokenPayloadResponseSchema]:
    try:
      staff = db.query(StaffModel).filter(
          StaffModel.email == access_code_data.email,
          StaffModel.deleted_at.is_(None),
          StaffModel.is_active == True
      ).first()

      if not staff:
        raise AppException(
            type=ErrorTypeEnum.UNAUTHORIZED,
            detail="Invalid email or password"
        )

      if not self._verify_password(access_code_data.password, staff.password):
        raise AppException(
            type=ErrorTypeEnum.UNAUTHORIZED,
            detail="Invalid email or password"
        )

      payload = self.jwt_service.create_access_token(staff.id)

      access_response = JWTAccessTokenPayloadResponseSchema(
        id=staff.id,
        token=payload["token"],
        msg="Check your email for access code"
      )
      
      email_service = EmailService()
      html_template = email_service.load_html_template("src/v1/templates/login_access_code.html")
      html = html_template.format(name=f"{staff.title} {staff.surname}", code=payload["code"])
      email_service.send_html_email(staff.email, "Login Access Code", html);

      return {
          "data": access_response
      }

    except Exception as exc:
      raise AppException.classify_error(exc)

  def login(self, login_data: LoginRequestSchema, db: Session) -> APIResponse[LoginResponseSchema]:
    try:
      jwt_service = jwt_service_instance();
      payload: JWTAccessTokenPayload = jwt_service.decode_access_token(login_data.token)
      
      if (payload["code"] != login_data.code):
        raise AppException(
            type=ErrorTypeEnum.UNAUTHORIZED,
            detail="Invalid/expired authentication code"
        )
      
      staff = db.query(StaffModel).filter(
          StaffModel.id == payload["id"],
          StaffModel.deleted_at.is_(None),
          StaffModel.is_active == True
      ).first()

      if not staff:
        raise AppException(
            type=ErrorTypeEnum.UNAUTHORIZED,
            detail="Invalid email or password"
        )

      token = self.jwt_service.create_auth_token(
          id=staff.id,
          role=staff.role
      )

      redis_auth_key = f"auth:{staff.id}"
      self.redis_service.set(redis_auth_key, token)

      login_response = LoginResponseSchema(
          auth_token=token,
          staff=LoginStaffResponseSchema(
              id=staff.id,
              email=staff.email,
              title=staff.title,
              surname=staff.surname,
              role=staff.role
          )
      )

      return {
          "data": login_response
      }

    except Exception as exc:
      raise AppException.classify_error(exc)

  def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
    plain_password_bytes: bytes = plain_password.encode("utf-8")
    hashed_password_bytes: bytes = hashed_password.encode("utf-8")

    return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)
