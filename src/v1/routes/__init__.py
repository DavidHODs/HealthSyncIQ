from fastapi import APIRouter
from typing_extensions import Sequence, Tuple

from .app import AppRoute
from .auth import AuthRoute

app_routes: APIRouter = AppRoute().router
auth_routes: APIRouter = AuthRoute().router

all_routes: Sequence[Tuple[APIRouter, list[str]]] = [
    (app_routes, ["Health"]),
    (auth_routes, ["Auth"])
]

__all__ = ["all_routes"]
