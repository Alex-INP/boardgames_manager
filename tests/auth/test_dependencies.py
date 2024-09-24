import jwt
import pytest

from src.auth.config import settings
from src.auth.dependencies import auth_only, check_not_exists, prepare_user_create_data
from src.auth.exceptions import (
    RegistrationException,
    SessionExpiredException,
    UnauthorizedException,
)
from src.auth.schemas import UserCreate
from src.utils import get_future_utc, get_past_utc
from tests.auth.factories import TokenFactory, UserFactory

pytestmark = pytest.mark.asyncio


@pytest.fixture
def form_data():
    return UserCreate(username="u_name", password="qwerty", email="somemail@mail.ru")


@pytest.fixture
def create_token(form_data):
    def _factory(exp_value=None):
        exp_value = exp_value or get_future_utc(days=10)
        return jwt.encode(
            {"sub": form_data.username, "exp": exp_value},
            settings.secret_key,
            settings.token_hash_alg,
        )

    return _factory


async def test_prepare_user_create_data_pwd_hashed(form_data):
    not_hashed_pwd = form_data.password
    res = await prepare_user_create_data(
        form_data.username, not_hashed_pwd, form_data.email
    )
    res_hashed_pwd = res.password
    assert res_hashed_pwd
    assert res_hashed_pwd != not_hashed_pwd


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


async def test_auth_only_ok(db, form_data, create_token):
    token_str = create_token()

    user = UserFactory(**form_data.model_dump())
    TokenFactory(value=token_str, user=user)

    assert user == await auth_only(db, token_str)


async def test_auth_only_jwt_token_exception(db, form_data, create_token):
    token_str = create_token()

    user = UserFactory(**form_data.model_dump())
    TokenFactory(value=token_str, user=user)
    await run_auth_only_with_exception(UnauthorizedException, db, "some_random_token")


async def test_auth_only_jwt_signature_exception(db, form_data, create_token):
    error_date = get_past_utc(days=10)
    token = create_token(error_date)

    user = UserFactory(**form_data.model_dump())
    TokenFactory(value=token, user=user)
    await run_auth_only_with_exception(UnauthorizedException, db, token)


async def test_auth_only_user_not_found(db, create_token):
    token = create_token()
    UserFactory()
    TokenFactory(value=token)
    await run_auth_only_with_exception(UnauthorizedException, db, token)


async def test_auth_only_token_not_found(db, create_token, form_data):
    UserFactory(**form_data.model_dump())
    await run_auth_only_with_exception(UnauthorizedException, db, create_token())


async def test_auth_only_session_expired(db, create_token, form_data):
    token_str = create_token()

    user = UserFactory(**form_data.model_dump())
    TokenFactory(value=token_str, user=user, expires=get_past_utc(days=10))
    await run_auth_only_with_exception(SessionExpiredException, db, token_str)


async def run_auth_only_with_exception(exception_class, *args):
    with pytest.raises(exception_class):
        await auth_only(*args)
