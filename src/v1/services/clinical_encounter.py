
import datetime
from uuid import UUID

from sqlalchemy import asc
from sqlalchemy.orm import Session
from typing_extensions import List

from v1.errors import AppException
from v1.models import ClinicalEncounterModel
from v1.schemas import (
  ClinicalEncounterCreateRequestSchema,
  ClinicalEncounterResponseSchema,
  ClinicalEncounterUpdateRequestSchema,
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


class ClinicalEncounterService:
  def __init__(self) -> None:
    None

  def create(self, data: ClinicalEncounterCreateRequestSchema, auth_payload: JWTTokenPayload,
             db: Session) -> APIResponse[CreateDataResponse]:
    try:
      encounter_data = data.model_dump()
      encounter_data.pop("patient")
      encounter = ClinicalEncounterModel(**encounter_data)

      encounter.patient_id = data.patient.id
      encounter.attending_doctor_id = UUID(auth_payload["id"])

      db.add(encounter)
      db.commit()
      db.refresh(encounter)

      return {
          "data": {
              "id": encounter.id,
              "message": f"Clinical Encounter created successfully"
          }
      }

    except Exception as exc:
      raise AppException.classify_error(exc)

  def update(self, id: UUID, patient_id: UUID, data: ClinicalEncounterUpdateRequestSchema, auth_payload: JWTTokenPayload,
             db: Session) -> APIResponse[UpdateDataResponse]:
    try:
      encounter = db.query(ClinicalEncounterModel).filter(
          ClinicalEncounterModel.id == id,
          ClinicalEncounterModel.patient_id == patient_id,
          ClinicalEncounterModel.deleted_at.is_(None)
      ).first()

      if not encounter:
        raise AppException(type=ErrorTypeEnum.NOT_FOUND)

      update_data = data.model_dump(exclude_unset=True)
      for key, value in update_data.items():
        setattr(
            encounter,
            key,
            value if value is not None else getattr(
                encounter,
                key))

      encounter.attending_doctor_id = UUID(auth_payload["id"])

      db.commit()
      db.refresh(encounter)

      return {
          "data": {
              "id": encounter.id,
              "message": f"Encounter updated successfully"
          }
      }

    except Exception as exc:
      raise AppException.classify_error(exc)

  def getAll(self, patient_id: UUID, limit: int, offset: int,
             db: Session) -> APIResponse[List[ClinicalEncounterResponseSchema]]:
    try:
      encounters = db.query(ClinicalEncounterModel).filter(
          ClinicalEncounterModel.deleted_at.is_(None),
          ClinicalEncounterModel.patient_id == patient_id
      ).order_by(asc(ClinicalEncounterModel.created_at)).offset(offset).limit(limit).all()

      total = db.query(ClinicalEncounterModel).filter(
          ClinicalEncounterModel.deleted_at.is_(None),
          ClinicalEncounterModel.patient_id == patient_id
      ).count()

      result = [
          ClinicalEncounterResponseSchema(
              id=encounter.id,
              encounter_type=encounter.encounter_type,
              presenting_complaint=encounter.presenting_complaint,
              status=encounter.status,
              created_at=encounter.created_at,
              start_date=encounter.start_date,
              end_date=encounter.end_date,
              attending_doctor=StaffResponseSchema(
                  id=encounter.staff.id,
                  email=encounter.staff.email,
                  title=encounter.staff.title,
                  surname=encounter.staff.surname,
                  first_name=encounter.staff.first_name,
                  last_name=encounter.staff.last_name,
                  role=encounter.staff.role,
                  departments=[
                      StaffDepartmentResponseSchema(
                          id=dept.id,
                          name=dept.name,
                          description=dept.description
                      )
                      for dept in encounter.staff.departments
                  ]
              )
          )
          for encounter in encounters
      ]

      return {
          "data": result,
          "metadata": {
              "total": total,
              "count": len(result),
              "page": offset // limit + 1,
          }
      }

    except Exception as exc:
      raise AppException.classify_error(exc)

  def getOne(self, id: UUID, patient_id: UUID,
             db: Session) -> APIResponse[ClinicalEncounterResponseSchema]:
    try:
      encounter = db.query(ClinicalEncounterModel).filter(
          ClinicalEncounterModel.id == id,
          ClinicalEncounterModel.patient_id == patient_id,
          ClinicalEncounterModel.deleted_at.is_(None)
      ).first()

      if not encounter:
        raise AppException(type=ErrorTypeEnum.NOT_FOUND)

      result = ClinicalEncounterResponseSchema(
          id=encounter.id,
          encounter_type=encounter.encounter_type,
          presenting_complaint=encounter.presenting_complaint,
          status=encounter.status,
          created_at=encounter.created_at,
          start_date=encounter.start_date,
          end_date=encounter.end_date,
          attending_doctor=StaffResponseSchema(
              id=encounter.staff.id,
              email=encounter.staff.email,
              title=encounter.staff.title,
              surname=encounter.staff.surname,
              first_name=encounter.staff.first_name,
              last_name=encounter.staff.last_name,
              role=encounter.staff.role,
              departments=[
                  StaffDepartmentResponseSchema(
                      id=dept.id,
                      name=dept.name,
                      description=dept.description
                  )
                  for dept in encounter.staff.departments
              ]
          )
      )

      return {
          "data": result
      }

    except Exception as exc:
      raise AppException.classify_error(exc)

  def delete(self, id: UUID, patient_id: UUID, db: Session) -> APIResponse[str]:
    try:
      encounter = db.query(ClinicalEncounterModel).filter(
          ClinicalEncounterModel.id == id,
          ClinicalEncounterModel.patient_id == patient_id,
          ClinicalEncounterModel.deleted_at.is_(None)
      ).first()

      if not encounter:
        raise AppException(type=ErrorTypeEnum.NOT_FOUND)

      encounter.deleted_at = datetime.datetime.now(datetime.timezone.utc)
      db.commit()
      db.refresh(encounter)

      return {
          "data": f"Encounter {encounter.id} deleted successfully"
      }

    except Exception as exc:
      raise AppException.classify_error(exc)

  def restore(self, id: UUID, patient_id: UUID,
              db: Session) -> APIResponse[str]:
    try:
      encounter = db.query(ClinicalEncounterModel).filter(
          ClinicalEncounterModel.id == id,
          ClinicalEncounterModel.patient_id == patient_id,
          ClinicalEncounterModel.deleted_at.isnot(None)
      ).first()

      if not encounter:
        raise AppException(type=ErrorTypeEnum.NOT_FOUND)

      encounter.deleted_at = None
      db.commit()
      db.refresh(encounter)

      return {
          "data": f"Encounter {encounter.id} restored successfully"
      }

    except Exception as exc:
      raise AppException.classify_error(exc)

  def close_encounter(self, id: UUID, patient_id: UUID,
                      db: Session) -> APIResponse[str]:
    try:
      encounter = db.query(ClinicalEncounterModel).filter(
          ClinicalEncounterModel.id == id,
          ClinicalEncounterModel.patient_id == patient_id
      ).first()

      if not encounter:
        raise AppException(type=ErrorTypeEnum.NOT_FOUND)

      if encounter.end_date:
        raise AppException(
            type=ErrorTypeEnum.BAD_REQUEST,
            detail="This clinical encounter has already been closed and cannot be closed again."
        )

      encounter.end_date = datetime.datetime.now(datetime.timezone.utc)
      db.commit()
      db.refresh(encounter)

      return {
          "data": f"Encounter {encounter.id} closed successfully"
      }

    except Exception as exc:
      raise AppException.classify_error(exc)
