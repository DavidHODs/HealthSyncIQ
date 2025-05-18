import os

from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")


class Config:
  PORT: int = int(os.getenv("PORT", 9000))
  HOST: str = os.getenv("HOST", "localhost")
  ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
  isDev: bool = ENVIRONMENT == "development"
  isProd: bool = ENVIRONMENT == "production"

  DB_PORT: int = int(os.getenv("DB_PORT", 5432))
  DB_DATABASE: str = os.getenv("DB_DATABASE", "")
  DB_USER: str = os.getenv("DB_USER", "")
  DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
  DB_HOST: str = os.getenv("DB_HOST", "localhost")

  JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "")
  JWT_EXPIRY_MINUTES: int = int(os.getenv("JWT_EXPIRY_MINUTES", 10080))
  JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
