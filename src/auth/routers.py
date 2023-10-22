from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm

from pydantic import EmailStr

from src.database import get_session
from src.auth.service import create, get_user_by_username_or_email, get_user_by_email
from src.auth.models import User
from src.auth.schemas import Token, UserCreate, UserRead
from src.auth.auth import check_password, get_access_token, get_current_user

router = APIRouter(prefix="/users")


@router.post("/login", response_model=Token)
def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
        Session=Depends(get_session)
    ):
    credentials_wrong_response = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password'
        )
    with Session() as session:
        user = get_user_by_email(db_session=session, email=form_data.username)
        if not user:
            raise credentials_wrong_response
    password_is_valid = check_password(form_data.password, user.hashed_password) 
    if not password_is_valid:
        raise credentials_wrong_response
    access_token = get_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/create", response_model=UserRead)
def user_create(email: Annotated[str, Form()], 
                username: Annotated[str, Form()],
                password: Annotated[str, Form()], 
                Session=Depends(get_session)):
    with Session() as session:
        user_in = UserCreate(email=email, username=username, password=password)
        user = get_user_by_username_or_email(db_session=session, username=user_in.username, email=user_in.email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='User with this credentials is already exists'
            )
        user = create(db_session=session, user_in=user_in)
        session.commit()
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "events": []
    }


@router.get("/get_user/{email}", response_model=UserRead)
def get_user(email: EmailStr, Session=Depends(get_session)):
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


@router.get("/check_auth", response_model=UserRead)
def check_auth(current_user: Annotated[User, Depends(get_current_user)]):
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
