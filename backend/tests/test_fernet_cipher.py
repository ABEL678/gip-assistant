"""Тесты FernetCipher (6.14a)."""

import pytest
from cryptography.fernet import Fernet, InvalidToken

from backend.src.adapters.security.fernet_cipher import FernetCipher

KEY = Fernet.generate_key().decode()
OTHER_KEY = Fernet.generate_key().decode()


def test_is_configured_with_valid_key():
    """Валидный ключ → is_configured() True."""
    cipher = FernetCipher(KEY)

    assert cipher.is_configured() is True


def test_encrypt_decrypt_roundtrip():
    """encrypt → decrypt возвращает исходный текст."""
    cipher = FernetCipher(KEY)
    plaintext = "secret-api-key-1234"

    token = cipher.encrypt(plaintext)

    assert isinstance(token, bytes)
    assert cipher.decrypt(token) == plaintext


def test_two_encryptions_differ():
    """Два шифрования одного текста дают разные токены (Fernet IV)."""
    cipher = FernetCipher(KEY)

    assert cipher.encrypt("same-text") != cipher.encrypt("same-text")


def test_decrypt_with_other_key_fails():
    """Расшифровка чужим ключом → InvalidToken."""
    token = FernetCipher(KEY).encrypt("secret")

    with pytest.raises(InvalidToken):
        FernetCipher(OTHER_KEY).decrypt(token)


def test_empty_key_encrypt_raises():
    """Пустой ключ: is_configured False, encrypt → ValueError."""
    cipher = FernetCipher("")

    assert cipher.is_configured() is False
    with pytest.raises(ValueError, match="LLM_ENCRYPTION_KEY"):
        cipher.encrypt("secret")


def test_empty_key_decrypt_raises():
    """Пустой ключ: decrypt → ValueError."""
    cipher = FernetCipher("")

    with pytest.raises(ValueError, match="LLM_ENCRYPTION_KEY"):
        cipher.decrypt(b"token")


def test_invalid_key_raises_on_init():
    """Невалидный непустой ключ → ValueError при создании."""
    with pytest.raises(ValueError):
        FernetCipher("not-a-valid-fernet-key")
