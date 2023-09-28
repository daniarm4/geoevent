from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel


class EventBase(BaseModel):
    name: str 
    description: Optional[str] = None
    longitude: float 
    latitude: float 


class EventCreate(EventBase):
    pass 


class EventRead(EventBase):
    id: int
    created_at: datetime
    user_id: int 


class EventUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class EventList(BaseModel):
    events: Optional[List[EventRead]]
