
import datetime
from uuid import UUID

from sqlalchemy import asc
from sqlalchemy.orm import Session
from typing_extensions import List

from v1.errors import AppException
from v1.models import PatientModel
from v1.schemas import (
  PatientCreateRequestSchema,
  PatientResponseSchema,
  PatientUpdateRequestSchema,
)
from v1.type_defs import (
  APIResponse,
  CreateDataResponse,
  ErrorTypeEnum,
  UpdateDataResponse,
)

from .general.encryption import EncryptionService


class PatientService:
  def __init__(self) -> None:
    self.encryption_service = EncryptionService()
    self.SENSITIVE_FIELDS = {
        "surname", "first_name", "last_name", "email",
        "phone_number", "contact_information", "emergency_contact"
    }
    None

  def create(self, data: PatientCreateRequestSchema,
             db: Session) -> APIResponse[CreateDataResponse]:
    try:
      patient = PatientModel(**data.model_dump())

      patient.registration_code = self.encryption_service.generate_registration_code()

      for field in self.SENSITIVE_FIELDS:
        setattr(
            patient,
            field,
            self.encryption_service.encrypt(
                getattr(
                    patient,
                    field)))

      db.add(patient)
      db.commit()
      db.refresh(patient)

      return {
          "data": {
              "id": patient.id,
              "message": f"Patient {self.encryption_service.decrypt(patient.first_name)} {self.encryption_service.decrypt(patient.last_name)} created successfully"
          }
      }

    except Exception as exc:
      raise AppException.classify_error(exc)

  def update(self, id: UUID, data: PatientUpdateRequestSchema,
             db: Session) -> APIResponse[UpdateDataResponse]:
    try:
      patient = db.query(PatientModel).filter(
          PatientModel.id == id,
          PatientModel.deleted_at.is_(None)
      ).first()

      if not patient:
        raise AppException(type=ErrorTypeEnum.NOT_FOUND)

      update_data = data.model_dump(exclude_unset=True)
      for key, value in update_data.items():
        if key in self.SENSITIVE_FIELDS:
          encrypted_value = self.encryption_service.encrypt(value)
          setattr(patient, key, encrypted_value)
        else:
          setattr(
              patient,
              key,
              value if value is not None else getattr(
                  patient,
                  key))

      db.commit()
      db.refresh(patient)

      return {
          "data": {
              "id": patient.id,
              "message": f"Patient {self.encryption_service.decrypt(patient.first_name)} {self.encryption_service.decrypt(patient.last_name)} updated successfully"
          }
      }

    except Exception as exc:
      raise AppException.classify_error(exc)

  def getAll(self, limit: int, offset: int,
             db: Session) -> APIResponse[List[PatientResponseSchema]]:
    try:
      patients = db.query(PatientModel).filter(
          PatientModel.deleted_at.is_(None)
      ).order_by(asc(PatientModel.created_at)).offset(offset).limit(limit).all()
      total = db.query(PatientModel).filter(
          PatientModel.deleted_at.is_(None)
      ).count()

      result = [
          PatientResponseSchema(
              id=patient.id,
              registration_code=patient.registration_code,
              surname=self.encryption_service.decrypt(patient.surname),
              first_name=self.encryption_service.decrypt(patient.first_name),
              last_name=self.encryption_service.decrypt(
                  patient.last_name) if patient.last_name else None,
              dob=patient.dob,
              genotype=patient.genotype,
              blood_group=patient.blood_group,
              gender=patient.gender,
              contact_information=self.encryption_service.decrypt(
                  patient.contact_information) if patient.contact_information else None,
              emergency_contact=self.encryption_service.decrypt(
                  patient.emergency_contact) if patient.emergency_contact else None,
              email=self.encryption_service.decrypt(patient.email),
              phone_number=self.encryption_service.decrypt(
                  patient.phone_number) if patient.phone_number else None,
              created_at=patient.created_at,
              updated_at=patient.updated_at
          )
          for patient in patients
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
             db: Session) -> APIResponse[PatientResponseSchema]:
    try:
      patient = db.query(PatientModel).filter(
          PatientModel.id == id,
          PatientModel.deleted_at.is_(None)
      ).first()

      if not patient:
        raise AppException(type=ErrorTypeEnum.NOT_FOUND)

      result = PatientResponseSchema(
          id=patient.id,
          registration_code=patient.registration_code,
          surname=self.encryption_service.decrypt(patient.surname),
          first_name=self.encryption_service.decrypt(patient.first_name),
          last_name=self.encryption_service.decrypt(
              patient.last_name) if patient.last_name else None,
          dob=patient.dob,
          genotype=patient.genotype,
          blood_group=patient.blood_group,
          gender=patient.gender,
          contact_information=self.encryption_service.decrypt(
              patient.contact_information) if patient.contact_information else None,
          emergency_contact=self.encryption_service.decrypt(
              patient.emergency_contact) if patient.emergency_contact else None,
          email=self.encryption_service.decrypt(patient.email),
          phone_number=self.encryption_service.decrypt(
              patient.phone_number) if patient.phone_number else None,
          created_at=patient.created_at,
          updated_at=patient.updated_at
      )

      return {
          "data": result
      }

    except Exception as exc:
      raise AppException.classify_error(exc)

  def delete(self, id: UUID, db: Session) -> APIResponse[str]:
    try:
      patient = db.query(PatientModel).filter(
          PatientModel.id == id,
          PatientModel.deleted_at.is_(None)
      ).first()

      if not patient:
        raise AppException(type=ErrorTypeEnum.NOT_FOUND)

      patient.deleted_at = datetime.datetime.now(datetime.timezone.utc)
      db.commit()
      db.refresh(patient)

      return {
          "data": f"Patient {patient.id} deleted successfully"
      }

    except Exception as exc:
      raise AppException.classify_error(exc)

  def restore(self, id: UUID, db: Session) -> APIResponse[str]:
    try:
      patient = db.query(PatientModel).filter(
          PatientModel.id == id,
          PatientModel.deleted_at.isnot(None)
      ).first()

      if not patient:
        raise AppException(type=ErrorTypeEnum.NOT_FOUND)

      patient.deleted_at = None
      db.commit()
      db.refresh(patient)

      return {
          "data": f"Patient {patient.id} restored successfully"
      }

    except Exception as exc:
      raise AppException.classify_error(exc)
