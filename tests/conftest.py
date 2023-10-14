import pytest

from fastapi.testclient import TestClient

from sqlalchemy import create_engine, delete

from tests.database import Session
from tests.factories import UserFactory, EventFactory
from src.main import app 
from src.database import Base, get_session
from src.event.models import Event
from src.auth.models import User
from src.auth.auth import get_hashed_password, get_access_token

TEST_DATABASE_URL = 'postgresql://postgres:postgres@localhost/test_geoevent_database'

test_engine = create_engine(TEST_DATABASE_URL)


@pytest.fixture(scope='session', autouse=True)
def db_setup(request):
    Base.metadata.create_all(test_engine)
    Session.configure(bind=test_engine, expire_on_commit=False)
    
    def override_get_session():
        return Session
    
    app.dependency_overrides[get_session] = override_get_session

    def teardown():
        Base.metadata.drop_all(test_engine)
        app.dependency_overrides.clear()

    request.addfinalizer(teardown)


@pytest.fixture
def db_session(request):
    session = Session()
    session.begin_nested()

    def teardown():
        session.rollback()
        session.close()

    request.addfinalizer(teardown)
    return session


@pytest.fixture(autouse=True) 
def cleanup():
    user_stmt = delete(User)
    event_stmt = delete(Event)
    with Session() as session:
        session.execute(user_stmt)
        session.execute(event_stmt)
        session.commit()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def auth_user():
    with Session() as session:
        hashed_password = get_hashed_password('12345678')
        user = User(
            email='test_user@example.com',
            username='test_user',
            hashed_password=hashed_password 
        )
        session.add(user)
        session.commit()
    return user 


@pytest.fixture() 
def token(auth_user):
    access_token = get_access_token(data={'sub': auth_user.email})
    return access_token


@pytest.fixture
def auth_header(token):
    return {'Authorization': f'Bearer {token}'}


@pytest.fixture 
def user_factory():
    return UserFactory


@pytest.fixture 
def event_factory():
    return EventFactory
