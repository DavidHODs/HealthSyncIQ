from .app import AppController
from .auth import AuthController
from .department import DepartmentController
from .patient import PatientController
from .staff import StaffController

__all__ = [
    "AppController",
    "AuthController",
    "DepartmentController",
    "StaffController",
    "PatientController"
]
