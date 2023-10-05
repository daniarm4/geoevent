import pytest

from fastapi.testclient import TestClient

from sqlalchemy import create_engine

from tests.database import Session
from tests.factories import UserFactory, EventFactory
from src.main import app 
from src.database import Base, get_session
from src.auth.models import User
from src.auth.auth import get_hashed_password, get_access_token
from src.config import TEST_DATABASE_URL

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

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(scope='session')
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


@pytest.fixture(scope='session') 
def token(auth_user):
    access_token = get_access_token(data={'sub': auth_user.email})
    return access_token


@pytest.fixture
def auth_header(token):
    return {'Authorization': f'Bearer {token}'}


@pytest.fixture 
def user():
    return UserFactory()


@pytest.fixture 
def event():
    return EventFactory()
