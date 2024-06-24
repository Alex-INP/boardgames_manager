from datetime import datetime

from pydantic import BaseModel, EmailStr, SecretStr


class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr


class User(UserCreate):
    id: int
    password: SecretStr
    is_active: bool
    role_id: int

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class Token(BaseModel):
    id: int
    value: str
    user_id: int
    expires: datetime
