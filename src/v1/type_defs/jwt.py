from datetime import datetime

from typing_extensions import NotRequired, TypedDict


class JWTTokenPayload(TypedDict):
  id: str
  role: str
  exp: NotRequired[datetime]
