
import datetime
from uuid import UUID

from sqlalchemy import asc
from sqlalchemy.orm import Session
from typing_extensions import List

from v1.errors import AppException
from v1.models import ClinicalNoteModel
from v1.schemas import (
  ClinicalNoteCreateRequestSchema,
  ClinicalNoteResponseSchema,
  ClinicalNoteUpdateRequestSchema,
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


class ClinicalNoteService:
  def __init__(self) -> None:
    None

  def create(self, data: ClinicalNoteCreateRequestSchema, auth_payload: JWTTokenPayload,
             db: Session) -> APIResponse[CreateDataResponse]:
    try:
      clinical_note_data = data.model_dump()
      clinical_note_data.pop("encounter")
      clinical_note = ClinicalNoteModel(**clinical_note_data)

      clinical_note.encounter_id = data.encounter.id
      clinical_note.note_author_id = UUID(auth_payload["id"])
      print(clinical_note.note_author_id)

      db.add(clinical_note)
      db.commit()
      db.refresh(clinical_note)

      return {
          "data": {
              "id": clinical_note.id,
              "message": f"Clinical note created successfully"
          }
      }

    except Exception as exc:
      raise AppException.classify_error(exc)

  def update(self, id: UUID, encounter_id: UUID, data: ClinicalNoteUpdateRequestSchema, auth_payload: JWTTokenPayload,
             db: Session) -> APIResponse[UpdateDataResponse]:
    try:
      clinical_note = db.query(ClinicalNoteModel).filter(
          ClinicalNoteModel.id == id,
          ClinicalNoteModel.encounter_id == encounter_id,
          ClinicalNoteModel.deleted_at.is_(None)
      ).first()

      if not clinical_note:
        raise AppException(type=ErrorTypeEnum.NOT_FOUND)

      update_data = data.model_dump(exclude_unset=True)
      for key, value in update_data.items():
        setattr(
            clinical_note,
            key,
            value if value is not None else getattr(
                clinical_note,
                key))

      clinical_note.note_author_id = UUID(auth_payload["id"])

      db.commit()
      db.refresh(clinical_note)

      return {
          "data": {
              "id": clinical_note.id,
              "message": f"Clinical note updated successfully"
          }
      }

    except Exception as exc:
      raise AppException.classify_error(exc)

  def getAll(self, encounter_id: UUID, limit: int, offset: int,
             db: Session) -> APIResponse[List[ClinicalNoteResponseSchema]]:
    try:
      clinical_notes = db.query(ClinicalNoteModel).filter(
          ClinicalNoteModel.deleted_at.is_(None),
          ClinicalNoteModel.encounter_id == encounter_id
      ).order_by(asc(ClinicalNoteModel.created_at)).offset(offset).limit(limit).all()

      total = db.query(ClinicalNoteModel).filter(
          ClinicalNoteModel.deleted_at.is_(None),
          ClinicalNoteModel.encounter_id == encounter_id
      ).count()

      result = [
          ClinicalNoteResponseSchema(
              id=clinical_note.id,
              note_type=clinical_note.note_type,
              note_content=clinical_note.note_content,
              created_at=clinical_note.created_at,
              updated_at=clinical_note.updated_at,
              note_author=StaffResponseSchema(
                  id=clinical_note.staff.id,
                  email=clinical_note.staff.email,
                  title=clinical_note.staff.title,
                  surname=clinical_note.staff.surname,
                  first_name=clinical_note.staff.first_name,
                  last_name=clinical_note.staff.last_name,
                  role=clinical_note.staff.role,
                  departments=[
                      StaffDepartmentResponseSchema(
                          id=dept.id,
                          name=dept.name,
                          description=dept.description
                      )
                      for dept in clinical_note.staff.departments
                  ]
              )
          )
          for clinical_note in clinical_notes
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

  def getOne(self, id: UUID, encounter_id: UUID,
             db: Session) -> APIResponse[ClinicalNoteResponseSchema]:
    try:
      clinical_note = db.query(ClinicalNoteModel).filter(
          ClinicalNoteModel.id == id,
          ClinicalNoteModel.encounter_id == encounter_id,
          ClinicalNoteModel.deleted_at.is_(None)
      ).first()

      if not clinical_note:
        raise AppException(type=ErrorTypeEnum.NOT_FOUND)

      result = ClinicalNoteResponseSchema(
          id=clinical_note.id,
          note_type=clinical_note.note_type,
          note_content=clinical_note.note_content,
          created_at=clinical_note.created_at,
          updated_at=clinical_note.updated_at,
          note_author=StaffResponseSchema(
              id=clinical_note.staff.id,
              email=clinical_note.staff.email,
              title=clinical_note.staff.title,
              surname=clinical_note.staff.surname,
              first_name=clinical_note.staff.first_name,
              last_name=clinical_note.staff.last_name,
              role=clinical_note.staff.role,
              departments=[
                  StaffDepartmentResponseSchema(
                      id=dept.id,
                      name=dept.name,
                      description=dept.description
                  )
                  for dept in clinical_note.staff.departments
              ]
          )
      )

      return {
          "data": result
      }

    except Exception as exc:
      raise AppException.classify_error(exc)

  def delete(self, id: UUID, encounter_id: UUID,
             db: Session) -> APIResponse[str]:
    try:
      clinical_note = db.query(ClinicalNoteModel).filter(
          ClinicalNoteModel.id == id,
          ClinicalNoteModel.encounter_id == encounter_id,
          ClinicalNoteModel.deleted_at.is_(None)
      ).first()

      if not clinical_note:
        raise AppException(type=ErrorTypeEnum.NOT_FOUND)

      clinical_note.deleted_at = datetime.datetime.now(datetime.timezone.utc)
      db.commit()
      db.refresh(clinical_note)

      return {
          "data": f"Clinical note {clinical_note.id} deleted successfully"
      }

    except Exception as exc:
      raise AppException.classify_error(exc)

  def restore(self, id: UUID, encounter_id: UUID,
              db: Session) -> APIResponse[str]:
    try:
      clinical_note = db.query(ClinicalNoteModel).filter(
          ClinicalNoteModel.id == id,
          ClinicalNoteModel.encounter_id == encounter_id,
          ClinicalNoteModel.deleted_at.isnot(None)
      ).first()

      if not clinical_note:
        raise AppException(type=ErrorTypeEnum.NOT_FOUND)

      clinical_note.deleted_at = None
      db.commit()
      db.refresh(clinical_note)

      return {
          "data": f"Clinical note {clinical_note.id} restored successfully"
      }

    except Exception as exc:
      raise AppException.classify_error(exc)
