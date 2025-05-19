from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from typing_extensions import List

from v1.errors import AppException
from v1.models import StaffModel
from v1.services import JWTService, RedisService, jwt_service, redis_service
from v1.type_defs import ErrorTypeEnum, JWTTokenPayload

async def authentication(
    roles: List[str],
    db: Session,
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
) -> JWTTokenPayload:
  token = credentials.credentials
  redis_service: RedisService = redis_service()
  jwt_service: JWTService = jwt_service()

  try:
    payload: JWTTokenPayload = jwt_service.decode_token(token)
    if payload.get("role") not in roles:
      raise AppException(
          type=ErrorTypeEnum.UNAUTHORIZED
      )

    valid_token = redis_service.get(token)
    if valid_token:
      return payload

    staff = db.query(StaffModel).filter(
        StaffModel.id == payload.get("id"),
        StaffModel.deleted_at.is_(None),
        StaffModel.is_active == True
    ).first()

    if not staff:
      raise AppException(
          type=ErrorTypeEnum.UNAUTHORIZED
      )

    jwt_token: str = jwt_service.create_token(
        id=staff.id,
        role=staff.role
    )

    redis_auth_key = f"auth:{staff.id}"
    redis_service.set(redis_auth_key, jwt_token)

    return JWTTokenPayload(
        id=str(staff.id),
        role=staff.role
    )

  except Exception:
    raise AppException(type=ErrorTypeEnum.INTERNAL_SERVER_ERROR)
