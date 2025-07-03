from datetime import datetime

from typing_extensions import NotRequired, TypedDict


class JWTTokenPayload(TypedDict):
  id: str
  role: str
  exp: NotRequired[datetime]
  
class JWTAccessTokenPayload(TypedDict):
  id: str
  code: str
  exp: NotRequired[datetime]
  
class JWTAccessTokenPayloadResponse(TypedDict):
  token: str
  code: str
