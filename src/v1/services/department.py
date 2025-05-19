
import datetime
from uuid import UUID
import bcrypt
from sqlalchemy.orm import Session

from v1.errors import AppException
from v1.models import DepartmentModel
from v1.schemas import DepartmentCreateRequestSchema, DepartmentUpdateRequestSchema, DepartmentResponseSchema
from v1.type_defs import APIResponse, ErrorTypeEnum, CreateDataResponse, UpdateDataResponse
from typing_extensions import List


class DepartmentService:
  def __init__(self) -> None:
    None

  def create(self, data: DepartmentCreateRequestSchema,
            db: Session) -> APIResponse[CreateDataResponse]:
    try:
      department = DepartmentModel(**data.model_dump())
      db.add(department)
      db.commit()
      db.refresh(department)

      return {
          "data": {
            "id": department.id,
            "message": f"Department {department.name} created successfully"
          }
      }

    except Exception as exc:
      raise AppException.classify_error(exc)
    
    
  def update(self, id: UUID, data: DepartmentUpdateRequestSchema,
            db: Session) -> APIResponse[UpdateDataResponse]:
    try:
      department = db.query(DepartmentModel).filter(
        DepartmentModel.id==id,
        DepartmentModel.deleted_at.is_(None)
      ).first()
      
      if not department:
        raise AppException(type=ErrorTypeEnum.NOT_FOUND)

      update_data = data.model_dump(exclude_unset=True)
      for key, value in update_data.items():
        setattr(department, key, value if value is not None else getattr(department, key))

      db.commit()
      db.refresh(department)

      return {
          "data": {
            "id": department.id,
            "message": f"Department {department.name} updated successfully"
          }
      }

    except Exception as exc:
      raise AppException.classify_error(exc)
    
  def getAll(self, db: Session) -> APIResponse[List[DepartmentResponseSchema]]:
    try:
      departments = db.query(DepartmentModel).filter(
        DepartmentModel.deleted_at.is_(None)
      ).all()

      result = [
        DepartmentResponseSchema(
          id=dept.id,
          name=dept.name,
          description=dept.description,
          created_at=dept.created_at,
          updated_at=dept.updated_at
        )
        for dept in departments
      ]

      return {
        "data": result
      }

    except Exception as exc:
      raise AppException.classify_error(exc)
    
  def getOne(self, id: UUID, db: Session) -> APIResponse[DepartmentResponseSchema]:
    try:
      department = db.query(DepartmentModel).filter(
        DepartmentModel.id == id,
        DepartmentModel.deleted_at.is_(None)
      ).first()
      
      if not department:
        raise AppException(type=ErrorTypeEnum.NOT_FOUND)

      result = DepartmentResponseSchema(
          id=department.id,
          name=department.name,
          description=department.description,
          created_at=department.created_at,
          updated_at=department.updated_at
        )
        

      return {
        "data": result
      }

    except Exception as exc:
      raise AppException.classify_error(exc)
    
  def delete(self, id: UUID, db: Session) -> APIResponse[str]:
    try:
      department = db.query(DepartmentModel).filter(
        DepartmentModel.id == id,
        DepartmentModel.deleted_at.is_(None)
      ).first()
      
      if not department:
        raise AppException(type=ErrorTypeEnum.NOT_FOUND)

      department.deleted_at = datetime.datetime.now(datetime.timezone.utc)
      db.commit()
      db.refresh(department)
      
      return {
        "data": f"Department {department.id} deleted successfully"
      }

    except Exception as exc:
      raise AppException.classify_error(exc)
    
    
  def restore(self, id: UUID, db: Session) -> APIResponse[str]:
    try:
      department = db.query(DepartmentModel).filter(
        DepartmentModel.id == id,
        DepartmentModel.deleted_at.is_not_(None)
      ).first()
      
      if not department:
        raise AppException(type=ErrorTypeEnum.NOT_FOUND)

      department.deleted_at = None
      db.commit()
      db.refresh(department)
      
      return {
        "data": f"Department {department.id} restored successfully"
      }

    except Exception as exc:
      raise AppException.classify_error(exc)
