from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    capacity = Column(Integer, nullable=False)

    bookings = relationship("Booking", back_populates="room", cascade="all, delete-orphan")