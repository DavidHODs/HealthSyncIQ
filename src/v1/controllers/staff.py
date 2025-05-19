from uuid import UUID

from fastapi import Depends, Response
from sqlalchemy.orm import Session
from typing_extensions import List

from database import get_db
from v1.errors import AppException, ExceptionHandler
from v1.middlewares import Authenticate
from v1.schemas import (
  StaffCreateRequestSchema,
  StaffResponseSchema,
  StaffUpdateRequestSchema,
)
from v1.services import StaffService
from v1.type_defs import (
  APIResponse,
  CreateDataResponse,
  JWTTokenPayload,
  StaffRole,
  UpdateDataResponse,
)


class StaffController:
  def __init__(self) -> None:
    self.staff_service: StaffService = StaffService()

  def create(
      self,
      data: StaffCreateRequestSchema,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(Authenticate([StaffRole.ADMIN]))
  ) -> APIResponse[CreateDataResponse] | Response:
    try:
      return self.staff_service.create(data, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  def update(
      self,
      id: UUID,
      data: StaffUpdateRequestSchema,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(Authenticate([StaffRole.ADMIN]))
  ) -> APIResponse[UpdateDataResponse] | Response:
    try:
      return self.staff_service.update(id, data, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  def getAll(
      self,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(Authenticate([StaffRole.ADMIN]))
  ) -> APIResponse[List[StaffResponseSchema]] | Response:
    try:
      return self.staff_service.getAll(db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  def getOne(
      self,
      id: UUID,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(Authenticate([StaffRole.ADMIN]))
  ) -> APIResponse[StaffResponseSchema] | Response:
    try:
      return self.staff_service.getOne(id, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  def delete(
      self,
      id: UUID,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(Authenticate([StaffRole.ADMIN]))
  ) -> APIResponse[str] | Response:
    try:
      return self.staff_service.delete(id, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  def restore(
      self,
      id: UUID,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(Authenticate([StaffRole.ADMIN]))
  ) -> APIResponse[str] | Response:
    try:
      return self.staff_service.restore(id, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)
