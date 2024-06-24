from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    created: Mapped[datetime] = mapped_column(default=func.now())
    updated: Mapped[datetime | None] = mapped_column(
        onupdate=func.now(), default=func.now()
    )
