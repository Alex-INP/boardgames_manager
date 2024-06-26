from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship, mapped_column, Mapped
from src.database import Base

from src.models import TimestampMixin


if TYPE_CHECKING:
    from src.auth.models import User


class Template(TimestampMixin, Base):
    __tablename__ = "templates"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()

    headers: Mapped[list["Header"]] = relationship(back_populates="template")
    filled_templates: Mapped[list["FilledTemplate"]] = relationship(
        back_populates="template"
    )


class Header(TimestampMixin, Base):
    __tablename__ = "headers"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str] = mapped_column()
    template_id: Mapped[str] = mapped_column(
        ForeignKey("templates.id", ondelete="CASCADE"), index=True
    )
    template: Mapped[Template] = relationship(back_populates="headers")


FilledTemplateUser = Table(
    "filledtemplates__users",
    Base.metadata,
    Column(
        "filled_template_id",
        ForeignKey("filled_templates.id", ondelete="CASCADE"),
        index=True,
    ),
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), index=True),
)


class FilledTemplate(TimestampMixin, Base):
    __tablename__ = "filled_templates"

    id: Mapped[int] = mapped_column(primary_key=True)
    creator_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), index=True
    )
    creator: Mapped["User"] = relationship(back_populates="filled_templates")
    template_id: Mapped[int] = mapped_column(
        ForeignKey("templates.id", ondelete="CASCADE"), index=True
    )
    template: Mapped[Template] = relationship(back_populates="filled_templates")

    players: Mapped[list["User"]] = relationship(secondary=FilledTemplateUser)
    results_for_headers: Mapped[list["ResultForHeader"]] = relationship(
        back_populates="filled_template"
    )


ResultForHeaderHeader = Table(
    "result_for_headers__headers",
    Base.metadata,
    Column(
        "result_for_header",
        ForeignKey("result_for_headers.id", ondelete="CASCADE"),
        index=True,
    ),
    Column("header", ForeignKey("headers.id", ondelete="CASCADE"), index=True),
)


class ResultForHeader(TimestampMixin, Base):
    __tablename__ = "result_for_headers"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[int] = mapped_column()
    filled_template_id: Mapped[int] = mapped_column(
        ForeignKey("filled_templates.id", ondelete="CASCADE"), index=True
    )
    filled_template: Mapped[FilledTemplate] = relationship(
        back_populates="results_for_headers"
    )
    player_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), index=True
    )
    player: Mapped["User"] = relationship(back_populates="results_for_headers")

    header: Mapped[Header] = relationship(secondary=ResultForHeaderHeader)
