from fastapi import APIRouter, Depends

from v1.controllers import AuthController
from v1.docs import get_responses
from v1.middlewares import Authenticate
from v1.schemas import (
  LoginResponseSchema, 
  JWTAccessTokenPayloadResponseSchema,
)
from v1.type_defs import BaseResponse, StaffRole


class AuthRoute:
  def __init__(self) -> None:
    self.router = APIRouter()
    self.controller = AuthController()
    self._register_routes()
  
  def _register_routes(self) -> None:
    self.router.add_api_route(
        path="/auth/get-access-token",
        endpoint=self.controller.get_access_token,
        methods=["POST"],
        description="Auth Access Token Endpoint",
        responses=get_responses(200, 401, 500),
        response_model=BaseResponse[JWTAccessTokenPayloadResponseSchema]
    )

    self.router.add_api_route(
        path="/auth/login",
        endpoint=self.controller.login,
        methods=["POST"],
        description="Auth Login Endpoint",
        responses=get_responses(200, 401, 500),
        response_model=BaseResponse[LoginResponseSchema]
    )
    
    self.router.add_api_route(
        path="/auth/change-password",
        endpoint=self.controller.change_password,
        methods=["POST"],
        description="Auth Change Password Endpoint",
        responses=get_responses(200, 401, 500),
        response_model=BaseResponse[str]
    )
    
    self.router.add_api_route(
        path="/auth/forgot-password",
        endpoint=self.controller.forgot_password,
        methods=["POST"],
        description="Auth Forgot Password Endpoint",
        dependencies=[Depends(Authenticate([StaffRole.ADMIN]))],
        responses=get_responses(200, 401, 500),
        response_model=BaseResponse[str]
    )
