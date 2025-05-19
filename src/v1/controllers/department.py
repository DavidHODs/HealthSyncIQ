from uuid import UUID

from fastapi import Depends, Response
from sqlalchemy.orm import Session
from typing_extensions import List

from database import get_db
from v1.errors import AppException, ExceptionHandler
from v1.middlewares import Authenticate
from v1.schemas import (
  DepartmentCreateRequestSchema,
  DepartmentResponseSchema,
  DepartmentUpdateRequestSchema,
)
from v1.services.department import DepartmentService
from v1.type_defs import (
  APIResponse,
  CreateDataResponse,
  JWTTokenPayload,
  StaffRole,
  UpdateDataResponse,
)


class DepartmentController:
  def __init__(self) -> None:
    self.department_service: DepartmentService = DepartmentService()
    self.authenticate: Authenticate = Authenticate([StaffRole.ADMIN])

  def create(
      self,
      data: DepartmentCreateRequestSchema,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(Authenticate([StaffRole.ADMIN]))
  ) -> APIResponse[CreateDataResponse] | Response:
    try:
      return self.department_service.create(data, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  def update(
      self,
      id: UUID,
      data: DepartmentUpdateRequestSchema,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(Authenticate([StaffRole.ADMIN]))
  ) -> APIResponse[UpdateDataResponse] | Response:
    try:
      return self.department_service.update(id, data, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  def getAll(
      self,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(Authenticate([StaffRole.ADMIN]))
  ) -> APIResponse[List[DepartmentResponseSchema]] | Response:
    try:
      return self.department_service.getAll(db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  def getOne(
      self,
      id: UUID,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(Authenticate([StaffRole.ADMIN]))
  ) -> APIResponse[DepartmentResponseSchema] | Response:
    try:
      return self.department_service.getOne(id, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  def delete(
      self,
      id: UUID,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(Authenticate([StaffRole.ADMIN]))
  ) -> APIResponse[str] | Response:
    try:
      return self.department_service.delete(id, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  def restore(
      self,
      id: UUID,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(Authenticate([StaffRole.ADMIN]))
  ) -> APIResponse[str] | Response:
    try:
      return self.department_service.restore(id, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)
