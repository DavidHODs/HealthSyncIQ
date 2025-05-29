
from fastapi import APIRouter, Depends
from typing_extensions import List

from v1.controllers import ClinicalNoteController
from v1.docs import get_responses
from v1.middlewares import Authenticate
from v1.schemas import ClinicalNoteResponseSchema
from v1.type_defs import (
  APIResponse,
  BaseResponse,
  CreateDataResponse,
  StaffRole,
  UpdateDataResponse,
)


class ClinicalNoteRoute:
  def __init__(self) -> None:
    self.router = APIRouter()
    self.controller = ClinicalNoteController()
    self._register_routes()

  def _register_routes(self) -> None:
    self.router.add_api_route(
        path="/clinical-notes",
        endpoint=self.controller.create,
        methods=["POST"],
        description="Create a new Clinical Note",
        dependencies=[Depends(Authenticate([StaffRole.DOCTOR]))],
        status_code=201,
        responses=get_responses(201, 400, 401, 500),
        response_model=BaseResponse[CreateDataResponse]
    )

    self.router.add_api_route(
        path="/clinical-notes/{id}/{encounter_id}",
        endpoint=self.controller.update,
        methods=["PUT"],
        description="Update an existing Clinical Note",
        dependencies=[Depends(Authenticate([StaffRole.DOCTOR]))],
        responses=get_responses(200, 400, 401, 404, 500),
        response_model=BaseResponse[UpdateDataResponse]
    )

    self.router.add_api_route(
        path="/clinical-notes/{encounter_id}",
        endpoint=self.controller.getAll,
        methods=["GET"],
        description="Get all Clinical Notes For an Encounter",
        dependencies=[Depends(Authenticate([StaffRole.DOCTOR]))],
        responses=get_responses(200, 401, 500),
        response_model=APIResponse[List[ClinicalNoteResponseSchema]]
    )

    self.router.add_api_route(
        path="/clinical-notes/{id}/{encounter_id}",
        endpoint=self.controller.getOne,
        methods=["GET"],
        description="Get a Single Clinical Note",
        dependencies=[Depends(Authenticate([StaffRole.DOCTOR]))],
        responses=get_responses(200, 401, 404, 500),
        response_model=BaseResponse[ClinicalNoteResponseSchema]
    )

    self.router.add_api_route(
        path="/clinical-notes/{id}/{encounter_id}",
        endpoint=self.controller.delete,
        methods=["DELETE"],
        description="Soft delete a Clinical Note",
        dependencies=[Depends(Authenticate([StaffRole.DOCTOR]))],
        responses=get_responses(200, 401, 404, 500),
        response_model=BaseResponse[str]
    )

    self.router.add_api_route(
        path="/clinical-notes/{id}/{encounter_id}/restore",
        endpoint=self.controller.restore,
        methods=["PATCH"],
        description="Restore a soft-deleted Clinical Note",
        dependencies=[Depends(Authenticate([StaffRole.DOCTOR]))],
        responses=get_responses(200, 401, 404, 500),
        response_model=BaseResponse[str]
    )
