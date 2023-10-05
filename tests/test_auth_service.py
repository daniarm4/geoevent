from src.auth.service import (
    get, 
    create, 
    get_user_by_email,
    get_user_by_username,
    delete 
)
from src.auth.schemas import UserCreate


def test_get(db_session, user):
    db_user = get(db_session=db_session, user_id=user.id)
    assert user.id == db_user.id


def test_get_user_by_email(db_session, user):
    db_user = get_user_by_email(db_session=db_session, email=user.email)
    assert user.id == db_user.id


def test_get_user_by_username(db_session, user):
    db_user = get_user_by_username(db_session=db_session, username=user.username)
    assert user.id == db_user.id


def test_create(db_session):
    user_in = UserCreate(
        email='new_user@example.com',
        username='new_user', 
        password='12345678'
    )
    user = create(db_session=db_session, user_in=user_in)
    db_session.commit()
    assert user


def test_delete(db_session, user):
    user_id = user.id
    delete(db_session=db_session, user=user)
    db_session.commit()
    db_user = get(db_session=db_session, user_id=user_id)
    assert db_user is None
