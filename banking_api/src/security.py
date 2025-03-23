from datetime import datetime, timedelta
from os import getenv
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = getenv("SECRET_KEY", "dummy_secret_key")
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def hash_password(password: str) -> str:
    """
    Function to hash a password using bcrypt.

    :param password: str: The password to hash.
    :return: str: The hashed password.
    """

    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Function to verify a password against a hashed password.

    :param plain_password: str: The plain text password.
    :param hashed_password: str: The hashed password.
    :return: bool: True if the password matches, False otherwise
    """

    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Function to create an access token using JWT.

    :param data: dict: The data to encode in the token.
    :param expires_delta: Optional[timedelta]: The expiry time for the token.
    :return: str: The access token.
    """

    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(weeks=100))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Function to get the current user from the access token.
    It also verifies the token.

    :param token: str: The access token.
    :return: str: The username of the current user.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )
        return username
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
