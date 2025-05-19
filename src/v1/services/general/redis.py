import asyncio
import time
from typing import Optional
import redis
import redis.exceptions

from settings import Config

REDIS_CONNECT_RETRIES = 3
REDIS_CONNECT_DELAY_SECONDS = 1

_redis_service_instance: Optional["RedisService"] = None


class RedisService:
    def __init__(self) -> None:
        self.host = Config.REDIS_HOST
        self.port = Config.REDIS_PORT
        self.db = Config.REDIS_DB
        self.username = Config.REDIS_USERNAME
        self.password = Config.REDIS_PASSWORD

        self.expiry_days = Config.JWT_TOKEN_AND_REDIS_EXPIRY_DAYS
        self.seconds_in_a_day = Config.SECONDS_IN_A_DAY

        self._redis_client: Optional[redis.Redis] = None


    def connect_client(self) -> None:
        if self._redis_client is not None:
            return

        for attempt in range(REDIS_CONNECT_RETRIES):
            try:
                print(f"Connection attempt {attempt + 1}/{REDIS_CONNECT_RETRIES}...")
                client = redis.Redis(
                    host=self.host,
                    port=self.port,
                    db=self.db,
                    username=self.username,
                    password=self.password,
                    decode_responses=True
                )

                client.ping()
                self._redis_client = client
                print("Successfully Connected to Redis Database")
                break

            except redis.exceptions.ConnectionError as e:
                print(f"Redis connection attempt {attempt + 1} failed: {e}")
                if attempt < REDIS_CONNECT_RETRIES - 1:
                    time.sleep(REDIS_CONNECT_DELAY_SECONDS)
                else:
                    self._redis_client = None
                    print("Failed to connect to Redis after multiple attempts. Redis operations will be skipped.")

            except Exception as e:
                 print(f"An unexpected error occurred during Redis connection attempt {attempt + 1}: {e}")
                 self._redis_client = None


    def close_client(self) -> None:
        if self._redis_client is not None:
            try:
                self._redis_client.close()
                print("Redis client closed.")
            except Exception as e:
                print(f"Error closing Redis client: {e}")
            finally:
                self._redis_client = None


    def _get_client(self) -> Optional[redis.Redis]:
        if self._redis_client is None:
            return None
        return self._redis_client

    def set(self, key: str, value: str) -> None:
        expiry_seconds: int = self.expiry_days * self.seconds_in_a_day
        client: Optional[redis.Redis] = self._get_client()

        if client is None:
            return None

        try:
            client.set(key, value, ex=expiry_seconds)

        except Exception as exc:
            return None


    def get(self, key: str) -> Optional[str]:
        client = self._get_client()
        if client is None:
            return None

        try:
            result = client.get(key)
            if result is None:
                return None
            
            return str(result)

        except Exception as exc:
            return None


    def delete(self, key: str) -> None:
        client = self._get_client()
        if client is None:
            return None

        try:
            client.delete(key)
        except Exception as exc:
            return None


def redis_service() -> "RedisService":
    global _redis_service_instance
    if _redis_service_instance is None:
        _redis_service_instance = RedisService()
    return _redis_service_instance