from jose import jwt 
from src.config import JWT_SECRET_KEY


def test_create_user(client):
    user_in = {
        'email': 'qwe@example.com', 
        'username': 'qwe', 
        'password': '12345678'
    }
    response = client.post('/users/create', json=user_in)
    assert response.status_code == 200


def test_login(client, auth_user):
    data = {
        'username': auth_user.email,
        'password': '12345678',
    }
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = client.post(
                    '/users/login', 
                    data=data, 
                    headers=headers
                )
    assert response.status_code == 200
    access_token = response.json()['access_token']
    assert access_token
    payload = jwt.decode(token=access_token, key=JWT_SECRET_KEY)
    assert payload.get('sub') == auth_user.email


def test_get_user(client, auth_user):
    response = client.get(f'users/get_user/{auth_user.email}')
    assert response.status_code == 200
    assert response.json()['id'] == auth_user.id


def test_get_me(client, auth_header):
    response = client.get('/users/me', headers=auth_header)
    assert response.status_code == 200
