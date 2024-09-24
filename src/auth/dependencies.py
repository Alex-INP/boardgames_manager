from typing import Annotated

from fastapi import Depends, Form, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import ExpiredSignatureError, InvalidTokenError
from pydantic import ValidationError
from sqlalchemy import exists, select, union_all
from sqlalchemy.orm import Session

from src.auth import models
from src.dependencies import get_session

from .exceptions import (
    RegistrationException,
    SessionExpiredException,
    UnauthorizedException,
)
from .schemas import UserCreate
from .utils import get_hashed_value, get_token_payload, is_token_expired


async def prepare_user_create_data(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    email: Annotated[str, Form()],
):
    hashed_password = get_hashed_value(password)
    form_data = UserCreate(username=username, password=hashed_password, email=email)
    return form_data


async def check_not_exists(
    db: Annotated[Session, Depends(get_session)],
    form_data: Annotated[UserCreate, Depends(prepare_user_create_data)],
):
    res = (
        db.execute(
            union_all(
                select(exists().where(models.User.username == form_data.username)),
                select(exists().where(models.User.email == form_data.email)),
            )
        )
        .scalars()
        .all()
    )

    username_exists = res[0]
    email_exists = res[1]
    error = None
    if username_exists:
        error = f"Username {form_data.username} already in use."

    if email_exists:
        email_err_msg = f"Email {form_data.email} already in use."
        error = f"{error} {email_err_msg}" if error else email_err_msg

    if error:
        raise RegistrationException(error)

    return form_data


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token", auto_error=False)


async def auth_only(
    db: Annotated[Session, Depends(get_session)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> models.User:
    try:
        payload = get_token_payload(token)
    except (ValidationError, InvalidTokenError, ExpiredSignatureError):
        raise UnauthorizedException()

    res = (
        db.query(models.Token, models.User)
        .filter_by(value=token)
        .join(models.User)
        .filter_by(username=payload.sub)
        .first()
    )

    if not res:
        raise UnauthorizedException()

    token, user = res[0], res[1]

    if is_token_expired(token.expires):
        raise SessionExpiredException()

    return user


async def auth_and_active_only(
    user: Annotated[models.User, Depends(auth_only)],
) -> models.User:
    if not user.is_active:
        raise HTTPException(status_code=400, detail="User is not active")
    return user
