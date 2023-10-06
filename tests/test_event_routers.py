from src.event.service import get


def test_get_all_events(client, event_factory):
    event_factory.create_batch(10)
    response = client.get('/events')
    assert response.status_code == 200
    events = response.json()['events']
    assert len(events) == 10


def test_get_event(client, event_factory):
    event = event_factory()
    response = client.get(f'/events/{event.id}')
    assert response.status_code == 200
    assert response.json()['id'] == event.id
    

def test_get_events_by_user_id(client, user_factory, event_factory):
    user = user_factory()
    event_factory.create_batch(10, user=user)
    response = client.get(f'/events/by_user/{user.id}')
    assert response.status_code == 200
    events = response.json()['events']
    assert len(events) == 10
    event = events[0]
    assert event['user_id'] == user.id


def test_create_new_event(client, auth_header, db_session):
    event_in = {
        'name': 'new event',
        'description': 'description',
        'longitude': 13.564732,
        'latitude': 13.583273
    }
    response = client.post('events/create', json=event_in, headers=auth_header)
    assert response.status_code == 200
    event_id = response.json()['id']
    event = get(db_session=db_session, event_id=event_id)
    assert event 


def test_delete_event_by_id(client, event_factory, auth_header, auth_user, db_session):
    event = event_factory(user=auth_user)
    response = client.delete(f'/events/{event.id}', headers=auth_header)
    assert response.status_code == 200
    event_id = response.json()['id']
    deleted_event = get(db_session=db_session, event_id=event_id)
    assert not deleted_event


def test_update_event_by_id(client, event_factory, auth_header, auth_user):
    event = event_factory(user=auth_user)
    values = {
        'description': 'New description'
    }
    response = client.put(f'/events/{event.id}', headers=auth_header, json=values)
    assert response.status_code == 200
    updated_event = response.json()
    assert updated_event['description'] == 'New description'
