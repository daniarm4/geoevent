from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from src.event.models import Event
from src.event.schemas import EventCreate, EventUpdate


def get(db_session: Session, event_id: int) -> Optional[Event]:
    """Gets an event by ID.

    Args:
        db_session: The database session.
        event_id: The ID of the event to get.
    
    Returns:
        The Event object if found, else None.
    """
    query = select(Event).where(Event.id==event_id)
    event = db_session.execute(query).scalar()
    return event


def get_events(db_session: Session) -> Optional[list[Event]]:
    """Gets all events.

    Args:
        db_session: The database session.
        
    Returns: 
        A list of all Event objects.
    """
    query = select(Event)
    events = db_session.scalars(query).all()
    return events


def get_events_by_user(db_session: Session, user_id: int) -> Optional[Event]:
    """Gets events for a user.

    Args:
        db_session: The database session.
        user_id: The ID of the user.

    Returns:
        An Event object if found, else None.
    """
    query = select(Event).where(Event.user_id==user_id)
    event = db_session.scalars(query).all()
    return event


def create_event(db_session: Session, event_in: EventCreate, user_id: int) -> Event:
    """Creates a new event.

    Args:
        db_session: The database session.
        event_in: The data for the new event.
        user_id: The ID of the user creating the event.

    Returns:
        The new Event object.
    """
    event = Event(
        **event_in.model_dump(),
        user_id=user_id
    )
    db_session.add(event)
    return event 


def delete_event(db_session: Session, event: Event) -> None:
    """Deletes an event.

    Args:
        db_session: The database session.
        event: The Event object to delete.
    """
    db_session.delete(event)


def update_event(db_session: Session, event_id: int, values: EventUpdate) -> None:
    """Updates an event.

    Args:
        db_session: The database session.
        event_id: The ID of the event to update.
        values: The data to update for the event.
    """
    stmt = (
        update(Event)
        .where(Event.id==event_id)
        .values(**values.model_dump(exclude_none=True))
    )
    db_session.execute(stmt)
