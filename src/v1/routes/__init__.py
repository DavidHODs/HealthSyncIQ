from fastapi import APIRouter
from typing_extensions import List, Sequence, Tuple

from .app import AppRoute
from .auth import AuthRoute
from .department import DepartmentRoute
from .staff import StaffRoute

app_routes: APIRouter = AppRoute().router
auth_routes: APIRouter = AuthRoute().router
department_routes: APIRouter = DepartmentRoute().router
staff_routes: APIRouter = StaffRoute().router

all_routes: Sequence[Tuple[APIRouter, List[str]]] = [
    (app_routes, ["Health"]),
    (auth_routes, ["Auth"]),
    (department_routes, ["Department"]),
    (staff_routes, ["Staff"]),
]

__all__ = ["all_routes"]
