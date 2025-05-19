from .auth import LoginRequestSchema, LoginResponseSchema
from .clinical_encounter import ClinicalEncounterSchema
from .clinical_note import ClinicalNoteSchema
from .clinical_order import ClinicalOrderSchema
from .clinical_order_result import ClinicalOrderResultSchema
from .department import DepartmentCreateRequestSchema, DepartmentUpdateRequestSchema, DepartmentResponseSchema
from .department_membership import DepartmentMembershipSchema
from .diagnosis import DiagnosisSchema
from .file_attachment import FileAttachmentSchema
from .medication_dispensing import MedicationDispensingSchema
from .nursing_task import NursingTaskSchema
from .patient import PatientSchema
from .staff import StaffSchema

__all__ = [
    "StaffSchema",
    "DepartmentCreateRequestSchema",
    "DepartmentUpdateRequestSchema",
    "DepartmentResponseSchema",
    "DepartmentMembershipSchema",
    "PatientSchema",
    "ClinicalEncounterSchema",
    "DiagnosisSchema",
    "ClinicalNoteSchema",
    "ClinicalOrderSchema",
    "ClinicalOrderResultSchema",
    "FileAttachmentSchema",
    "MedicationDispensingSchema",
    "NursingTaskSchema",
    "LoginRequestSchema",
    "LoginResponseSchema"
]
