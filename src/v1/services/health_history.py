from uuid import UUID

from sqlalchemy import asc
from sqlalchemy.orm import Session, selectinload
from typing_extensions import List

from v1.errors import AppException
from v1.models import (
  ClinicalEncounterModel,
  ClinicalOrderModel,
  DiagnosisModel,
  LaboratoryOrderModel,
  PatientModel,
  StaffModel,
)
from v1.schemas import (
  EncounterSummarySchema,
  HealthHistorySummarySchema,
  PatientInfoSchema,
)
from v1.type_defs import APIResponse, ErrorTypeEnum


class HealthHistorySummarizationService:
  def __init__(self) -> None:
    pass

  def build_summary(self, patient_id: UUID,
                    db: Session) -> APIResponse[HealthHistorySummarySchema]:
    try:
      patient = db.query(PatientModel).filter(
          PatientModel.id == patient_id,
          PatientModel.deleted_at.is_(None)
      ).first()

      if not patient:
        raise AppException(type=ErrorTypeEnum.NOT_FOUND)

      patient_summary = PatientInfoSchema(
          dob=patient.dob,
          gender=patient.gender,
          genotype=patient.genotype,
          blood_group=patient.blood_group,
          meta=patient.meta
      )

      encounter_models = db.query(ClinicalEncounterModel).options(
          selectinload(
              ClinicalEncounterModel.staff).selectinload(
              StaffModel.departments)
      ).filter(
          ClinicalEncounterModel.patient_id == patient_id,
          ClinicalEncounterModel.deleted_at.is_(None)
      ).order_by(asc(ClinicalEncounterModel.created_at)).all()

      summaries: List[EncounterSummarySchema] = []
      for enc in encounter_models:
        diagnosis = db.query(DiagnosisModel).filter(
            DiagnosisModel.encounter_id == enc.id,
            DiagnosisModel.deleted_at.is_(None)
        ).first()

        lab_orders = db.query(LaboratoryOrderModel).join(ClinicalOrderModel).filter(
            ClinicalOrderModel.encounter_id == enc.id,
            LaboratoryOrderModel.deleted_at.is_(None)
        ).all()

        lab_struct = [lab.result_data for lab in lab_orders]

        summaries.append(EncounterSummarySchema(
            date=enc.created_at,
            type=enc.encounter_type,
            doctor=f"{enc.staff.title} {enc.staff.first_name} {enc.staff.last_name}",
            complaint=enc.presenting_complaint,
            diagnosis=diagnosis.diagnosis_description if diagnosis else None,
            labs=lab_struct
        ))

      health_history = HealthHistorySummarySchema(
          patient=patient_summary,
          encounter_summaries=summaries
      )

      return {"data": health_history}
    except Exception as exc:
      raise AppException.classify_error(exc)
