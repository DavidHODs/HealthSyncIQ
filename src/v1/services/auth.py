
import random
import re
import string

import bcrypt
from sqlalchemy.orm import Session

from v1.errors import AppException
from v1.models import StaffModel
from v1.schemas import (
  AccessRequestCodeSchema,
  ChangePasswordRequestSchema,
  ForgotPasswordRequestSchema,
  JWTAccessTokenPayloadResponseSchema,
  LoginRequestSchema,
  LoginResponseSchema,
  LoginStaffResponseSchema,
)
from v1.services.general.email import EmailService
from v1.type_defs import APIResponse, ErrorTypeEnum, JWTAccessTokenPayload

from .general.jwt import jwt_service_instance
from .general.redis import redis_service_instance


class AuthService:
  def __init__(self) -> None:
    self.jwt_service = jwt_service_instance()
    self.redis_service = redis_service_instance()

  def get_access_token(self, access_code_data: AccessRequestCodeSchema,
                       db: Session) -> APIResponse[JWTAccessTokenPayloadResponseSchema]:
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

      if not self._verify_password_(access_code_data.password, staff.password):
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
      html_template = email_service.load_html_template(
          "src/v1/templates/login_access_code.html")
      html = html_template.format(
          name=f"{staff.title} {staff.surname}",
          code=payload["code"])

      isEmailSent = email_service.send_html_email(
          staff.email, "Login Access Code", html)
      if not isEmailSent:
        raise AppException(
            type=ErrorTypeEnum.INTERNAL_SERVER_ERROR,
            detail="Network error during login. Please check your network connection."
        )

      return {
          "data": access_response
      }

    except Exception as exc:
      raise AppException.classify_error(exc)

  def login(self, login_data: LoginRequestSchema,
            db: Session) -> APIResponse[LoginResponseSchema]:
    try:
      jwt_service = jwt_service_instance()
      payload: JWTAccessTokenPayload = jwt_service.decode_access_token(
          login_data.token)

      if (payload["code"] != login_data.code):
        raise AppException(
            type=ErrorTypeEnum.UNAUTHORIZED,
            detail="Invalid/expired authentication code. Please try logging in again."
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

  def change_password(self, change_password_data: ChangePasswordRequestSchema,
                      db: Session) -> APIResponse[str]:
    try:
      staff = db.query(StaffModel).filter(
          StaffModel.email == change_password_data.email,
          StaffModel.deleted_at.is_(None),
          StaffModel.is_active == True
      ).first()

      if not staff:
        raise AppException(
            type=ErrorTypeEnum.UNAUTHORIZED,
            detail="Invalid email or password"
        )

      if not self._verify_password_(
              change_password_data.old_password, staff.password):
        raise AppException(
            type=ErrorTypeEnum.UNAUTHORIZED,
            detail="Invalid email or password"
        )

      if change_password_data.new_password != change_password_data.confirm_password:
        raise AppException(
            type=ErrorTypeEnum.VALIDATION_ERROR,
            detail="New password and confirmation do not match"
        )

      password = change_password_data.new_password
      if (
          len(password) < 8 or
          not re.search(r"[A-Z]", password) or
          not re.search(r"[a-z]", password) or
          not re.search(r"\d", password) or
          not re.search(r"[!@#$%&*]", password)
      ):
        raise AppException(
            type=ErrorTypeEnum.VALIDATION_ERROR,
            detail="Password must be at least 8 characters and include uppercase, lowercase, digit, and symbol (!@#$%&*)"
        )

      hashed_password = bcrypt.hashpw(
          change_password_data.new_password.encode("utf-8"),
          bcrypt.gensalt()
      ).decode("utf-8")

      staff.password = hashed_password
      db.commit()

      return {
          "data": "Password changed successfully"
      }

    except Exception as exc:
      db.rollback()
      raise AppException.classify_error(exc)

  def forgot_password(self, forgot_password_data: ForgotPasswordRequestSchema,
                      db: Session) -> APIResponse[str]:
    try:
      staff = db.query(StaffModel).filter(
          StaffModel.email == forgot_password_data.email,
          StaffModel.deleted_at.is_(None),
          StaffModel.is_active == True
      ).first()

      if not staff:
        raise AppException(
            type=ErrorTypeEnum.UNAUTHORIZED,
            detail="Invalid email"
        )

      random_password = self._generate_password_()
      hashed_password = bcrypt.hashpw(
          random_password.encode("utf-8"),
          bcrypt.gensalt()).decode("utf-8")

      email_service = EmailService()
      html_template = email_service.load_html_template(
          "src/v1/templates/password_reset.html")
      html = html_template.format(
          name=f"{staff.title} {staff.surname}",
          password=random_password)
      email_service.send_html_email(staff.email, "Password Reset", html)

      staff.password = hashed_password
      db.commit()

      return {
          "data": "Check your email for new password"
      }

    except Exception as exc:
      raise AppException.classify_error(exc)

  def _verify_password_(self, plain_password: str,
                        hashed_password: str) -> bool:
    plain_password_bytes: bytes = plain_password.encode("utf-8")
    hashed_password_bytes: bytes = hashed_password.encode("utf-8")

    return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)

  def _generate_password_(self, length: int = 8) -> str:
    symbols = "!@#$%&*"

    required = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice(symbols)
    ]

    safe_chars = (
        string.ascii_uppercase +
        string.ascii_lowercase +
        string.digits +
        symbols
    )

    remaining = random.choices(safe_chars, k=length - len(required))
    all_chars = required + remaining
    random.shuffle(all_chars)
    return ''.join(all_chars)
