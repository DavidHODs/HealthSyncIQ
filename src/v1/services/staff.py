
import datetime
import string
import uuid
from uuid import UUID

import bcrypt
from sqlalchemy import asc
from sqlalchemy.orm import Session, selectinload
from typing_extensions import Dict, List, Optional

from v1.errors import AppException
from v1.models import DepartmentMembershipModel, StaffModel
from v1.schemas import (
  StaffCreateRequestSchema,
  StaffDepartmentResponseSchema,
  StaffResponseSchema,
  StaffUpdateRequestSchema,
)
from v1.services.general.email import EmailService
import random
from v1.type_defs import (
  APIResponse,
  CreateDataResponse,
  ErrorTypeEnum,
  UpdateDataResponse,
)


class StaffService:
  def __init__(self) -> None:
    None

  def create(self, data: StaffCreateRequestSchema,
             db: Session) -> APIResponse[CreateDataResponse]:
    try:
      random_password = self._generate_password_()
      hashed_password = bcrypt.hashpw(
          random_password.encode("utf-8"),
          bcrypt.gensalt()).decode("utf-8")

      staff_data = data.model_dump(exclude={"departments"})
      staff_data["password"] = hashed_password

      departments_data: List[Dict[str, uuid.UUID]] = [
          dpt.model_dump() for dpt in data.departments]
      
      email_service = EmailService()
      html_template = email_service.load_html_template("src/v1/templates/account_password.html")
      html = html_template.format(name=f"{staff_data['title']} {staff_data['surname']}", password=random_password)
      email_service.send_html_email(staff_data["email"], "Welcome to HealthSyncIQ", html);

      staff = StaffModel(**staff_data)
      db.add(staff)
      db.flush()

      membership_objects: List[DepartmentMembershipModel] = []
      for dept_data in departments_data:
        membership = DepartmentMembershipModel(
            staff_id=staff.id,
            department_id=dept_data["id"]
        )
        membership_objects.append(membership)

      db.add_all(membership_objects)

      db.commit()

      db.refresh(staff)
      
      return {
          "data": {
              "id": staff.id,
              "message": f"Staff {staff.title} {staff.surname} {staff.first_name} created successfully Check email for your password"
          }
      }

    except Exception as exc:
      raise AppException.classify_error(exc)

  def update(self, id: UUID, data: StaffUpdateRequestSchema,
             db: Session) -> APIResponse[UpdateDataResponse]:
    try:
      staff = db.query(StaffModel).filter(
          StaffModel.id == id,
          StaffModel.deleted_at.is_(None)
      ).first()

      if not staff:
        raise AppException(type=ErrorTypeEnum.NOT_FOUND)

      staff_update_data = data.model_dump(exclude_unset=True)
      department_update_data: Optional[List[Dict[str, uuid.UUID]]] = staff_update_data.pop(
          "departments", None)

      if department_update_data is not None:
        new_department_ids = [dpt_data["id"]
                              for dpt_data in department_update_data]

        db.query(DepartmentMembershipModel).filter(
            DepartmentMembershipModel.staff_id == staff.id
        ).delete(synchronize_session=False)

        membership_objects: List[DepartmentMembershipModel] = []
        for dept_id in new_department_ids:
          membership = DepartmentMembershipModel(
              staff_id=staff.id,
              department_id=dept_id
          )
          membership_objects.append(membership)

        db.add_all(membership_objects)

      for key, value in staff_update_data.items():
        setattr(
            staff,
            key,
            value if value is not None else getattr(staff, key)
        )

      db.commit()
      db.refresh(staff)

      return {
          "data": {
              "id": staff.id,
              "message": f"Staff {staff.title} {staff.surname} {staff.first_name} updated successfully"
          }
      }

    except Exception as exc:
      raise AppException.classify_error(exc)

  def getAll(self, limit: int, offset: int,
             db: Session) -> APIResponse[List[StaffResponseSchema]]:
    try:
      staffs = db.query(StaffModel).options(
          selectinload(StaffModel.departments)
      ).filter(
          StaffModel.deleted_at.is_(None)
      ).order_by(asc(StaffModel.surname)).offset(offset).limit(limit).all()

      total = db.query(StaffModel).filter(
          StaffModel.deleted_at.is_(None)
      ).count()

      result = [
          StaffResponseSchema(
              id=staff.id,
              email=staff.email,
              title=staff.title,
              surname=staff.surname,
              first_name=staff.first_name,
              last_name=staff.last_name,
              role=staff.role,
              departments=[
                  StaffDepartmentResponseSchema(
                      id=dpt.id,
                      name=dpt.name,
                      description=dpt.description
                  )
                  for dpt in staff.departments
              ]
          )
          for staff in staffs
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

  def getOne(self, id: UUID,
             db: Session) -> APIResponse[StaffResponseSchema]:
    try:
      staff = db.query(StaffModel).options(
          selectinload(StaffModel.departments)
      ).filter(
          StaffModel.id == id,
          StaffModel.deleted_at.is_(None)
      ).first()

      if not staff:
        raise AppException(type=ErrorTypeEnum.NOT_FOUND)

      result = StaffResponseSchema(
          id=staff.id,
          email=staff.email,
          title=staff.title,
          surname=staff.surname,
          first_name=staff.first_name,
          last_name=staff.last_name,
          role=staff.role,
          departments=[
              StaffDepartmentResponseSchema(
                  id=dpt.id,
                  name=dpt.name,
                  description=dpt.description
              )
              for dpt in staff.departments
          ]
      )

      return {
          "data": result
      }

    except Exception as exc:
      raise AppException.classify_error(exc)

  def delete(self, id: UUID, db: Session) -> APIResponse[str]:
    try:
      staff = db.query(StaffModel).filter(
          StaffModel.id == id,
          StaffModel.deleted_at.is_(None)
      ).first()

      if not staff:
        raise AppException(type=ErrorTypeEnum.NOT_FOUND)

      staff.deleted_at = datetime.datetime.now(datetime.timezone.utc)
      db.commit()
      db.refresh(staff)

      return {
          "data": f"Staff {staff.id} deleted successfully"
      }

    except Exception as exc:
      raise AppException.classify_error(exc)

  def restore(self, id: UUID, db: Session) -> APIResponse[str]:
    try:
      staff = db.query(StaffModel).filter(
          StaffModel.id == id,
          StaffModel.deleted_at.isnot(None)
      ).first()

      if not staff:
        raise AppException(type=ErrorTypeEnum.NOT_FOUND)

      staff.deleted_at = None
      db.commit()
      db.refresh(staff)

      return {
          "data": f"Staff {staff.id} restored successfully"
      }

    except Exception as exc:
      raise AppException.classify_error(exc)
    
  def _generate_password_(self, length: int = 8) -> str:
    symbols = "!@#$%&*"

    required = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice(symbols)
    ]

    safe_chars = (
        string.ascii_uppercase +
        string.ascii_lowercase +
        string.digits +
        symbols
    )

    remaining = random.choices(safe_chars, k=length - len(required))
    all_chars = required + remaining
    random.shuffle(all_chars)
    return ''.join(all_chars)
