from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SqlEnum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.db.database import Base


class BookingStatus(str, Enum):
    ACTIVE = "Ativa"
    CANCELED = "Cancelada"


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)

    start_at = Column(DateTime(timezone=True), nullable=False, index=True)
    end_at = Column(DateTime(timezone=True), nullable=False, index=True)

    status = Column(
        String(20), SqlEnum(BookingStatus), default=BookingStatus.ACTIVE, nullable=False
    )

    participants = Column(JSONB, nullable=False)

    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    room = relationship("Room", back_populates="bookings")
    user = relationship("User", back_populates="bookings")
