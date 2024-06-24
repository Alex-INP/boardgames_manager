from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column, Session

from src.models import TimestampMixin
from src.database import Base
from src.points_tables.models import FilledTemplate, ResultForHeader


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("user_roles.id"))

    filled_templates: Mapped[list[FilledTemplate]] = relationship(
        back_populates="creator"
    )
    results_for_headers: Mapped[list[ResultForHeader]] = relationship(
        back_populates="player"
    )
    token: Mapped["Token"] = relationship(back_populates="user")

    @classmethod
    def get_by_username(cls, db: Session, username: str):
        return db.query(cls).filter(cls.username == username).first()


class UserRole(TimestampMixin, Base):
    __tablename__ = "user_roles"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column()


class Token(TimestampMixin, Base):
    __tablename__ = "access_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str | None] = mapped_column()
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True
    )
    user: Mapped[User] = relationship(back_populates="token")
    expires: Mapped[datetime | None] = mapped_column()

    @classmethod
    def insert_or_update(cls, db: Session, user_id: int, value: str, expires):
        token = db.query(cls).filter_by(user_id=user_id).first()
        if token:
            token.value = value
            token.expires = expires
        else:
            token = cls(value=value, user_id=user_id, expires=expires)
            db.add(token)
        db.commit()
