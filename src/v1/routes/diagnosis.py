
from fastapi import APIRouter, Depends

from v1.controllers import DiagnosisController
from v1.docs import get_responses
from v1.middlewares import Authenticate
from v1.schemas import DiagnosisResponseSchema
from v1.type_defs import (
  BaseResponse,
  CreateDataResponse,
  StaffRole,
  UpdateDataResponse,
)


class DiagnosisRoute:
  def __init__(self) -> None:
    self.router = APIRouter()
    self.controller = DiagnosisController()
    self._register_routes()

  def _register_routes(self) -> None:
    self.router.add_api_route(
        path="/diagnosis",
        endpoint=self.controller.create,
        methods=["POST"],
        description="Create a new Diagnosis",
        dependencies=[Depends(Authenticate([StaffRole.DOCTOR]))],
        status_code=201,
        responses=get_responses(201, 400, 401, 500),
        response_model=BaseResponse[CreateDataResponse]
    )

    self.router.add_api_route(
        path="/diagnosis/{id}",
        endpoint=self.controller.update,
        methods=["PUT"],
        description="Update an existing Diagnosis",
        dependencies=[Depends(Authenticate([StaffRole.DOCTOR]))],
        responses=get_responses(200, 400, 401, 404, 500),
        response_model=BaseResponse[UpdateDataResponse]
    )

    self.router.add_api_route(
        path="/diagnosis/{id}",
        endpoint=self.controller.getOne,
        methods=["GET"],
        description="Get a Single Diagnosis",
        dependencies=[Depends(Authenticate([StaffRole.DOCTOR]))],
        responses=get_responses(200, 401, 404, 500),
        response_model=BaseResponse[DiagnosisResponseSchema]
    )

    self.router.add_api_route(
        path="/diagnosis/{id}",
        endpoint=self.controller.delete,
        methods=["DELETE"],
        description="Soft delete a Diagnosis",
        dependencies=[Depends(Authenticate([StaffRole.DOCTOR]))],
        responses=get_responses(200, 401, 404, 500),
        response_model=BaseResponse[str]
    )

    self.router.add_api_route(
        path="/diagnosis/{id}/restore",
        endpoint=self.controller.restore,
        methods=["PATCH"],
        description="Restore a soft-deleted Diagnosis",
        dependencies=[Depends(Authenticate([StaffRole.DOCTOR]))],
        responses=get_responses(200, 401, 404, 500),
        response_model=BaseResponse[str]
    )
