import datetime
import random
import string
from uuid import UUID

import jwt
from typing_extensions import Any, Dict, Optional, cast

from settings import Config
from v1.errors import AppException
from v1.type_defs import (
  ErrorTypeEnum,
  JWTAccessTokenPayload,
  JWTAccessTokenPayloadResponse,
  JWTTokenPayload,
)

_jwt_service_instance: Optional["JWTService"] = None


class JWTService:
  def __init__(self) -> None:
    self.secret_key = Config.JWT_SECRET_KEY
    self.algorithm = Config.JWT_ALGORITHM
    self.expiry_days = Config.JWT_TOKEN_AND_REDIS_EXPIRY_DAYS
    self.seconds_in_a_day = Config.SECONDS_IN_A_DAY

  def create_auth_token(self, id: UUID, role: str) -> str:
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

  def create_access_token(self, id: UUID) -> JWTAccessTokenPayloadResponse:
    try:
      code = self._generate_access_code_()

      payload = JWTAccessTokenPayload(
          id=str(id),
          code=code,
          exp=datetime.datetime.now(
              datetime.timezone.utc) + datetime.timedelta(minutes=10)
      )

      encoded_jwt = jwt.encode(
          cast(Dict[str, Any], payload),
          self.secret_key,
          algorithm=self.algorithm
      )

      token = encoded_jwt if isinstance(
          encoded_jwt, str) else encoded_jwt.decode("utf-8")

      return JWTAccessTokenPayloadResponse(
          code=code,
          token=token
      )

    except Exception as exc:
      raise AppException.classify_error(error=exc)

  def decode_auth_token(self, token: str) -> JWTTokenPayload:
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

  def decode_access_token(self, token: str) -> JWTAccessTokenPayload:
    try:
      payload = jwt.decode(
          token,
          self.secret_key,
          algorithms=[self.algorithm]
      )

      return cast(JWTAccessTokenPayload, payload)

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

  def _generate_access_code_(self, length: int = 8) -> str:
    symbols = "!@#$%&*"

    required = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice(symbols)
    ]

    safe_chars = (
        string.ascii_uppercase +
        string.ascii_lowercase +
        string.digits +
        symbols
    )

    remaining = random.choices(safe_chars, k=length - len(required))
    all_chars = required + remaining
    random.shuffle(all_chars)
    return ''.join(all_chars)


def jwt_service_instance() -> JWTService:
  global _jwt_service_instance

  if _jwt_service_instance is None:
    _jwt_service_instance = JWTService()

  return _jwt_service_instance
