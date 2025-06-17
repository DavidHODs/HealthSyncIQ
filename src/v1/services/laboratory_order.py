import datetime
from uuid import UUID

from sqlalchemy.orm import Session, selectinload

from v1.errors import AppException
from v1.models import LaboratoryOrderModel, StaffModel
from v1.schemas import (
  ClinicalOrderIdRef,
  LaboratoryOrderCreateRequestSchema,
  LaboratoryOrderResponseSchema,
  LaboratoryOrderUpdateRequestSchema,
  LaboratoryStaffDepartmentResponse,
  LaboratoryStaffResponse,
)
from v1.type_defs import (
  APIResponse,
  CreateDataResponse,
  ErrorTypeEnum,
  JWTTokenPayload,
  UpdateDataResponse,
)


class LaboratoryOrderService:
  def __init__(self) -> None:
    pass

  def create(self, data: LaboratoryOrderCreateRequestSchema, auth_payload: JWTTokenPayload,
             db: Session) -> APIResponse[CreateDataResponse]:
    try:
      order_data = data.model_dump()

      order_ref = order_data.pop("order")

      lab_order = LaboratoryOrderModel(**order_data)

      lab_order.order_id = order_ref["id"]
      lab_order.performed_by_id = UUID(auth_payload["id"])

      db.add(lab_order)
      db.commit()
      db.refresh(lab_order)

      return {
          "data": {
              "id": lab_order.id,
              "message": "Laboratory Order Result created successfully"
          }
      }

    except Exception as exc:
      raise AppException.classify_error(exc)

  def update(self, id: UUID, order_id: UUID, data: LaboratoryOrderUpdateRequestSchema, auth_payload: JWTTokenPayload,
             db: Session) -> APIResponse[UpdateDataResponse]:
    try:
      lab_order = db.query(LaboratoryOrderModel).filter(
          LaboratoryOrderModel.id == id,
          LaboratoryOrderModel.order_id == order_id,
          LaboratoryOrderModel.deleted_at.is_(None)
      ).first()

      if not lab_order:
        raise AppException(type=ErrorTypeEnum.NOT_FOUND)

      update_data = data.model_dump(exclude_unset=True)

      for key, value in update_data.items():
        if key == "verified_by":
          if value and "id" in value:
            setattr(lab_order, "verified_by_id", value["id"])
          elif value is None:
            setattr(lab_order, "verified_by_id", None)
        else:
          setattr(lab_order, key, value)

      db.commit()
      db.refresh(lab_order)

      return {
          "data": {
              "id": lab_order.id,
              "message": "Laboratory Order Result updated successfully"
          }
      }

    except Exception as exc:
      raise AppException.classify_error(exc)

  def getOne(self, id: UUID, order_id: UUID,
             db: Session) -> APIResponse[LaboratoryOrderResponseSchema]:
    try:
      lab_order = db.query(LaboratoryOrderModel).options(
          selectinload(LaboratoryOrderModel.order)
      ).filter(
          LaboratoryOrderModel.id == id,
          LaboratoryOrderModel.order_id == order_id,
          LaboratoryOrderModel.deleted_at.is_(None)
      ).first()

      if not lab_order:
        raise AppException(type=ErrorTypeEnum.NOT_FOUND)

      if lab_order.performed_by_id:
        performed_by_staff = db.query(StaffModel).options(
            selectinload(StaffModel.departments)
        ).filter(
            StaffModel.id == lab_order.performed_by_id,
            StaffModel.deleted_at.is_(None)
        ).first()
        if performed_by_staff:
          departments_data = [
              LaboratoryStaffDepartmentResponse(id=dpt.id, name=dpt.name)
              for dpt in performed_by_staff.departments
          ]
          performed_by_staff_response = LaboratoryStaffResponse(
              id=performed_by_staff.id,
              title=performed_by_staff.title,
              name=f"{performed_by_staff.first_name} {performed_by_staff.surname}",
              departments=departments_data
          )

      verified_by_staff_response = None
      if lab_order.verified_by_id:
        verified_by_staff = db.query(StaffModel).options(
            selectinload(StaffModel.departments)
        ).filter(
            StaffModel.id == lab_order.verified_by_id,
            StaffModel.deleted_at.is_(None)
        ).first()
        if verified_by_staff:
          departments_data = [
              LaboratoryStaffDepartmentResponse(id=dpt.id, name=dpt.name)
              for dpt in verified_by_staff.departments
          ]
          verified_by_staff_response = LaboratoryStaffResponse(
              id=verified_by_staff.id,
              title=verified_by_staff.title,
              name=f"{verified_by_staff.first_name} {verified_by_staff.surname}",
              departments=departments_data
          )

      result = LaboratoryOrderResponseSchema(
          id=lab_order.id,
          order=ClinicalOrderIdRef(id=lab_order.order_id),
          result_type=lab_order.result_type,
          result_data=lab_order.result_data,
          result_notes=lab_order.result_notes,
          file_attachments=lab_order.file_attachments,
          performed_by=performed_by_staff_response,
          verified_by=verified_by_staff_response,
          performed_at=lab_order.performed_at,
          verified_at=lab_order.verified_at,
          created_at=lab_order.created_at,
          updated_at=lab_order.updated_at,
          deleted_at=lab_order.deleted_at,
      )

      return {
          "data": result
      }

    except Exception as exc:
      raise AppException.classify_error(exc)

  def delete(self, id: UUID, order_id: UUID, db: Session) -> APIResponse[str]:
    try:
      lab_order = db.query(LaboratoryOrderModel).filter(
          LaboratoryOrderModel.id == id,
          LaboratoryOrderModel.order_id == order_id,
          LaboratoryOrderModel.deleted_at.is_(None)
      ).first()

      if not lab_order:
        raise AppException(type=ErrorTypeEnum.NOT_FOUND)

      lab_order.deleted_at = datetime.datetime.now(datetime.timezone.utc)
      db.commit()
      db.refresh(lab_order)

      return {
          "data": f"Laboratory Order Result {lab_order.id} deleted successfully"
      }

    except Exception as exc:
      raise AppException.classify_error(exc)

  def restore(self, id: UUID, order_id: UUID,
              db: Session) -> APIResponse[str]:
    try:
      lab_order = db.query(LaboratoryOrderModel).filter(
          LaboratoryOrderModel.id == id,
          LaboratoryOrderModel.order_id == order_id,
          LaboratoryOrderModel.deleted_at.isnot(None)
      ).first()

      if not lab_order:
        raise AppException(type=ErrorTypeEnum.NOT_FOUND)

      lab_order.deleted_at = None
      db.commit()
      db.refresh(lab_order)

      return {
          "data": f"Laboratory Order Result {lab_order.id} restored successfully"
      }

    except Exception as exc:
      raise AppException.classify_error(exc)
