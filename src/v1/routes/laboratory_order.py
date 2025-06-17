from fastapi import APIRouter, Depends

from v1.controllers import LaboratoryOrderController
from v1.docs import get_responses
from v1.middlewares import Authenticate
from v1.schemas import LaboratoryOrderResponseSchema
from v1.type_defs import (
  BaseResponse,
  CreateDataResponse,
  StaffRole,
  UpdateDataResponse,
)


class LaboratoryOrderRoute:
  def __init__(self) -> None:
    self.router = APIRouter()
    self.controller = LaboratoryOrderController()
    self._register_routes()

  def _register_routes(self) -> None:
    self.router.add_api_route(
        path="/laboratory-orders",
        endpoint=self.controller.create,
        methods=["POST"],
        description="Create a new Laboratory Order Result",
        dependencies=[Depends(Authenticate([StaffRole.TECHNOLOGIST]))],
        status_code=201,
        responses=get_responses(201, 400, 401, 500),
        response_model=BaseResponse[CreateDataResponse]
    )

    self.router.add_api_route(
        path="/laboratory-orders/{id}/{order_id}",
        endpoint=self.controller.update,
        methods=["PUT"],
        description="Update an existing Laboratory Order Result",
        dependencies=[Depends(Authenticate([StaffRole.TECHNOLOGIST]))],
        responses=get_responses(200, 400, 401, 404, 500),
        response_model=BaseResponse[UpdateDataResponse]
    )

    self.router.add_api_route(
        path="/laboratory-orders/{id}/{order_id}",
        endpoint=self.controller.getOne,
        methods=["GET"],
        description="Get a Single Laboratory Order Result For a Clinical Order",
        dependencies=[Depends(Authenticate([StaffRole.TECHNOLOGIST]))],
        responses=get_responses(200, 401, 404, 500),
        response_model=BaseResponse[LaboratoryOrderResponseSchema]
    )

    self.router.add_api_route(
        path="/laboratory-orders/{id}/{order_id}",
        endpoint=self.controller.delete,
        methods=["DELETE"],
        description="Soft delete a Laboratory Order Result",
        dependencies=[Depends(Authenticate([StaffRole.TECHNOLOGIST]))],
        responses=get_responses(200, 401, 404, 500),
        response_model=BaseResponse[str]
    )

    self.router.add_api_route(
        path="/laboratory-orders/{id}/{order_id}/restore",
        endpoint=self.controller.restore,
        methods=["PATCH"],
        description="Restore a soft-deleted Laboratory Order Result",
        dependencies=[Depends(Authenticate([StaffRole.TECHNOLOGIST]))],
        responses=get_responses(200, 401, 404, 500),
        response_model=BaseResponse[str]
    )
