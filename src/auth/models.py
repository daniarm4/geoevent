from typing import List

from sqlalchemy.orm import mapped_column, Mapped, relationship, validates
from sqlalchemy import String

from src.database import Base


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(150), unique=True)
    username: Mapped[str] = mapped_column(String(150), unique=True)
    hashed_password: Mapped[str]

    events: Mapped[List["Event"]] = relationship(
        back_populates='user'
    )
    
    def __str__(self):
        return f"{self.username}"

    @validates('email')
    def validate_email(self, key, email):
        assert '@' in email, 'Email must contain "@"'
        return email
