from datetime import timedelta

from app.repositories.booking_repo import BookingRepository
from app.schemas.booking_schema import (
    BookingCreate,
    BookingResponse,
    BookingDetailResponse,
    OutboxEventSchema,
)
from app.exceptions.base import BusinessRuleError, NotFoundError
from app.models.booking import BookingStatus
from fastapi_pagination import LimitOffsetPage


class BookingService:
    def __init__(self, booking_repository: BookingRepository) -> None:
        self.booking_repository = booking_repository

    async def _validate_room(self, booking: BookingCreate) -> str:
        room_data = await self.booking_repository.get_room_data(
            room_id=booking.room_id,
        )

        if room_data is None:
            raise NotFoundError(message=f"Sala de ID {booking.room_id} nao encontrada.")

        exceeded_capacity = room_data.capacity < len(booking.participants)

        if exceeded_capacity:
            raise BusinessRuleError("A sala excedeu sua capacidade.")

        return room_data.name

    async def _validate_booking_interval(self, booking: BookingCreate) -> None:
        if booking.start_at >= booking.end_at:
            raise BusinessRuleError(
                "O horário de início (start_at) deve ser anterior ao término (end_at)."
            )

        duration = booking.end_at - booking.start_at

        if duration < timedelta(minutes=15):
            raise BusinessRuleError("A reserva deve ter duração mínima de 15 minutos.")

        if duration > timedelta(hours=8):
            raise BusinessRuleError("A reserva não pode exceder 8 horas de duração.")

    async def create_booking(self, booking: BookingCreate, user_id: int) -> int:
        await self._validate_booking_interval(booking)
        has_overlap = await self.booking_repository.check_overlap(
            room_id=booking.room_id, start_at=booking.start_at, end_at=booking.end_at
        )

        if has_overlap:
            raise BusinessRuleError("A sala já está reservada para este horário.")

        room_name = await self._validate_room(booking)

        payload = {
            "title": booking.title,
            "start_at": booking.start_at.isoformat(),
            "end_at": booking.end_at.isoformat(),
            "participants": booking.participants,
            "room_name": room_name,
        }

        return await self.booking_repository.create_booking(booking, user_id, payload)

    async def update_booking(
        self, booking_id: int, user_id: int, new_data: BookingCreate
    ) -> None:
        await self._validate_booking_interval(new_data)
        booking = await self.booking_repository.get_booking_by_id(booking_id)

        if not booking:
            raise NotFoundError(message=f"Reserva de ID {booking_id} não encontrada.")

        if booking.status == BookingStatus.CANCELED:
            raise BusinessRuleError(
                "Não é possível editar uma reserva que já foi cancelada."
            )

        # Verifica overlap ignorando a própria reserva que estamos editando
        has_overlap = await self.booking_repository.check_overlap(
            room_id=new_data.room_id,
            start_at=new_data.start_at,
            end_at=new_data.end_at,
            exclude_booking_id=booking_id,
        )

        if has_overlap:
            raise BusinessRuleError(
                "Os novos horários entram em conflito com outra reserva ativa."
            )

        room_name = await self._validate_room(new_data)

        payload = {
            "booking_id": booking_id,
            "title": new_data.title,
            "start_at": new_data.start_at.isoformat(),
            "end_at": new_data.end_at.isoformat(),
            "participants": new_data.participants,
            "room_name": room_name,
        }

        await self.booking_repository.update_booking(booking_id, new_data, payload)

    async def cancel_booking(self, booking_id: int) -> None:
        booking = await self.booking_repository.get_booking_by_id(booking_id)

        if booking is None:
            raise NotFoundError(message=f"Reserva de ID {booking_id} não encontrada.")

        if booking.status == BookingStatus.CANCELED:
            raise BusinessRuleError("Esta reserva já encontra-se cancelada.")

        payload = {
            "booking_id": booking_id,
            "title": booking.title,
            "start_at": booking.start_at.isoformat(),
            "end_at": booking.end_at.isoformat(),
            "participants": booking.participants,
            "room_name": booking.room_name,
        }

        await self.booking_repository.cancel_booking(booking_id, payload)

    async def get_bookings(self) -> LimitOffsetPage[BookingResponse]:
        return await self.booking_repository.get_bookings()

    async def get_booking_by_id(self, booking_id: int) -> BookingDetailResponse:
        booking = await self.booking_repository.get_booking_by_id(booking_id)

        if booking_id is None:
            raise NotFoundError(message=f"Reserva de ID {booking_id} nao encontrada.")

        return booking
