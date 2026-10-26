"""Fernet-реализация SecretCipherPort (6.14a)."""

from cryptography.fernet import Fernet

from backend.src.domain.ports.secret_cipher import SecretCipherPort


class FernetCipher(SecretCipherPort):
    """Симметричное шифрование ключей LLM (Fernet)."""

    def __init__(self, key: str) -> None:
        self._fernet: Fernet | None = None
        if key:
            # Невалидный непустой ключ → ValueError от Fernet.
            self._fernet = Fernet(key.encode())

    def is_configured(self) -> bool:
        """Настроен ли ключ шифрования."""
        return self._fernet is not None

    def encrypt(self, plaintext: str) -> bytes:
        """Зашифровать строку."""
        return self._require_fernet().encrypt(plaintext.encode())

    def decrypt(self, token: bytes) -> str:
        """Расшифровать ciphertext."""
        return self._require_fernet().decrypt(token).decode()

    def _require_fernet(self) -> Fernet:
        if self._fernet is None:
            raise ValueError("LLM_ENCRYPTION_KEY не задан")
        return self._fernet
