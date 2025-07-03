from fastapi import Depends, Response
from sqlalchemy.orm import Session

from database import get_db
from v1.errors import AppException, ExceptionHandler
from v1.middlewares import Authenticate
from v1.schemas import (
  LoginRequestSchema, 
  LoginResponseSchema, 
  AccessRequestCodeSchema, 
  JWTAccessTokenPayloadResponseSchema, 
  ChangePasswordRequestSchema,
  ForgotPasswordRequestSchema
)
from v1.services import AuthService
from v1.type_defs import APIResponse, StaffRole, JWTTokenPayload


class AuthController:
  def __init__(self) -> None:
    self.auth_service: AuthService = AuthService()

  def get_access_token(self, access_code: AccessRequestCodeSchema, db: Session = Depends(
          get_db)) -> APIResponse[JWTAccessTokenPayloadResponseSchema] | Response:
    try:
      return self.auth_service.get_access_token(access_code, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)
    
  def login(self, login_data: LoginRequestSchema, db: Session = Depends(
          get_db)) -> APIResponse[LoginResponseSchema] | Response:
    try:
      return self.auth_service.login(login_data, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)
    
  def change_password(self, change_password_data: ChangePasswordRequestSchema, db: Session = Depends(
          get_db)) -> APIResponse[str] | Response:
    try:
      return self.auth_service.change_password(change_password_data, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)
    
  def forgot_password(self, 
                      forgot_password_data: ForgotPasswordRequestSchema, 
                      db: Session = Depends(get_db),
                      auth_payload: JWTTokenPayload = Depends(Authenticate([StaffRole.ADMIN]))) -> APIResponse[str] | Response:
    try:
      return self.auth_service.forgot_password(forgot_password_data, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)
