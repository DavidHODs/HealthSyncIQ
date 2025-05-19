from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from typing_extensions import List

from database.setup import get_db
from v1.models import StaffModel
from v1.services import jwt_service_instance, redis_service_instance
from v1.type_defs import JWTTokenPayload, StaffRole


class Authenticate:
  def __init__(self, roles: List[StaffRole]):
    self.roles = roles

  def __call__(
      self,
      credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
      db: Session = Depends(get_db)
  ) -> JWTTokenPayload:
    token = credentials.credentials
    redis_service = redis_service_instance()
    jwt_service = jwt_service_instance()

    try:
      payload: JWTTokenPayload = jwt_service.decode_token(token)

      if payload.get("role") not in {role.value for role in self.roles}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permission for this operation"
        )

      if not redis_service.get(token):
        staff = db.query(StaffModel).filter(
            StaffModel.id == payload.get("id"),
            StaffModel.deleted_at.is_(None),
            StaffModel.is_active == True
        ).first()

        if not staff:
          raise HTTPException(
              status_code=status.HTTP_401_UNAUTHORIZED,
              detail="Invalid authentication credentials"
          )

        new_token = jwt_service.create_token(id=staff.id, role=staff.role)
        redis_auth_key = f"auth:{staff.id}"
        redis_service.set(redis_auth_key, new_token)

      return JWTTokenPayload(id=str(payload.get("id")),
                             role=str(payload.get("role")))

    except HTTPException:
      raise
    except Exception:
      raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Could not validate credentials",
          headers={"WWW-Authenticate": "Bearer"}
      )
