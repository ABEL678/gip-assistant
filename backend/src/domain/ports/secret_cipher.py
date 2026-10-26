"""Порт шифрования секретов (6.14a)."""

from abc import ABC, abstractmethod


class SecretCipherPort(ABC):
    """Симметричное шифрование секретов (Fernet)."""

    @abstractmethod
    def is_configured(self) -> bool:
        """Настроен ли ключ шифрования."""

    @abstractmethod
    def encrypt(self, plaintext: str) -> bytes:
        """Зашифровать строку. Результат — ciphertext для БД."""

    @abstractmethod
    def decrypt(self, token: bytes) -> str:
        """Расшифровать ciphertext. Plaintext — только в памяти."""
