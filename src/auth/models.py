from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship

from src.database import Base
from src.models import TimestampMixin
from src.points_tables.models import FilledTemplate, ResultForHeader


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)
    role_id: Mapped[int] = mapped_column(
        ForeignKey("user_roles.id", ondelete="SET NULL"), index=True
    )
    role: Mapped["UserRole"] = relationship(backref="users")

    filled_templates: Mapped[list[FilledTemplate]] = relationship(
        back_populates="creator"
    )
    results_for_headers: Mapped[list[ResultForHeader]] = relationship(
        back_populates="player"
    )
    token: Mapped["Token"] = relationship(back_populates="user")


class UserRole(TimestampMixin, Base):
    __tablename__ = "user_roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)


class Token(TimestampMixin, Base):
    __tablename__ = "access_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str] = mapped_column()
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True
    )
    user: Mapped[User] = relationship(back_populates="token")
    expires: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    @classmethod
    def insert_or_update(cls, db: Session, user_id: int, value: str, expires: datetime):
        token = db.query(cls).filter_by(user_id=user_id).first()
        if token:
            token.value = value
            token.expires = expires
        else:
            token = cls(value=value, user_id=user_id, expires=expires)
            db.add(token)
        db.commit()
