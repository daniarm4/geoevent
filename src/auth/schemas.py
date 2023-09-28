from typing import List

from pydantic import BaseModel, EmailStr, constr

from src.event.schemas import EventRead


class UserBase(BaseModel):
    email: EmailStr
    username: str 


class UserCreate(UserBase):
    password: constr(min_length=8, max_length=20) 


class UserIn(UserBase):    
    password: constr(min_length=8, max_length=20)


class UserRead(UserBase):
    id: int 
    events: List[EventRead] = []
    

class UserUpdate(UserBase):
    pass 


class Token(BaseModel):
    access_token: str 
    token_type: str 


class TokenData(BaseModel):
    email: str