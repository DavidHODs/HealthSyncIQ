from fastapi import APIRouter, Depends
from typing_extensions import List

from v1.controllers import ClinicalOrderController
from v1.docs import get_responses
from v1.middlewares import Authenticate
from v1.schemas import ClinicalOrderResponseSchema
from v1.type_defs import (
  APIResponse,
  BaseResponse,
  CreateDataResponse,
  StaffRole,
  UpdateDataResponse,
)


class ClinicalOrderRoute:
  def __init__(self) -> None:
    self.router = APIRouter()
    self.controller = ClinicalOrderController()
    self._register_routes()

  def _register_routes(self) -> None:
    self.router.add_api_route(
        path="/clinical-orders",
        endpoint=self.controller.create,
        methods=["POST"],
        description="Create a new Clinical Order",
        dependencies=[Depends(Authenticate([StaffRole.DOCTOR]))],
        status_code=201,
        responses=get_responses(201, 400, 401, 500),
        response_model=BaseResponse[CreateDataResponse]
    )

    self.router.add_api_route(
        path="/clinical-orders/{id}/{encounter_id}",
        endpoint=self.controller.update,
        methods=["PUT"],
        description="Update an existing Clinical Order",
        dependencies=[Depends(Authenticate([StaffRole.DOCTOR]))],
        responses=get_responses(200, 400, 401, 404, 500),
        response_model=BaseResponse[UpdateDataResponse]
    )

    self.router.add_api_route(
        path="/clinical-orders/{encounter_id}",
        endpoint=self.controller.getAll,
        methods=["GET"],
        description="Get all Clinical Orders For a Clinical Encounter",
        dependencies=[Depends(Authenticate([StaffRole.DOCTOR]))],
        responses=get_responses(200, 401, 500),
        response_model=APIResponse[List[ClinicalOrderResponseSchema]]
    )

    self.router.add_api_route(
        path="/clinical-orders/{id}/{encounter_id}",
        endpoint=self.controller.getOne,
        methods=["GET"],
        description="Get a Single Clinical Order For a Clinical Encounter",
        dependencies=[Depends(Authenticate([StaffRole.DOCTOR]))],
        responses=get_responses(200, 401, 404, 500),
        response_model=BaseResponse[ClinicalOrderResponseSchema]
    )

    self.router.add_api_route(
        path="/clinical-orders/{id}/{encounter_id}",
        endpoint=self.controller.delete,
        methods=["DELETE"],
        description="Soft delete a Clinical Order",
        dependencies=[Depends(Authenticate([StaffRole.DOCTOR]))],
        responses=get_responses(200, 401, 404, 500),
        response_model=BaseResponse[str]
    )

    self.router.add_api_route(
        path="/clinical-orders/{id}/{encounter_id}/restore",
        endpoint=self.controller.restore,
        methods=["PATCH"],
        description="Restore a soft-deleted Clinical Order",
        dependencies=[Depends(Authenticate([StaffRole.DOCTOR]))],
        responses=get_responses(200, 401, 404, 500),
        response_model=BaseResponse[str]
    )
