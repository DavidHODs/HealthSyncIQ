import secrets
import string

from cryptography.fernet import Fernet
from typing_extensions import Optional, overload

from settings import Config


class EncryptionService:
  def __init__(self) -> None:
    self.fernet = Fernet(Config.ENCRYPTION_KEY.encode())

  @overload
  def encrypt(self, value: None) -> None: ...

  @overload
  def encrypt(self, value: str) -> str: ...

  def encrypt(self, value: str | None) -> Optional[str]:
    if not value:
      return None
    return self.fernet.encrypt(value.encode()).decode()

  @overload
  def decrypt(self, encrypted_value: None) -> None: ...

  @overload
  def decrypt(self, encrypted_value: str) -> str: ...

  def decrypt(self, encrypted_value: str | None) -> Optional[str]:
    if not encrypted_value:
      return None
    return self.fernet.decrypt(encrypted_value.encode()).decode()

  def generate_registration_code(self) -> str:
    alphabet = string.ascii_uppercase + string.digits
    registration_code = "".join(secrets.choice(alphabet) for _ in range(6))
    return f"HS-{registration_code}"
