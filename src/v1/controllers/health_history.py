from uuid import UUID

from fastapi import Depends, Response
from sqlalchemy.orm import Session
from typing_extensions import List

from database import get_db
from v1.errors import AppException, ExceptionHandler
from v1.middlewares import Authenticate
from v1.schemas import HealthHistorySummarySchema
from v1.services import HealthHistorySummarizationService
from v1.type_defs import (
  APIResponse,
  JWTTokenPayload,
  StaffRole
)


class HealthHistorySummarizationController:
  def __init__(self) -> None:
    self.health_history_summarization_service: HealthHistorySummarizationService = HealthHistorySummarizationService()

  def build_summary(
      self,
      patient_id: UUID,
      db: Session = Depends(get_db),
      auth_payload: JWTTokenPayload = Depends(Authenticate([StaffRole.DOCTOR]))
  ) -> APIResponse[HealthHistorySummarySchema] | Response:
    try:
      return self.health_history_summarization_service.build_summary(patient_id, db)
    except AppException as exc:
      return ExceptionHandler.handle_error(exc)