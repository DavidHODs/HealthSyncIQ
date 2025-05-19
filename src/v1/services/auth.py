
import bcrypt
from sqlalchemy.orm import Session

from v1.errors import AppException
from v1.models import StaffModel
from v1.schemas import (
  LoginRequestSchema,
  LoginResponseSchema,
  LoginStaffResponseSchema,
)
from v1.type_defs import APIResponse, ErrorTypeEnum

from .general.jwt import jwt_service_instance
from .general.redis import redis_service_instance


class AuthService:
  def __init__(self) -> None:
    self.jwt_service = jwt_service_instance()
    self.redis_service = redis_service_instance()

  def login(self, login_data: LoginRequestSchema,
            db: Session) -> APIResponse[LoginResponseSchema]:
    try:
      staff = db.query(StaffModel).filter(
          StaffModel.email == login_data.email,
          StaffModel.deleted_at.is_(None),
          StaffModel.is_active == True
      ).first()

      if not staff:
        raise AppException(
            type=ErrorTypeEnum.UNAUTHORIZED,
            detail="Invalid email or password"
        )

      if not self._verify_password(login_data.password, staff.password):
        raise AppException(
            type=ErrorTypeEnum.UNAUTHORIZED,
            detail="Invalid email or password"
        )

      token = self.jwt_service.create_token(
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
