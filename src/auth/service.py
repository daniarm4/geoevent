from typing import Optional

from sqlalchemy import select

from src.database import Session
from src.auth.models import User
from src.auth.schemas import UserCreate
from src.auth.auth import get_hashed_password

def get(db_session: Session, user_id: int) -> Optional[User]:
    """Gets a user by ID.

    Args:
        db_session: The database session.
        user_id: The ID of the user to get.

    Returns:
        The User object if found, else None.
    """
    return db_session.get(User, user_id)


def get_user_by_email(db_session: Session, email) -> Optional[User]:
    """Gets a user by email.

    Args:
        db_session: The database session.
        email: The email of the user to get.

    Returns:
        The User object if found, else None.
    """
    query = select(User).where(User.email==email)
    user = db_session.scalar(query)
    return user


def get_user_by_username(db_session: Session, username) -> Optional[User]:
    """Gets a user by username.

    Args:
        db_session: The database session.
        username: The username of the user to get.

    Returns:
        The User object if found, else None.
    """
    query = select(User).where(User.username==username)
    user = db_session.scalar(query)
    return user


def create(db_session: Session, user_in: UserCreate) -> User:
    """Creates a new user.

    Args:
        db_session: The database session.
        user_in: The data for the new user.

    Returns:
        The new User object.
    """
    hashed_password = get_hashed_password(user_in.password)
    user = User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=hashed_password    
    )
    db_session.add(user)
    return user 


def delete(db_session: Session, user: User) -> None:
    """Deletes a user.

    Args:
        db_session: The database session.
        user: The User object to delete.
    """
    db_session.delete(user)
