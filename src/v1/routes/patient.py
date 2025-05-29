
from fastapi import APIRouter, Depends
from typing_extensions import List

from v1.controllers import PatientController
from v1.docs import get_responses
from v1.middlewares import Authenticate
from v1.schemas import PatientResponseSchema
from v1.type_defs import (
  APIResponse,
  BaseResponse,
  CreateDataResponse,
  StaffRole,
  UpdateDataResponse,
)


class PatientRoute:
  def __init__(self) -> None:
    self.router = APIRouter()
    self.controller = PatientController()
    self._register_routes()

  def _register_routes(self) -> None:
    self.router.add_api_route(
        path="/patients",
        endpoint=self.controller.create,
        methods=["POST"],
        description="Create a new Patient",
        dependencies=[Depends(Authenticate([StaffRole.ADMIN]))],
        status_code=201,
        responses=get_responses(201, 400, 401, 500),
        response_model=BaseResponse[CreateDataResponse]
    )

    self.router.add_api_route(
        path="/patients/{id}",
        endpoint=self.controller.update,
        methods=["PUT"],
        description="Update an existing Patient",
        dependencies=[Depends(Authenticate([StaffRole.ADMIN]))],
        responses=get_responses(200, 400, 401, 404, 500),
        response_model=BaseResponse[UpdateDataResponse]
    )

    self.router.add_api_route(
        path="/patients",
        endpoint=self.controller.getAll,
        methods=["GET"],
        description="Get all Patients",
        dependencies=[Depends(Authenticate([StaffRole.ADMIN]))],
        responses=get_responses(200, 401, 500),
        response_model=APIResponse[List[PatientResponseSchema]]
    )

    self.router.add_api_route(
        path="/patients/{id}",
        endpoint=self.controller.getOne,
        methods=["GET"],
        description="Get a single Patient by ID",
        dependencies=[Depends(Authenticate([StaffRole.ADMIN]))],
        responses=get_responses(200, 401, 404, 500),
        response_model=BaseResponse[PatientResponseSchema]
    )

    self.router.add_api_route(
        path="/patients/{id}",
        endpoint=self.controller.delete,
        methods=["DELETE"],
        description="Soft delete a Patient by ID",
        dependencies=[Depends(Authenticate([StaffRole.ADMIN]))],
        responses=get_responses(200, 401, 404, 500),
        response_model=BaseResponse[str]
    )

    self.router.add_api_route(
        path="/patients/{id}/restore",
        endpoint=self.controller.restore,
        methods=["PATCH"],
        description="Restore a soft-deleted Patient by ID",
        dependencies=[Depends(Authenticate([StaffRole.ADMIN]))],
        responses=get_responses(200, 401, 404, 500),
        response_model=BaseResponse[str]
    )
