from fastapi import APIRouter

from v1.controllers import AuthController
from v1.docs import get_responses
from v1.schemas import LoginResponseSchema
from v1.type_defs import BaseResponse


class AuthRoute:
  def __init__(self) -> None:
    self.router = APIRouter()
    self.controller = AuthController()
    self._register_routes()

  def _register_routes(self) -> None:
    self.router.add_api_route(
        path="/auth/login",
        endpoint=self.controller.login,
        methods=["POST"],
        description="Auth Login Endpoint",
        responses=get_responses(200, 401, 500),
        response_model=BaseResponse[LoginResponseSchema]
    )
