import os
from typing_extensions import List, cast
from dotenv import load_dotenv
from v1.errors import AppException
from v1.type_defs import ErrorTypeEnum

load_dotenv(dotenv_path=".env", override=True, verbose=True)

class Config:
    PORT: int = int(cast(str, os.getenv("PORT")))
    HOST: str = cast(str, os.getenv("HOST"))
    ENVIRONMENT: str = cast(str, os.getenv("ENVIRONMENT"))
    isDev: bool = ENVIRONMENT == "development"
    isProd: bool = ENVIRONMENT == "production"

    DB_PORT: int = int(cast(str, os.getenv("DB_PORT")))
    DB_DATABASE: str = cast(str, os.getenv("DB_DATABASE"))
    DB_USER: str = cast(str, os.getenv("DB_USER"))
    DB_PASSWORD: str = cast(str, os.getenv("DB_PASSWORD"))
    DB_HOST: str = os.getenv("DB_HOST", "localhost")

    JWT_SECRET_KEY: str = cast(str, os.getenv("JWT_SECRET_KEY"))
    JWT_ALGORITHM: str = cast(str, os.getenv("JWT_ALGORITHM"))

    REDIS_HOST: str = cast(str, os.getenv("REDIS_HOST"))
    REDIS_PORT: int = int(cast(str, os.getenv("REDIS_PORT")))
    REDIS_DB: int = int(cast(str, os.getenv("REDIS_DB")))
    REDIS_USERNAME: str = cast(str, os.getenv("REDIS_USERNAME"))
    REDIS_PASSWORD: str = cast(str, os.getenv("REDIS_PASSWORD"))

    JWT_TOKEN_AND_REDIS_EXPIRY_DAYS: int = int(
        cast(str, os.getenv("JWT_TOKEN_AND_REDIS_EXPIRY_DAYS")))
    SECONDS_IN_A_DAY: int = 86400

    ENCRYPTION_KEY: str = cast(str, os.getenv("ENCRYPTION_KEY"))

    REQUIRED_VARIABLES = [
        "PORT",
        "HOST",
        "ENVIRONMENT",
        "DB_PORT",
        "DB_HOST",
        "DB_DATABASE",
        "DB_USER", 
        "DB_PASSWORD",
        "JWT_SECRET_KEY",
        "JWT_ALGORITHM",
        "REDIS_HOST",
        "REDIS_PORT",
        "REDIS_DB",
        "REDIS_USERNAME",
        "REDIS_PASSWORD",
        "JWT_TOKEN_AND_REDIS_EXPIRY_DAYS",
        "ENCRYPTION_KEY"
    ]

    @staticmethod
    def validate_required_environment_variables() -> None:
        missing_variables: List[str] = []
        
        for variable in Config.REQUIRED_VARIABLES:
            variable_value = os.getenv(variable)
            if not variable_value or variable_value.strip() == "":
                missing_variables.append(variable)

        if len(missing_variables) > 0:
            raise AppException(
                type=ErrorTypeEnum.INTERNAL_SERVER_ERROR,
                detail=f"Missing required environment variables: {', '.join(missing_variables)}"
            )