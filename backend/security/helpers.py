import jwt

from datetime import datetime, timedelta, timezone

from sqlalchemy import select

from database.db import AsyncSessionLocal

from fastapi import Depends, HTTPException, status, Security
from fastapi.security import (
    OAuth2PasswordBearer,
)

from database.models import Employee

from passlib.context import CryptContext

from typing import Annotated

from .schema import TokenData


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login",
)


async def get_user(username: str) -> Employee | None:

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Employee).where(Employee.Email == username)
        )

        user_in_db = result.scalar_one_or_none()

    if user_in_db is None:
        return

    return user_in_db


async def authenticate_user(username: str):
    user = await get_user(username)

    if not user:
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, key="EB9A1A5DF8558D32155C5E52B2E1A", algorithm="HS256"
    )
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, key="EB9A1A5DF8558D32155C5E52B2E1A", algorithms="HS256"
        )
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except Exception as e:
        raise credentials_exception

    user = await get_user(username=token_data.username)

    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: Annotated[Employee, Security(get_current_user)],
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No account found"
        )
    return current_user
