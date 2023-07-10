from uuid import UUID
from hashlib import scrypt
from datetime import datetime, timedelta
import os
import base64
import hmac

import sqlalchemy as sa
from sqlalchemy.engine import Connection
from fastapi.encoders import jsonable_encoder
import sendgrid
import jwt

from .schemas import ResetToken
from .models import reset_token
from ..users.models import user_table
from ..users.schemas import User
from config import settings
from .exceptions import InvalidToken, ExpiredToken, InvalidCredentials


def create_reset_token(
    conn: Connection,
    user_id: UUID,
    expiration_date: datetime = datetime.utcnow() + timedelta(hours=3),
) -> ResetToken:
    """
    Generate a reset token for the given user and return the plain token
    """
    key = os.urandom(32)
    hash = scrypt(
        key,
        salt=settings.reset_token_key.encode("utf-8"),
        n=2**14,
        r=8,
        p=1,
        dklen=32,
    )
    token = base64.urlsafe_b64encode(key).decode("utf-8")

    stmt = sa.insert(reset_token).values(
        user_id=user_id,
        hash=hash,
        expires_at=expiration_date,
    )
    conn.execute(stmt)

    return ResetToken(token=token, expires_at=expiration_date)


def verify_reset_token(conn: Connection, token: str) -> UUID:
    """
    Verify the given token and return the user_id if the token is valid.
    """

    hash = scrypt(
        base64.urlsafe_b64decode(token),
        salt="test".encode("utf-8"),
        n=2**14,
        r=8,
        p=1,
        dklen=32,
    )

    stmt = sa.select(reset_token).where(reset_token.c.hash == hash)
    result = conn.execute(stmt).fetchone()

    if result is None:
        raise InvalidToken
    elif result.expires_at < datetime.now():
        raise ExpiredToken

    return result.user_id


def create_password_hash(password: str) -> tuple[bytes, bytes]:
    """
    Create an hash from the given password.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The hashed password.
        bytes: The salt used to hash the password.
    """

    salt = os.urandom(32)
    hash = scrypt(password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1, dklen=32)
    return hash, salt


def reset_password(conn: Connection, user_id: UUID, password: str) -> None:
    """
    Reset the password of the user with the given id.

    Args:
        user_id (UUID): The id of the user to reset the password.
        password (str): The new password.
    """
    hash, salt = create_password_hash(password)
    stmt = (
        sa.update(user_table)
        .where(user_table.c.id == user_id)
        .values(
            password_hash=hash,
            salt=salt,
        )
        .returning(user_table.c.id)
    )
    conn.execute(stmt)


def verify_password(hash: bytes, salt: bytes, password: str) -> bool:
    """
    Verify that the given password match the given hash.

    Args:
        hash (bytes): The hash of the password.
        salt (bytes): The salt used to hash the password.
        password (str): The password to verify.

    Returns:
        bool: True if the password match the hash, False otherwise.
    """
    new_hash = scrypt(
        password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1, dklen=32
    )
    return hmac.compare_digest(hash, new_hash)


def get_user_password_hash(conn: Connection, email: str) -> tuple[bytes, bytes]:
    """
    Get the password hash and salt for the user with the given id.

    Args:
        email (str): The email of the user to get the password hash.

    Returns:
        tuple[bytes, bytes]: The password hash and salt.
    """
    stmt = sa.select(user_table).where(user_table.c.email == email)
    result = conn.execute(stmt).fetchone()

    if result is None:
        raise InvalidCredentials

    return result.password_hash, result.salt


def generate_jwt_token(user: User) -> str:
    """
    Generate a JWT token for the given user.

    Args:
        user (User): The user to generate the token for.

    Returns:
        str: The generated JWT token.
    """
    return jwt.encode(
        {
            **jsonable_encoder(user),
            # Add expiration date
        },
        settings.jwt_private_key,
        algorithm="HS256",
    )


def verify_jwt_token(token: str) -> User:
    try:
        return User(**jwt.decode(token, settings.jwt_private_key, algorithms=["HS256"]))
    except jwt.exceptions.InvalidSignatureError:
        raise InvalidToken


def send_reset_password_email(email: str, token: ResetToken) -> None:
    """
    Send a reset password email to the given email address.

    Args:
        email (str): The email address to send the email to.
        token (ResetToken): The reset token to include in the email.
    """
    return
    sg = sendgrid.SendGridAPIClient(api_key=settings.sendgrid_api_key)
