from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.dependencies import get_session
from src.utils import get_now_utc

from . import models
from .config import settings
from .dependencies import auth_only, check_not_exists
from .schemas import TokenPayload, TokenResponse, UserCreate
from .utils import authenticate, create_token

router = APIRouter()


# @router.get("/create_db_data")
# async def cr_user(db: Annotated[Session, Depends(get_session)]):
#     user = models.User(
#         email="alex@mail.ru",
#         username="alex",
#         password="$2b$12$Ytvun5JZQKWmdo/A1DhZ6eVIw/KKq9ZAIkPpoqDsKdFmK7rnnbTZu",  # qwerty
#         role_id=1,
#     )
#
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#
#     token = models.Token(
#         user_id=user.id,
#         value="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbGV4IiwiZXhwIjoxNzE5MjI2OTM0fQ.rDj3iU0CzfUXxegqPTrIS-dK1wMcIL9sdbns-Ue2F3E",
#     )
#     db.add(token)
#     db.commit()
#     db.refresh(token)
#     return "OK"


@router.post("/register_user")
async def register_user(
    db: Annotated[Session, Depends(get_session)],
    form_data: Annotated[UserCreate, Depends(check_not_exists)],
):
    role_id = db.scalar(
        select(models.UserRole.id).filter(models.UserRole.name == "User")
    )
    user = models.User(role_id=role_id, **form_data.model_dump())
    db.add(user)
    db.commit()
    return "Created"


@router.get("/need_auth", dependencies=[Depends(auth_only)])
def need_auth_route():
    return "OK"


# ToDo должно работать с нескольких устройств
@router.post("/token", response_model=TokenResponse)
async def token(
    db: Annotated[Session, Depends(get_session)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> TokenResponse:
    user = authenticate(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    expire_delta = timedelta(minutes=settings.token_expire_minutes)
    expire_time = get_now_utc() + expire_delta

    payload = TokenPayload(name=user.username, exp=expire_time)
    access_token = create_token(payload=payload.model_dump())

    models.Token.insert_or_update(db, user.id, access_token, expire_time)

    return TokenResponse(access_token=access_token)


@router.get("/session_expired")
def session_expired():
    return "some session expired html"
