import pytest

from app.core.security import hash_password, verify_password


def test_password_hashing():
    password = "password01"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed_password=hashed)


def test_wrong_password():
    password = "password2"
    hashed = hash_password(password)

    assert verify_password("wrongpassword", hashed_password=hashed) is False
