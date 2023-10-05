from typing import Optional, List
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class EventBase(BaseModel):
    name: str 
    description: Optional[str] = None
    longitude: Decimal = Field(max_digits=12, decimal_places=6)
    latitude: Decimal = Field(max_digits=12, decimal_places=6)


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
    events: List[EventRead] = []
