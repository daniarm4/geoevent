from typing import Annotated
from datetime import timedelta, datetime

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status 

from sqlalchemy import select

from passlib.context import CryptContext
from jose import jwt, JWTError

from src import config
from src.database import Session
from src.auth.models import User

JWT_SECRET_KEY = config.JWT_SECRET_KEY
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/users/login')

def check_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


def get_hashed_password(password):
    return pwd_context.hash(password) 


def get_access_token(data: dict):
    to_encode = data.copy() 
    expire = datetime.utcnow() + timedelta(days=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm="HS256")
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try: 
        payload = jwt.decode(token=token, key=JWT_SECRET_KEY,algorithms=['HS256'])
        email = payload.get("sub")
        if not email: 
            raise credentials_exception 
    except JWTError:    
        raise credentials_exception
    with Session() as session:
        query = select(User).where(User.email==email)
        user = session.scalar(query)
    if not user:
        raise credentials_exception
    return user 
