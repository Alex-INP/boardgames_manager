from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy import exists
from sqlalchemy.orm import Session

from .config import settings
from .exceptions import (
    UnauthorizedException,
    RegistrationException,
    SessionExpiredException,
)
from .schemas import User, UserCreate
from .utils import get_hashed_value, is_token_expired
from src.dependencies import get_session

from src.auth import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token", auto_error=False)


async def get_current_user(
    db: Annotated[Session, Depends(get_session)],
    token: Annotated[str, Depends(oauth2_scheme)],
):
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.token_hash_alg]
        )
        payload_username: str = payload.get("sub")
        if payload_username is None:
            raise UnauthorizedException()
    except InvalidTokenError:
        raise SessionExpiredException()

    user = models.User.get_by_username(db, payload_username)
    if user is None:
        raise UnauthorizedException()
    return user


async def get_active_user(user: Annotated[User, Depends(get_current_user)]):
    if not user.is_active:
        raise HTTPException(status_code=400, detail="User is not active")
    return user


async def check_not_exists(
    db: Annotated[Session, Depends(get_session)],
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    email: Annotated[str, Form()],
):
    hashed_password = get_hashed_value(password)
    form_data = UserCreate(username=username, password=hashed_password, email=email)

    username_exists = db.query(
        exists().where(models.User.username == form_data.username)
    ).scalar()
    if username_exists:
        raise RegistrationException(f"User {form_data.username} already exists")

    email_exists = db.query(
        exists().where(models.User.email == form_data.email)
    ).scalar()
    if email_exists:
        raise RegistrationException(f"Email {form_data.email} already in use")

    return form_data


async def authenticated_only(
    db: Annotated[Session, Depends(get_session)],
    token: Annotated[str, Depends(oauth2_scheme)],
):
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.token_hash_alg]
        )
        payload_username: str = payload.get("sub")
        if payload_username is None:
            raise UnauthorizedException()
    except InvalidTokenError:
        raise UnauthorizedException()

    user_id = (
        db.query(models.User.id)
        .filter(models.User.username == payload_username)
        .scalar_subquery()
    )
    token = db.query(models.Token).filter_by(value=token, user_id=user_id).first()
    if not token:
        raise UnauthorizedException()

    if is_token_expired(token.expires):
        raise SessionExpiredException()
