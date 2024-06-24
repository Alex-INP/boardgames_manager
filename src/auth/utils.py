from datetime import datetime

import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.auth import models
from src.auth.config import settings


context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authenticate(db: Session, username: str, password: str) -> models.User | None:
    user = db.query(models.User).filter(models.User.username == username).first()
    if user and verify_password(password, user.password):
        return user
    return None


def verify_password(plain_pwd, hashed_pwd):
    return context.verify(plain_pwd, hashed_pwd)


def get_hashed_value(value):
    return context.hash(value)


def create_token(payload: dict) -> str:
    encoded_jwt = jwt.encode(payload, settings.secret_key, settings.token_hash_alg)
    return encoded_jwt


def is_token_expired(token_expires_datetime: datetime | None) -> bool:
    if token_expires_datetime:
        return token_expires_datetime < datetime.now()
    return False
