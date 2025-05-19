from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Security
from fastapi.security import HTTPBearer
from psycopg import OperationalError
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing_extensions import AsyncGenerator

from database import get_db
from settings import INIT_START_TIME, Config
from v1.routes import all_routes
from v1.services.general.redis import RedisService, redis_service_instance
from v1.type_defs import UvicornKwargs

load_dotenv(dotenv_path=".env")
INIT_START_TIME

redis_service: RedisService = redis_service_instance()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
  print("Starting up application...")

  try:
    db = next(get_db())
    db.connection().execute(text("SELECT 1"))
    print("Database connection successful")
  except (OperationalError, SQLAlchemyError) as exc:
    print(f"Database connection failed: {exc}")
    exit(1)
  finally:
    if 'db' in locals() and db:
      db.close()

  redis_service.connect_client()

  yield

  print("Shutting down application...")

  redis_service.close_client()


security_scheme = HTTPBearer(
    scheme_name="Authorization",
    description="JWT Token (Bearer format)",
    bearerFormat="JWT"
)

app: FastAPI = FastAPI(
    lifespan=lifespan,
    title="HealthSyncIQ API",
    security=[Security(security_scheme)],
    version="1.0.0")

for router, tags in all_routes:
  app.include_router(router, prefix="/api/v1", tags=list(tags))

if __name__ == "__main__":
  uvicorn_kwargs: UvicornKwargs = {
      "host": Config.HOST,
      "port": Config.PORT,
      "reload": Config.isDev
  }

  print(f"app running at {Config.HOST}:{Config.PORT}")
  uvicorn.run("src.main:app", **uvicorn_kwargs)
