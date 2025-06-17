from fastapi import APIRouter
from typing_extensions import List, Sequence, Tuple

from .app import AppRoute
from .auth import AuthRoute
from .clinical_encounter import ClinicalEncounterRoute
from .clinical_note import ClinicalNoteRoute
from .department import DepartmentRoute
from .diagnosis import DiagnosisRoute
from .patient import PatientRoute
from .staff import StaffRoute
from .clinical_order import ClinicalOrderRoute

app_routes: APIRouter = AppRoute().router
auth_routes: APIRouter = AuthRoute().router
department_routes: APIRouter = DepartmentRoute().router
staff_routes: APIRouter = StaffRoute().router
patient_routes: APIRouter = PatientRoute().router
clinical_encounter_routes: APIRouter = ClinicalEncounterRoute().router
diagnosis_routes: APIRouter = DiagnosisRoute().router
clinical_note_routes: APIRouter = ClinicalNoteRoute().router
clinical_Order_routes: APIRouter = ClinicalOrderRoute().router

all_routes: Sequence[Tuple[APIRouter, List[str]]] = [
    (auth_routes, ["Auth"]),
    (clinical_encounter_routes, ["Clinical Encounter"]),
    (clinical_note_routes, ["Clinical Note"]),
    (clinical_Order_routes, ["Clinical Order"]),
    (department_routes, ["Department"]),
    (diagnosis_routes, ["Diagnosis"]),
    (app_routes, ["Health"]),
    (staff_routes, ["Staff"]),
    (patient_routes, ["Patient"]),
]

__all__ = ["all_routes"]
