
from fastapi import APIRouter, Depends
from typing_extensions import List

from v1.controllers import StaffController
from v1.docs import get_responses
from v1.middlewares import Authenticate
from v1.schemas import StaffResponseSchema
from v1.type_defs import (
  BaseResponse,
  CreateDataResponse,
  StaffRole,
  UpdateDataResponse,
)


class StaffRoute:
  def __init__(self) -> None:
    self.router = APIRouter()
    self.controller = StaffController()
    self._register_routes()

  def _register_routes(self) -> None:
    self.router.add_api_route(
        path="/staffs",
        endpoint=self.controller.create,
        methods=["POST"],
        description="Create a new Staff",
        dependencies=[Depends(Authenticate([StaffRole.ADMIN]))],
        responses=get_responses(201, 400, 401, 500),
        response_model=BaseResponse[CreateDataResponse]
    )

    self.router.add_api_route(
        path="/staffs/{id}",
        endpoint=self.controller.update,
        methods=["PUT"],
        description="Update an existing Staff",
        dependencies=[Depends(Authenticate([StaffRole.ADMIN]))],
        responses=get_responses(200, 400, 401, 404, 500),
        response_model=BaseResponse[UpdateDataResponse]
    )

    self.router.add_api_route(
        path="/staffs",
        endpoint=self.controller.getAll,
        methods=["GET"],
        description="Get all Staffs",
        dependencies=[Depends(Authenticate([StaffRole.ADMIN]))],
        responses=get_responses(200, 401, 500),
        response_model=BaseResponse[List[StaffResponseSchema]]
    )

    self.router.add_api_route(
        path="/staffs/{id}",
        endpoint=self.controller.getOne,
        methods=["GET"],
        description="Get a single Staff by ID",
        dependencies=[Depends(Authenticate([StaffRole.ADMIN]))],
        responses=get_responses(200, 401, 404, 500),
        response_model=BaseResponse[StaffResponseSchema]
    )

    self.router.add_api_route(
        path="/staffs/{id}",
        endpoint=self.controller.delete,
        methods=["DELETE"],
        description="Soft delete a Staff by ID",
        dependencies=[Depends(Authenticate([StaffRole.ADMIN]))],
        responses=get_responses(200, 401, 404, 500),
        response_model=BaseResponse[str]
    )

    self.router.add_api_route(
        path="/staffs/{id}/restore",
        endpoint=self.controller.restore,
        methods=["PUT"],
        description="Restore a soft-deleted Staff by ID",
        dependencies=[Depends(Authenticate([StaffRole.ADMIN]))],
        responses=get_responses(200, 401, 404, 500),
        response_model=BaseResponse[str]
    )
