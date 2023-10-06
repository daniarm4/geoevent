from src.event.service import (
    get, 
    get_events,
    get_events_by_user,
    create_event,
    delete_event,
    update_event
)
from src.event.schemas import EventCreate, EventUpdate


def test_get(event_factory, db_session):
    t_event = event_factory()
    event = get(db_session=db_session, event_id=t_event.id)
    assert event.id == t_event.id


def test_get_events(event_factory, db_session):
    t_events = event_factory.create_batch(10)
    events = get_events(db_session=db_session)
    assert len(t_events) == len(events)


def test_get_events_by_user(user_factory, event_factory, db_session):
    user = user_factory()
    t_events = event_factory.create_batch(10, user=user)
    events = get_events_by_user(db_session=db_session, user_id=user.id)
    assert len(t_events) == len(events)


def test_create_event(user_factory, db_session):
    user = user_factory()
    event_in = EventCreate(
        name='new event',
        description='description',
        longitude=13.537482,
        latitude=13.534123 
    )
    event = create_event(db_session=db_session, event_in=event_in, user_id=user.id)
    db_session.commit()
    assert event 
    created_event = get(db_session=db_session, event_id=event.id)
    assert created_event


def test_delete_event(event_factory, db_session):
    event = event_factory()
    delete_event(db_session=db_session, event=event)
    db_session.commit()
    deleted_event = get(db_session=db_session, event_id=event.id)
    assert  not deleted_event


def test_update_event(event_factory, db_session):
    event = event_factory()
    event_in = EventUpdate(
        description='New description'
    )
    update_event(db_session=db_session, event_id=event.id, values=event_in)
    db_session.commit()
    updated_event = get(db_session=db_session, event_id=event.id)   
    assert updated_event.description == 'New description'
