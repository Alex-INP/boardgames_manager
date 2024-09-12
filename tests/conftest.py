import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import alembic
from alembic.config import Config
from src.database import Base
from src.dependencies import get_session
from src.main import app as main_app

from .config import settings

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
    echo=settings.echo_queries,
)
session_factory = sessionmaker(autoflush=True, bind=engine)
scoped_session_factory = scoped_session(session_factory)


@pytest.fixture(scope="session")
def prepare_database():
    run_migrations()
    yield
    Base.metadata.reflect(bind=engine)
    Base.metadata.drop_all(bind=engine)


def run_migrations():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.database_url)
    alembic.command.upgrade(alembic_cfg, "head")


@pytest.fixture
def client():
    def get_session_override():
        session = session_factory()
        try:
            yield session
        finally:
            session.close()

    main_app.dependency_overrides[get_session] = get_session_override
    client = TestClient(main_app)
    return client


@pytest.fixture
def db(prepare_database):
    session = scoped_session_factory()
    yield session
    session.close()
