from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.database import get_session
from src.auth.models import User
from src.auth.auth import get_current_user
from src.event.service import (
    get_events, 
    get, 
    get_events_by_user,
    create_event, 
    delete_event, 
    update_event, 
)
from src.event.schemas import (
    EventCreate, 
    EventRead, 
    EventList, 
    EventUpdate
)

router = APIRouter(prefix="/events")


def event_to_dict(event):
    return {
        "id": event.id,
        "name": event.name,
        "description": event.description,
        "created_at": event.created_at,
        "longitude": event.longitude,
        "latitude": event.latitude,
        "user_id": event.user_id
    }


@router.get("/", response_model=EventList)
def get_all_events(Session=Depends(get_session)):
    event_list = []
    with Session() as session:
        events = get_events(session)
        for event in events:
            event_list.append(event_to_dict(event))
    return {"events": event_list}


@router.get("/{event_id}", response_model=EventRead)
def get_event(event_id: int, Session=Depends(get_session)):    
    with Session() as session:
        event = get(session, event_id)
    response_event = event_to_dict(event)
    return response_event


@router.get("/by_user/{user_id}", response_model=EventList)
def get_events_by_user_id(user_id: int, Session=Depends(get_session)):
    event_list = []
    with Session() as session:
        events = get_events_by_user(session, user_id)
        for event in events:
            event_list.append(event_to_dict(event))
    return {"events": event_list}


@router.post("/create", response_model=EventRead)
def create_new_event(
        event_in: EventCreate, 
        current_user: Annotated[User, Depends(get_current_user)], 
        Session=Depends(get_session)
    ):
    with Session() as session:
        event = create_event(session, event_in, current_user.id)
        session.commit()
    response_event = event_to_dict(event)
    return response_event


@router.delete("/{event_id}", response_model=EventRead)
def delete_event_by_id(
        event_id: int, 
        current_user: Annotated[User, Depends(get_current_user)], 
        Session=Depends(get_session)
    ):
    with Session() as session:
        event = get(session, event_id)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"An event with this id does not exist"}
            )
        if event.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"You can't delete this event"}
            )
        event_response = event_to_dict(event)
        delete_event(session, event)
        session.commit()
    return event_response


@router.put("/{event_id}", response_model=EventRead)
def update_event_by_id(
        event_id: int, 
        values: EventUpdate, 
        current_user: Annotated[User, Depends(get_current_user)], 
        Session=Depends(get_session)
    ):
    with Session() as session:
        event = get(session, event_id)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"An event with this id does not exist"}
            )
        if event.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"You can't update this event"}
            )
        update_event(session, event_id, values)
        response_event = event_to_dict(event)
        session.commit()
    return response_event
