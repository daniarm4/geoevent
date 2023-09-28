from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from pydantic import EmailStr

from src.database import Session
from src.auth.service import create, get_user_by_email
from src.auth.models import User
from src.auth.schemas import Token, UserCreate, UserRead
from src.auth.auth import check_password, get_access_token, get_current_user

router = APIRouter(prefix="/users")


@router.post("/login", response_model=Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    with Session() as session:
        user = get_user_by_email(db_session=session, email=form_data.username)
        if not user:
            raise credentials_exception
    password_is_valid = check_password(form_data.password, user.hashed_password) 
    if not password_is_valid:
        raise credentials_exception
    access_token = get_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/create", response_model=UserRead)
def user_create(user_in: UserCreate):
    with Session() as session:
        user = get_user_by_email(db_session=session, email=user_in.email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )
        user = create(db_session=session, user_in=user_in)
        session.commit()
    return {"id": user.id, "email": user.email, "username": user.username, "events": []}


@router.get("/get_user", response_model=UserRead)
def get_user(email: EmailStr):
    with Session() as session:
        user = get_user_by_email(db_session=session, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with this email and password not found"
        )
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "events": []
    }


@router.get("/me", response_model=UserRead)
def me(current_user: Annotated[User, Depends(get_current_user)]):
    if not current_user: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not authenticated"
        )
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "events": []
    }
