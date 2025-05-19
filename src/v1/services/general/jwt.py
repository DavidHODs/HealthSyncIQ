import datetime
from typing import Any, Dict, cast
from uuid import UUID

import jwt
from typing_extensions import Optional

from settings import Config
from v1.errors import AppException
from v1.type_defs import ErrorTypeEnum, JWTTokenPayload

_jwt_service_instance: Optional["JWTService"] = None


class JWTService:
  def __init__(self) -> None:
    self.secret_key = Config.JWT_SECRET_KEY
    self.algorithm = Config.JWT_ALGORITHM
    self.expiry_days = Config.JWT_TOKEN_AND_REDIS_EXPIRY_DAYS
    self.seconds_in_a_day = Config.SECONDS_IN_A_DAY

  def create_token(self, id: UUID, role: str) -> str:
    try:
      payload = JWTTokenPayload(
          id=str(id),
          role=role,
          exp=datetime.datetime.now(
              datetime.timezone.utc) + datetime.timedelta(seconds=self.expiry_days * self.seconds_in_a_day)
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
  global _jwt_service_instance

  if _jwt_service_instance is None:
    _jwt_service_instance = JWTService()

  return _jwt_service_instance
