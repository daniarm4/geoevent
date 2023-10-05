from typing import List

from pydantic import BaseModel, EmailStr, SecretStr, Field

from src.event.schemas import EventRead


class UserBase(BaseModel):
    email: EmailStr = Field(max_length=155)
    username: str = Field(max_length=155)


class UserCreate(UserBase):
    password: SecretStr = Field(min_length=8, max_length=16)


class UserIn(UserBase):    
    password: SecretStr = Field(min_length=8, max_length=16)


class UserRead(UserBase):
    id: int 
    events: List[EventRead] = []
    

class UserUpdate(UserBase):
    pass 


class Token(BaseModel):
    access_token: str 


class TokenData(BaseModel):
    email: EmailStr 