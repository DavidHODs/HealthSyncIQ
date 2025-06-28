from fastapi import APIRouter, Depends

from v1.controllers import HealthHistorySummarizationController
from v1.docs import get_responses
from v1.middlewares import Authenticate
from v1.schemas import HealthHistorySummarySchema
from v1.type_defs import (
  BaseResponse,
  StaffRole
)


class HealthHistorySummarizationRoute:
  def __init__(self) -> None:
    self.router = APIRouter()
    self.controller = HealthHistorySummarizationController()
    self._register_routes()

  def _register_routes(self) -> None:
    self.router.add_api_route(
        path="/health-history-summarization/{patient_id}",
        endpoint=self.controller.build_summary,
        methods=["GET"],
        description="Build Health History Summary For a Patient",
        dependencies=[Depends(Authenticate([StaffRole.DOCTOR]))],
        responses=get_responses(200, 401, 404, 500),
        response_model=BaseResponse[HealthHistorySummarySchema]
    )
