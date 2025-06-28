from uuid import UUID

from fastapi import Depends, Response
from sqlalchemy.orm import Session
from typing_extensions import List

from database import get_db
from v1.errors import AppException, ExceptionHandler
from v1.middlewares import Authenticate
from v1.schemas import (
  PatientCreateRequestSchema,
  PatientResponseSchema,
  PatientUpdateRequestSchema,
)
from v1.services import PatientService
from v1.type_defs import (
  APIResponse,
  CreateDataResponse,
  JWTTokenPayload,
  StaffRole,
  UpdateDataResponse,
)


class PatientController:
  def __init__(self) -> None:
    self.patient_service: PatientService = PatientService()

  def create(
      self,
      data: PatientCreateRequestSchema,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(Authenticate([StaffRole.ADMIN, StaffRole.DOCTOR]))
  ) -> APIResponse[CreateDataResponse] | Response:
    try:
      return self.patient_service.create(data, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  def update(
      self,
      id: UUID,
      data: PatientUpdateRequestSchema,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(Authenticate([StaffRole.ADMIN, StaffRole.DOCTOR]))
  ) -> APIResponse[UpdateDataResponse] | Response:
    try:
      return self.patient_service.update(id, data, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  def getAll(
      self,
      limit: int = 15,
      page: int = 1,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(Authenticate([StaffRole.ADMIN, StaffRole.DOCTOR]))
  ) -> APIResponse[List[PatientResponseSchema]] | Response:
    try:
      offset: int = (page - 1) * limit

      return self.patient_service.getAll(limit, offset, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  def getOne(
      self,
      id: UUID,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(Authenticate([StaffRole.ADMIN, StaffRole.DOCTOR]))
  ) -> APIResponse[PatientResponseSchema] | Response:
    try:
      return self.patient_service.getOne(id, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  def delete(
      self,
      id: UUID,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(Authenticate([StaffRole.ADMIN, StaffRole.DOCTOR]))
  ) -> APIResponse[str] | Response:
    try:
      return self.patient_service.delete(id, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  def restore(
      self,
      id: UUID,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(Authenticate([StaffRole.ADMIN, StaffRole.DOCTOR]))
  ) -> APIResponse[str] | Response:
    try:
      return self.patient_service.restore(id, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)
