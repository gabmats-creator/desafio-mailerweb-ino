from pydantic import ConfigDict, Field, model_validator, EmailStr
from datetime import datetime, timedelta
from app.models.booking import BookingStatus
from app.exceptions.base import BusinessRuleError
from app.schemas.base import BaseDTO

class BookingBase(BaseDTO):
    title: str = Field(..., min_length=3, max_length=200, description="Título da reunião")
    room_id: int = Field(..., gt=0, description="ID da sala que será reservada")
    start_at: datetime = Field(..., description="Data e hora de início (ISO 8601)")
    end_at: datetime = Field(..., description="Data e hora de término (ISO 8601)")

    participants: list[EmailStr] = Field(..., min_length=1, description="Lista de e-mails dos convidados")

class BookingCreate(BookingBase):
    pass

class BookingResponse(BaseDTO):
    id: int
    status: BookingStatus
    room_name: str
    room_id: int
    start_at: datetime
    end_at: datetime
    title: str

class BookingDetailResponse(BookingResponse):
    user_name: str
    participants: list[EmailStr]

class OutboxEventSchema(BaseDTO):
    booking_id: int | None = None
    title: str
    room_name: str
    start_at: datetime
    end_at: datetime
    participants: list[EmailStr]