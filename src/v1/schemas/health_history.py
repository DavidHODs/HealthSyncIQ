from datetime import date, datetime

from pydantic import BaseModel
from typing_extensions import Any, Dict, List, Optional


class PatientInfoSchema(BaseModel):
  dob: Optional[date]
  gender: Optional[str]
  genotype: Optional[str]
  blood_group: Optional[str]
  meta: Optional[List[Dict[str, str]]] = []


class EncounterSummarySchema(BaseModel):
  date: datetime
  type: str
  doctor: Optional[str]
  complaint: Optional[str]
  diagnosis: Optional[str]
  labs: Optional[List[Dict[str, Any]]] = []


class HealthHistorySummarySchema(BaseModel):
  patient: PatientInfoSchema
  encounter_summaries: List[EncounterSummarySchema]

  class Config:
    json_schema_extra = {
        "example": {
            "patient": {
                "dob": "1977-06-12",
                "gender": "Male",
                "genotype": "AA",
                "blood_group": "O+",
                "meta": [
                    {"allergy": "Penicillin"},
                    {"allergy": "Peanuts"},
                    {"chronic_condition": "Diabetes"},
                    {"chronic_condition": "Hypertension"}
                ]
            },
            "encounter_summaries": [
                {
                    "date": "2025-05-17T00:00:00",
                    "type": "Consultation",
                    "doctor": "Dr. Jane Smith",
                    "complaint": "Fever and cough",
                    "diagnosis": "Acute bronchitis",
                    "labs": []
                }
            ]
        }
    }
