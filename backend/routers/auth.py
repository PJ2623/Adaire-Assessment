from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from security.helpers import authenticate_user, create_access_token
from security.schema import Token

from typing import Annotated


router = APIRouter(
    tags=["Auth"]
)


@router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """
    Login and get access token.
    ## Sample response:
    ```json
    {
        "access_token": "your_access_token",
        "token_type": "bearer"
    }
    """
    user = await authenticate_user(form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=15)
    access_token = create_access_token(
        data={"sub": user.Email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
