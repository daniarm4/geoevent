from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Numeric, DateTime 

from src.database import Base


class Event(Base):
    __tablename__ = 'event'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    created_at = mapped_column(DateTime(timezone=True), default=datetime.utcnow(), nullable=False)
    longitude = mapped_column(Numeric(12, 6), nullable=False) 
    latitude = mapped_column(Numeric(12, 6), nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
    user: Mapped["User"] = relationship(back_populates='events')
