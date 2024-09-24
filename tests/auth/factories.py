from factory import Sequence, SubFactory, fuzzy
from factory.alchemy import SQLAlchemyModelFactory

from src.auth.models import Token, User, UserRole
from tests.config import settings
from tests.conftest import scoped_session_factory


class UserRoleFactory(SQLAlchemyModelFactory):
    class Meta:
        model = UserRole
        sqlalchemy_session = scoped_session_factory()
        sqlalchemy_session_persistence = settings.session_action_on_factory_obj_created

    name = Sequence(lambda n: f"Role {n}")


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = scoped_session_factory()
        sqlalchemy_session_persistence = settings.session_action_on_factory_obj_created

    email = Sequence(lambda n: f"some_mail_{n}@mail.ru")
    username = fuzzy.FuzzyText()
    password = fuzzy.FuzzyText()
    is_active = True
    role = SubFactory(UserRoleFactory)


class TokenFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Token
        sqlalchemy_session = scoped_session_factory()
        sqlalchemy_session_persistence = settings.session_action_on_factory_obj_created

    value = fuzzy.FuzzyText()
    user = SubFactory(UserFactory)
