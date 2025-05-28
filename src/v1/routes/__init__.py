from fastapi import APIRouter
from typing_extensions import List, Sequence, Tuple

from .app import AppRoute
from .auth import AuthRoute
from .clinical_encounter import ClinicalEncounterRoute
from .department import DepartmentRoute
from .patient import PatientRoute
from .staff import StaffRoute

app_routes: APIRouter = AppRoute().router
auth_routes: APIRouter = AuthRoute().router
department_routes: APIRouter = DepartmentRoute().router
staff_routes: APIRouter = StaffRoute().router
patient_routes: APIRouter = PatientRoute().router
clinical_encounter_routes: APIRouter = ClinicalEncounterRoute().router

all_routes: Sequence[Tuple[APIRouter, List[str]]] = [
    (auth_routes, ["Auth"]),
    (clinical_encounter_routes, ["Clinical Encounter"]),
    (department_routes, ["Department"]),
    (app_routes, ["Health"]),
    (staff_routes, ["Staff"]),
    (patient_routes, ["Patient"])
]

__all__ = ["all_routes"]
