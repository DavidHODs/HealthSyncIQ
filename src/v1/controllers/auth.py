from fastapi import Depends, Response
from sqlalchemy.orm import Session

from database import get_db
from v1.errors import AppException, ExceptionHandler
from v1.schemas import LoginRequestSchema, LoginResponseSchema
from v1.services import AuthService
from v1.type_defs import APIResponse


class AuthController:
  def __init__(self) -> None:
    self.auth_service: AuthService = AuthService()

  def login(self, login_data: LoginRequestSchema, db: Session = Depends(
          get_db)) -> APIResponse[LoginResponseSchema] | Response:
    try:
      return self.auth_service.login(login_data, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)
