import string
import secrets
from cryptography.fernet import Fernet

from settings import Config


class EncryptionService:
    def __init__(self) -> None:
        self.fernet = Fernet(Config.ENCRYPTION_KEY.encode())
    
    def encrypt(self, value: str | None) -> str | None:
        if not value:
            return None
        return self.fernet.encrypt(value.encode()).decode()

    def decrypt(self, encrypted_value: str | None) -> str | None:
        if not encrypted_value:
            return None
        return self.fernet.decrypt(encrypted_value.encode()).decode()
    
    def generate_registration_code(self) -> str:
        alphabet = string.ascii_uppercase + string.digits
        registration_code = "".join(secrets.choice(alphabet) for _ in range(6))
        return f"HS-{registration_code}"