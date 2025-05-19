
from fastapi import APIRouter, Depends
from typing_extensions import List

from v1.controllers.department import DepartmentController
from v1.docs import get_responses
from v1.middlewares import Authenticate
from v1.schemas import DepartmentResponseSchema
from v1.type_defs import (
  BaseResponse,
  CreateDataResponse,
  StaffRole,
  UpdateDataResponse,
)


class DepartmentRoute:
  def __init__(self) -> None:
    self.router = APIRouter()
    self.controller = DepartmentController()
    self._register_routes()

  def _register_routes(self) -> None:
    self.router.add_api_route(
        path="/departments",
        endpoint=self.controller.create,
        methods=["POST"],
        description="Create a new Department",
        dependencies=[Depends(Authenticate([StaffRole.ADMIN]))],
        responses=get_responses(201, 400, 401, 500),
        response_model=BaseResponse[CreateDataResponse]
    )

    self.router.add_api_route(
        path="/departments/{id}",
        endpoint=self.controller.update,
        methods=["PUT"],
        description="Update an existing Department",
        dependencies=[Depends(Authenticate([StaffRole.ADMIN]))],
        responses=get_responses(200, 400, 401, 404, 500),
        response_model=BaseResponse[UpdateDataResponse]
    )

    self.router.add_api_route(
        path="/departments",
        endpoint=self.controller.getAll,
        methods=["GET"],
        description="Get all Departments",
        dependencies=[Depends(Authenticate([StaffRole.ADMIN]))],
        responses=get_responses(200, 401, 500),
        response_model=BaseResponse[List[DepartmentResponseSchema]]
    )

    self.router.add_api_route(
        path="/departments/{id}",
        endpoint=self.controller.getOne,
        methods=["GET"],
        description="Get a single Department by ID",
        dependencies=[Depends(Authenticate([StaffRole.ADMIN]))],
        responses=get_responses(200, 401, 404, 500),
        response_model=BaseResponse[DepartmentResponseSchema]
    )

    self.router.add_api_route(
        path="/departments/{id}",
        endpoint=self.controller.delete,
        methods=["DELETE"],
        description="Soft delete a Department by ID",
        dependencies=[Depends(Authenticate([StaffRole.ADMIN]))],
        responses=get_responses(200, 401, 404, 500),
        response_model=BaseResponse[str]
    )

    self.router.add_api_route(
        path="/departments/{id}/restore",
        endpoint=self.controller.restore,
        methods=["PUT"],
        description="Restore a soft-deleted Department by ID",
        dependencies=[Depends(Authenticate([StaffRole.ADMIN]))],
        responses=get_responses(200, 401, 404, 500),
        response_model=BaseResponse[str]
    )
