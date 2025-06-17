from uuid import UUID

from fastapi import Depends, Response
from sqlalchemy.orm import Session

from database import get_db
from v1.errors import AppException, ExceptionHandler
from v1.middlewares import Authenticate
from v1.schemas import (
  LaboratoryOrderCreateRequestSchema,
  LaboratoryOrderResponseSchema,
  LaboratoryOrderUpdateRequestSchema,
)
from v1.services import LaboratoryOrderService
from v1.type_defs import (
  APIResponse,
  CreateDataResponse,
  JWTTokenPayload,
  StaffRole,
  UpdateDataResponse,
)


class LaboratoryOrderController:
  def __init__(self) -> None:
    self.laboratory_order_service: LaboratoryOrderService = LaboratoryOrderService()

  def create(
      self,
      data: LaboratoryOrderCreateRequestSchema,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(
          Authenticate([StaffRole.TECHNOLOGIST]))
  ) -> APIResponse[CreateDataResponse] | Response:
    try:
      return self.laboratory_order_service.create(data, auth_payload, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  def update(
      self,
      id: UUID,
      order_id: UUID,
      data: LaboratoryOrderUpdateRequestSchema,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(
          Authenticate([StaffRole.TECHNOLOGIST]))
  ) -> APIResponse[UpdateDataResponse] | Response:
    try:
      return self.laboratory_order_service.update(
          id, order_id, data, auth_payload, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  def getOne(
      self,
      id: UUID,
      order_id: UUID,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(
          Authenticate([StaffRole.TECHNOLOGIST]))
  ) -> APIResponse[LaboratoryOrderResponseSchema] | Response:
    try:
      return self.laboratory_order_service.getOne(id, order_id, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  def delete(
      self,
      id: UUID,
      order_id: UUID,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(
          Authenticate([StaffRole.TECHNOLOGIST]))
  ) -> APIResponse[str] | Response:
    try:
      return self.laboratory_order_service.delete(id, order_id, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  def restore(
      self,
      id: UUID,
      order_id: UUID,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(
          Authenticate([StaffRole.TECHNOLOGIST]))
  ) -> APIResponse[str] | Response:
    try:
      return self.laboratory_order_service.restore(id, order_id, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)
