from uuid import UUID

from fastapi import Depends, Response
from sqlalchemy.orm import Session
from typing_extensions import List

from database import get_db
from v1.errors import AppException, ExceptionHandler
from v1.middlewares import Authenticate
from v1.schemas import (
  ClinicalOrderCreateRequestSchema,
  ClinicalOrderUpdateRequestSchema,
  ClinicalOrderResponseSchema,
)
from v1.services import ClinicalOrderService
from v1.type_defs import (
  APIResponse,
  CreateDataResponse,
  JWTTokenPayload,
  StaffRole,
  UpdateDataResponse,
)


class ClinicalOrderController:
  def __init__(self) -> None:
    self.clinical_order_service: ClinicalOrderService = ClinicalOrderService()

  def create(
      self,
      data: ClinicalOrderCreateRequestSchema,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(Authenticate([StaffRole.DOCTOR]))
  ) -> APIResponse[CreateDataResponse] | Response:
    try:
      return self.clinical_order_service.create(data, auth_payload, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  def update(
      self,
      id: UUID,
      encounter_id: UUID,
      data: ClinicalOrderUpdateRequestSchema,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(Authenticate([StaffRole.DOCTOR]))
  ) -> APIResponse[UpdateDataResponse] | Response:
    try:
      return self.clinical_order_service.update(
          id, encounter_id, data, auth_payload, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  def getAll(
      self,
      encounter_id: UUID,
      limit: int = 15,
      page: int = 1,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(Authenticate([StaffRole.DOCTOR]))
  ) -> APIResponse[List[ClinicalOrderResponseSchema]] | Response:
    try:
      offset: int = (page - 1) * limit

      return self.clinical_order_service.getAll(
          encounter_id, limit, offset, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  def getOne(
      self,
      id: UUID,
      encounter_id: UUID,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(Authenticate([StaffRole.DOCTOR]))
  ) -> APIResponse[ClinicalOrderResponseSchema] | Response:
    try:
      return self.clinical_order_service.getOne(id, encounter_id, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  def delete(
      self,
      id: UUID,
      encounter_id: UUID,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(Authenticate([StaffRole.DOCTOR]))
  ) -> APIResponse[str] | Response:
    try:
      return self.clinical_order_service.delete(id, encounter_id, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  def restore(
      self,
      id: UUID,
      encounter_id: UUID,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(Authenticate([StaffRole.DOCTOR]))
  ) -> APIResponse[str] | Response:
    try:
      return self.clinical_order_service.restore(id, encounter_id, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)