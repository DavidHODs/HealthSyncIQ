from uuid import UUID

from fastapi import Depends, Response
from sqlalchemy.orm import Session
from typing_extensions import List

from database import get_db
from v1.errors import AppException, ExceptionHandler
from v1.middlewares import Authenticate
from v1.schemas import (
  ClinicalEncounterCreateRequestSchema,
  ClinicalEncounterResponseSchema,
  ClinicalEncounterUpdateRequestSchema,
)
from v1.services import ClinicalEncounterService
from v1.type_defs import (
  APIResponse,
  CreateDataResponse,
  JWTTokenPayload,
  StaffRole,
  UpdateDataResponse,
)


class ClinicalEncounterController:
  def __init__(self) -> None:
    self.clinical_encounter_service: ClinicalEncounterService = ClinicalEncounterService()

  def create(
      self,
      data: ClinicalEncounterCreateRequestSchema,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(Authenticate([StaffRole.DOCTOR]))
  ) -> APIResponse[CreateDataResponse] | Response:
    try:
      return self.clinical_encounter_service.create(data, auth_payload, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  def update(
      self,
      id: UUID,
      patient_id: UUID,
      data: ClinicalEncounterUpdateRequestSchema,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(Authenticate([StaffRole.DOCTOR]))
  ) -> APIResponse[UpdateDataResponse] | Response:
    try:
      return self.clinical_encounter_service.update(
          id, patient_id, data, auth_payload, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  def getAll(
      self,
      patient_id: UUID,
      limit: int = 15,
      page: int = 1,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(Authenticate([StaffRole.DOCTOR]))
  ) -> APIResponse[List[ClinicalEncounterResponseSchema]] | Response:
    try:
      offset: int = (page - 1) * limit

      return self.clinical_encounter_service.getAll(
          patient_id, limit, offset, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  def getOne(
      self,
      id: UUID,
      patient_id: UUID,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(Authenticate([StaffRole.DOCTOR]))
  ) -> APIResponse[ClinicalEncounterResponseSchema] | Response:
    try:
      return self.clinical_encounter_service.getOne(id, patient_id, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  def delete(
      self,
      id: UUID,
      patient_id: UUID,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(Authenticate([StaffRole.DOCTOR]))
  ) -> APIResponse[str] | Response:
    try:
      return self.clinical_encounter_service.delete(id, patient_id, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)

  def restore(
      self,
      id: UUID,
      patient_id: UUID,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(Authenticate([StaffRole.DOCTOR]))
  ) -> APIResponse[str] | Response:
    try:
      return self.clinical_encounter_service.restore(id, patient_id, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)
    
  def close_encounter(
      self,
      id: UUID,
      patient_id: UUID,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(Authenticate([StaffRole.DOCTOR]))
  ) -> APIResponse[str] | Response:
    try:
      return self.clinical_encounter_service.close_encounter(id, patient_id, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)
