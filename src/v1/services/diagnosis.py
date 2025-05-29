
import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from v1.errors import AppException
from v1.models import DiagnosisModel
from v1.schemas import (
  DiagnosisCreateRequestSchema,
  DiagnosisResponseSchema,
  DiagnosisUpdateRequestSchema,
  StaffDepartmentResponseSchema,
  StaffResponseSchema,
)
from v1.type_defs import (
  APIResponse,
  CreateDataResponse,
  ErrorTypeEnum,
  JWTTokenPayload,
  UpdateDataResponse,
)


class DiagnosisService:
  def __init__(self) -> None:
    None

  def create(self, data: DiagnosisCreateRequestSchema, auth_payload: JWTTokenPayload,
             db: Session) -> APIResponse[CreateDataResponse]:
    try:
      diagnosis_data = data.model_dump()
      diagnosis_data.pop("diagnosis")
      diagnosis = DiagnosisModel(**diagnosis_data)

      diagnosis.encounter_id = data.encounter.id
      diagnosis.diagnosed_by_id = UUID(auth_payload["id"])

      db.add(diagnosis)
      db.commit()
      db.refresh(diagnosis)

      return {
          "data": {
              "id": diagnosis.id,
              "message": f"Diagnosis created successfully"
          }
      }

    except Exception as exc:
      raise AppException.classify_error(exc)

  def update(self, id: UUID, data: DiagnosisUpdateRequestSchema, auth_payload: JWTTokenPayload,
             db: Session) -> APIResponse[UpdateDataResponse]:
    try:
      diagnosis = db.query(DiagnosisModel).filter(
          DiagnosisModel.id == id,
          DiagnosisModel.deleted_at.is_(None)
      ).first()

      if not diagnosis:
        raise AppException(type=ErrorTypeEnum.NOT_FOUND)

      update_data = data.model_dump(exclude_unset=True)
      for key, value in update_data.items():
        setattr(
            diagnosis,
            key,
            value if value is not None else getattr(
                diagnosis,
                key))

      diagnosis.diagnosed_by_id = UUID(auth_payload["id"])

      db.commit()
      db.refresh(diagnosis)

      return {
          "data": {
              "id": diagnosis.id,
              "message": f"Diagnosis updated successfully"
          }
      }

    except Exception as exc:
      raise AppException.classify_error(exc)

  def getOne(self, id: UUID,
             db: Session) -> APIResponse[DiagnosisResponseSchema]:
    try:
      diagnosis = db.query(DiagnosisModel).filter(
          DiagnosisModel.id == id,
          DiagnosisModel.deleted_at.is_(None)
      ).first()

      if not diagnosis:
        raise AppException(type=ErrorTypeEnum.NOT_FOUND)

      result = DiagnosisResponseSchema(
          id=diagnosis.id,
          diagnosis_description=diagnosis.diagnosis_description,
          diagnosed_by=StaffResponseSchema(
              id=diagnosis.staff.id,
              email=diagnosis.staff.email,
              title=diagnosis.staff.title,
              surname=diagnosis.staff.surname,
              first_name=diagnosis.staff.first_name,
              last_name=diagnosis.staff.last_name,
              role=diagnosis.staff.role,
              departments=[
                  StaffDepartmentResponseSchema(
                      id=dept.id,
                      name=dept.name,
                      description=dept.description
                  )
                  for dept in diagnosis.staff.departments
              ]
          ),
          notes=diagnosis.notes,
          created_at=diagnosis.created_at,
          updated_at=diagnosis.updated_at
      )

      return {
          "data": result
      }

    except Exception as exc:
      raise AppException.classify_error(exc)

  def delete(self, id: UUID, db: Session) -> APIResponse[str]:
    try:
      diagnosis = db.query(DiagnosisModel).filter(
          DiagnosisModel.id == id,
          DiagnosisModel.deleted_at.is_(None)
      ).first()

      if not diagnosis:
        raise AppException(type=ErrorTypeEnum.NOT_FOUND)

      diagnosis.deleted_at = datetime.datetime.now(datetime.timezone.utc)
      db.commit()
      db.refresh(diagnosis)

      return {
          "data": f"Diagnosis {diagnosis.id} deleted successfully"
      }

    except Exception as exc:
      raise AppException.classify_error(exc)

  def restore(self, id: UUID, db: Session) -> APIResponse[str]:
    try:
      diagnosis = db.query(DiagnosisModel).filter(
          DiagnosisModel.id == id,
          DiagnosisModel.deleted_at.isnot(None)
      ).first()

      if not diagnosis:
        raise AppException(type=ErrorTypeEnum.NOT_FOUND)

      diagnosis.deleted_at = None
      db.commit()
      db.refresh(diagnosis)

      return {
          "data": f"Diagnosis {diagnosis.id} restored successfully"
      }

    except Exception as exc:
      raise AppException.classify_error(exc)
