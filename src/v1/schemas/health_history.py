from datetime import date, datetime

from pydantic import BaseModel
from typing_extensions import Any, Dict, List, Optional


class PatientInfoSchema(BaseModel):
  dob: Optional[date]
  gender: Optional[str]
  genotype: Optional[str]
  blood_group: Optional[str]
  meta: Optional[Dict[str, Any]] = {}


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
                "allergies": ["Penicillin", "Peanuts"],
                "chronic_conditions": ["Diabetes", "Hypertension"]
            },
            "encounter_summaries": [
                {
                    "date": "2025-05-17",
                    "type": "Consultation",
                    "doctor": "Dr. Jane Smith",
                    "complaint": "Fever and cough",
                    "diagnosis": "Acute bronchitis",
                    "labs": {
                        "CBC": {
                            "hemoglobin": "14.2 g/dL",
                            "wbc": "8.5 x10^9/L",
                            "notes": "Routine check-up"
                        }
                    }
                }
            ]
        }
    }
