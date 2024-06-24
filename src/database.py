from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from .config import settings


engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
    echo=settings.echo_queries,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# for sqlLite
session = SessionLocal()
session.execute(text("pragma foreign_keys=on"))
session.close()


class Base(DeclarativeBase):
    pass
