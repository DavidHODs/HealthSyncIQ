from uuid import UUID

from fastapi import Depends, Response
from sqlalchemy.orm import Session

from database import get_db
from v1.errors import AppException, ExceptionHandler
from v1.middlewares import Authenticate
from v1.schemas import (
  DiagnosisCreateRequestSchema,
  DiagnosisResponseSchema,
  DiagnosisUpdateRequestSchema,
)
from v1.services import DiagnosisService
from v1.type_defs import (
  APIResponse,
  CreateDataResponse,
  JWTTokenPayload,
  StaffRole,
  UpdateDataResponse,
)


class DiagnosisController:
  def __init__(self) -> None:
    self.diagnosis_service: DiagnosisService = DiagnosisService()

  def create(
      self,
      data: DiagnosisCreateRequestSchema,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(Authenticate([StaffRole.DOCTOR]))
  ) -> APIResponse[CreateDataResponse] | Response:
    try:
      return self.diagnosis_service.create(data, auth_payload, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  def update(
      self,
      id: UUID,
      data: DiagnosisUpdateRequestSchema,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(Authenticate([StaffRole.DOCTOR]))
  ) -> APIResponse[UpdateDataResponse] | Response:
    try:
      return self.diagnosis_service.update(
          id, data, auth_payload, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  def getOne(
      self,
      id: UUID,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(Authenticate([StaffRole.DOCTOR]))
  ) -> APIResponse[DiagnosisResponseSchema] | Response:
    try:
      return self.diagnosis_service.getOne(id, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  def delete(
      self,
      id: UUID,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(Authenticate([StaffRole.DOCTOR]))
  ) -> APIResponse[str] | Response:
    try:
      return self.diagnosis_service.delete(id, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  def restore(
      self,
      id: UUID,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(Authenticate([StaffRole.DOCTOR]))
  ) -> APIResponse[str] | Response:
    try:
      return self.diagnosis_service.restore(id, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)
