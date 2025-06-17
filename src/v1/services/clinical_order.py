import datetime
from uuid import UUID

from sqlalchemy import asc
from sqlalchemy.orm import Session, selectinload
from typing_extensions import List

from v1.errors import AppException
from v1.models import ClinicalOrderModel, StaffModel
from v1.schemas import (
  ClinicalOrderCreateRequestSchema,
  ClinicalOrderIdRef,
  ClinicalOrderOrderedByStaffResponse,
  ClinicalOrderResponseSchema,
  ClinicalOrderStaffDepartmentResponse,
  ClinicalOrderUpdateRequestSchema,
)
from v1.type_defs import (
  APIResponse,
  CreateDataResponse,
  ErrorTypeEnum,
  JWTTokenPayload,
  UpdateDataResponse,
)


class ClinicalOrderService:
  def __init__(self) -> None:
    pass

  def create(self, data: ClinicalOrderCreateRequestSchema, auth_payload: JWTTokenPayload,
             db: Session) -> APIResponse[CreateDataResponse]:
    try:
      order_data = data.model_dump()

      encounter_ref = order_data.pop("encounter")
      target_department_ref = order_data.pop("target_department")

      order = ClinicalOrderModel(**order_data)

      order.encounter_id = encounter_ref["id"]
      order.target_department_id = target_department_ref["id"]
      order.ordered_by_id = UUID(auth_payload["id"])

      db.add(order)
      db.commit()
      db.refresh(order)

      return {
          "data": {
              "id": order.id,
              "message": f"Clinical Order created successfully"
          }
      }

    except Exception as exc:
      raise AppException.classify_error(exc)

  def update(self, id: UUID, encounter_id: UUID, data: ClinicalOrderUpdateRequestSchema, auth_payload: JWTTokenPayload,
             db: Session) -> APIResponse[UpdateDataResponse]:
    try:
      order = db.query(ClinicalOrderModel).filter(
          ClinicalOrderModel.id == id,
          ClinicalOrderModel.encounter_id == encounter_id,
          ClinicalOrderModel.deleted_at.is_(None)
      ).first()

      if not order:
        raise AppException(type=ErrorTypeEnum.NOT_FOUND)

      update_data = data.model_dump(exclude_unset=True)

      for key, value in update_data.items():
        if key == "target_department":
          if value and "id" in value:
            setattr(order, "target_department_id", value["id"])
          elif value is None:
            setattr(order, "target_department_id", None)
        else:
          setattr(order, key, value)

      order.ordered_by_id = UUID(auth_payload["id"])

      db.commit()
      db.refresh(order)

      return {
          "data": {
              "id": order.id,
              "message": f"Clinical Order updated successfully"
          }
      }

    except Exception as exc:
      raise AppException.classify_error(exc)

  def getAll(self, encounter_id: UUID, limit: int, offset: int,
             db: Session) -> APIResponse[List[ClinicalOrderResponseSchema]]:
    try:
      orders = db.query(ClinicalOrderModel).filter(
          ClinicalOrderModel.deleted_at.is_(None),
          ClinicalOrderModel.encounter_id == encounter_id
      ).order_by(asc(ClinicalOrderModel.created_at)).offset(offset).limit(limit).all()

      total = db.query(ClinicalOrderModel).filter(
          ClinicalOrderModel.deleted_at.is_(None),
          ClinicalOrderModel.encounter_id == encounter_id
      ).count()

      result = []
      for order in orders:
        if order.ordered_by_id:
          staff = db.query(StaffModel).options(
              selectinload(StaffModel.departments)
          ).filter(
              StaffModel.id == order.ordered_by_id,
              StaffModel.deleted_at.is_(None)
          ).first()

          if staff:
            ordered_by_staff = ClinicalOrderOrderedByStaffResponse(
                id=staff.id,
                title=staff.title,
                name=f"{staff.first_name} {staff.surname}",
                departments=[
                    ClinicalOrderStaffDepartmentResponse(
                        id=dpt.id,
                        name=dpt.name
                    )
                    for dpt in staff.departments
                ]
            )

        result.append(
            ClinicalOrderResponseSchema(
                id=order.id,
                encounter=ClinicalOrderIdRef(id=order.encounter_id),
                order_type=order.order_type,
                order_details=order.order_details,
                target_department=ClinicalOrderIdRef(
                    id=order.target_department_id),
                ordered_by=ordered_by_staff,
                priority=order.priority,
                status=order.status,
                order_notes=order.order_notes,
                created_at=order.created_at,
                updated_at=order.updated_at,
            )
        )

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
             db: Session) -> APIResponse[ClinicalOrderResponseSchema]:
    try:
      order = db.query(ClinicalOrderModel).filter(
          ClinicalOrderModel.id == id,
          ClinicalOrderModel.encounter_id == encounter_id,
          ClinicalOrderModel.deleted_at.is_(None)
      ).first()

      if not order:
        raise AppException(type=ErrorTypeEnum.NOT_FOUND)

      if order.ordered_by_id:
        staff = db.query(StaffModel).options(
            selectinload(StaffModel.departments)
        ).filter(
            StaffModel.id == order.ordered_by_id,
            StaffModel.deleted_at.is_(None)
        ).first()

        if staff:
          ordered_by_staff = ClinicalOrderOrderedByStaffResponse(
              id=staff.id,
              title=staff.title,
              name=f"{staff.first_name} {staff.surname}",
              departments=[
                  ClinicalOrderStaffDepartmentResponse(
                      id=dpt.id,
                      name=dpt.name
                  )
                  for dpt in staff.departments
              ]
          )

      result = ClinicalOrderResponseSchema(
          id=order.id,
          encounter=ClinicalOrderIdRef(id=order.encounter_id),
          order_type=order.order_type,
          order_details=order.order_details,
          target_department=ClinicalOrderIdRef(id=order.target_department_id),
          ordered_by=ordered_by_staff,
          priority=order.priority,
          status=order.status,
          order_notes=order.order_notes,
          created_at=order.created_at,
          updated_at=order.updated_at,
      )

      return {
          "data": result
      }

    except Exception as exc:
      raise AppException.classify_error(exc)

  def delete(self, id: UUID, encounter_id: UUID,
             db: Session) -> APIResponse[str]:
    try:
      order = db.query(ClinicalOrderModel).filter(
          ClinicalOrderModel.id == id,
          ClinicalOrderModel.encounter_id == encounter_id,
          ClinicalOrderModel.deleted_at.is_(None)
      ).first()

      if not order:
        raise AppException(type=ErrorTypeEnum.NOT_FOUND)

      order.deleted_at = datetime.datetime.now(datetime.timezone.utc)
      db.commit()
      db.refresh(order)

      return {
          "data": f"Clinical Order {order.id} deleted successfully"
      }

    except Exception as exc:
      raise AppException.classify_error(exc)

  def restore(self, id: UUID, encounter_id: UUID,
              db: Session) -> APIResponse[str]:
    try:
      order = db.query(ClinicalOrderModel).filter(
          ClinicalOrderModel.id == id,
          ClinicalOrderModel.encounter_id == encounter_id,
          ClinicalOrderModel.deleted_at.isnot(None)
      ).first()

      if not order:
        raise AppException(type=ErrorTypeEnum.NOT_FOUND)

      order.deleted_at = None
      db.commit()
      db.refresh(order)

      return {
          "data": f"Clinical Order {order.id} restored successfully"
      }

    except Exception as exc:
      raise AppException.classify_error(exc)
