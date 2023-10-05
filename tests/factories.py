import factory 
from factory.alchemy import SQLAlchemyModelFactory
from factory.fuzzy import FuzzyText, FuzzyDecimal

from tests.database import Session 
from src.auth.auth import get_hashed_password
from src.auth.models import User
from src.event.models import Event 


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True 
        sqlalchemy_session = Session
        sqlalchemy_session_persistence = 'commit'


class UserFactory(BaseFactory):
    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda o: f'{o.username}@example.com')
    hashed_password = get_hashed_password('12345678')

    class Meta:
        model = User


class EventFactory(BaseFactory):
    name = FuzzyText()
    user = factory.SubFactory(UserFactory)
    description = FuzzyText()
    longitude = FuzzyDecimal(low=0, precision=6)
    latitude = FuzzyDecimal(low=0, precision=6)

    class Meta:
        model = Event 
