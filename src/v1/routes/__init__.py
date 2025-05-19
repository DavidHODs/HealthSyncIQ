from fastapi import APIRouter
from typing_extensions import Sequence, Tuple

from .app import AppRoute
from .auth import AuthRoute
from .department import DepartmentRoute

app_routes: APIRouter = AppRoute().router
auth_routes: APIRouter = AuthRoute().router
department_routes: APIRouter = DepartmentRoute().router

all_routes: Sequence[Tuple[APIRouter, list[str]]] = [
    (app_routes, ["Health"]),
    (auth_routes, ["Auth"]),
    (department_routes, ["Department"])
]

__all__ = ["all_routes"]
