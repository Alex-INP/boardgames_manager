import pytest

from src.auth.dependencies import check_not_exists
from src.auth.exceptions import RegistrationException
from src.auth.schemas import UserCreate
from tests.auth.factories import UserFactory

pytestmark = pytest.mark.asyncio


@pytest.fixture
def form_data():
    return UserCreate(username="u_name", password="qwerty", email="somemail@mail.ru")


async def test_check_not_exists_ok(db, form_data):
    assert await check_not_exists(db, form_data) == form_data


async def test_check_not_exists_username_exists(db, form_data):
    UserFactory(username=form_data.username)
    with pytest.raises(RegistrationException) as e:
        await check_not_exists(db, form_data)
    assert str(e.value) == f"400: Username {form_data.username} already in use."


async def test_check_not_exists_email_exists(db, form_data):
    UserFactory(email=form_data.email)
    with pytest.raises(RegistrationException) as e:
        await check_not_exists(db, form_data)
    assert str(e.value) == f"400: Email {form_data.email} already in use."
