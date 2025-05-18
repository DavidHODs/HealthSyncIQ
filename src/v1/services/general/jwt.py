import datetime
from typing import Any, Dict, cast
from uuid import UUID

import jwt

from settings import Config
from v1.errors import AppException
from v1.type_defs import ErrorTypeEnum, JWTTokenPayload


class JWTService:
  def __init__(self) -> None:
    self.secret_key = Config.JWT_SECRET_KEY
    self.algorithm = Config.JWT_ALGORITHM
    self.expiry_minutes = Config.JWT_EXPIRY_MINUTES

  def create_token(
      self, id: UUID, title: str, surname: str, role: str
  ) -> str:
    try:
      payload = JWTTokenPayload(
          id=str(id),
          title=title,
          surname=surname,
          role=role,
          exp=datetime.datetime.now(
              datetime.timezone.utc) + datetime.timedelta(minutes=self.expiry_minutes)
      )

      encoded_jwt = jwt.encode(
          cast(Dict[str, Any], payload),
          self.secret_key,
          algorithm=self.algorithm
      )
      return encoded_jwt if isinstance(
          encoded_jwt, str) else encoded_jwt.decode("utf-8")

    except Exception as exc:
      raise AppException.classify_error(error=exc)

  def decode_token(self, token: str) -> JWTTokenPayload:
    try:
      payload = jwt.decode(
          token,
          self.secret_key,
          algorithms=[self.algorithm]
      )

      return cast(JWTTokenPayload, payload)

    except jwt.ExpiredSignatureError:
      raise AppException(
          type=ErrorTypeEnum.INTERNAL_SERVER_ERROR,
          detail="Expired Token"
      )

    except jwt.InvalidTokenError:
      raise AppException(
          type=ErrorTypeEnum.INTERNAL_SERVER_ERROR,
          detail="Invalid Token"
      )

    except Exception as exc:
      raise AppException.classify_error(error=exc)


def jwt_service() -> JWTService:
  return JWTService()
