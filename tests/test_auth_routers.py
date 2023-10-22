from jose import jwt 

from src.auth.service import get 
from src.config import JWT_SECRET_KEY


def test_create_user(client, db_session):
    user_in = {
        'email': 'qwe@example.com', 
        'username': 'qwe', 
        'password': '12345678'
    }
    response = client.post('/users/create', data=user_in)
    assert response.status_code == 200
    user_id = response.json()['id']
    user = get(db_session=db_session, user_id=user_id)
    assert user


def test_login(client, user_factory):
    user = user_factory()
    data = {
        'username': user.email,
        'password': '12345678',
    }
    response = client.post('/users/login', data=data)
    assert response.status_code == 200
    access_token = response.json()['access_token']
    assert access_token
    payload = jwt.decode(token=access_token, key=JWT_SECRET_KEY)
    assert payload.get('sub') == user.email


def test_get_user(client, user_factory):
    user = user_factory()
    response = client.get(f'users/get_user/{user.email}')
    assert response.status_code == 200
    assert response.json()['id'] == user.id


def test_check_auth(client, auth_header):
    response = client.get('/users/check_auth', headers=auth_header)
    assert response.status_code == 200
