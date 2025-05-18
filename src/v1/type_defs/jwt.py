from datetime import datetime
from typing import TypedDict


class JWTTokenPayload(TypedDict):
  id: str
  title: str
  surname: str
  role: str
  exp: datetime
