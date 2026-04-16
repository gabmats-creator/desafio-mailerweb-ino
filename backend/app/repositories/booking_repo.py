import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, insert, update
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from app.models.booking import Booking, BookingStatus
from app.models.user import User
from app.models.room import Room
from app.models.outbox import OutboxEvent, EventType
from app.schemas.booking_schema import (
    BookingCreate,
    BookingResponse,
    BookingDetailResponse,
    OutboxEventSchema,
)
from app.exceptions.base import BusinessRuleError
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import LimitOffsetPage


class BookingRepository:
    def __init__(self, database: AsyncSession) -> None:
        self.database_session = database

    async def check_overlap(
        self,
        room_id: int,
        start_at: datetime,
        end_at: datetime,
        exclude_booking_id: int | None = None,
    ) -> bool:
        statement = select(Booking).where(
            and_(
                Booking.room_id == room_id,
                Booking.status == BookingStatus.ACTIVE,
                Booking.start_at < end_at,
                Booking.end_at > start_at,
            )
        )

        if exclude_booking_id:
            statement = statement.where(Booking.id != exclude_booking_id)

        result = await self.database_session.execute(statement)
        return result.scalars().first() is not None

    async def create_booking(
        self,
        booking: BookingCreate,
        user_id: int,
        payload: dict,
    ) -> int:
        # 1. Prepara o Insert da Reserva
        booking_stmt = (
            insert(Booking)
            .values(
                title=booking.title,
                room_id=booking.room_id,
                user_id=user_id,
                start_at=booking.start_at,
                end_at=booking.end_at,
                participants=booking.participants,
                status=BookingStatus.ACTIVE,
            )
            .returning(Booking.id)
        )

        try:
            # 2. Executa a reserva e pega o ID gerado
            booking_id = (
                await self.database_session.execute(booking_stmt)
            ).scalar_one()

            # 4. Insere no Outbox na mesma sessão
            payload["booking_id"] = booking_id
            outbox_stmt = insert(OutboxEvent).values(
                event_type=EventType.BOOKING_CREATED, payload=payload
            )
            await self.database_session.execute(outbox_stmt)

            # 5. O Commit Atômico (Salva os dois no banco ao mesmo tempo)
            await self.database_session.commit()
            return booking_id

        except IntegrityError:
            await self.database_session.rollback()
            raise BusinessRuleError(
                "Erro ao criar reserva. Verifique se a sala informada realmente existe."
            )

    async def update_booking(self, booking_id: int, new_data: BookingCreate, payload: dict) -> None:
        statement = update(Booking).where(Booking.id == booking_id).values(
            title=new_data.title,
            room_id=new_data.room_id,
            start_at=new_data.start_at,
            end_at=new_data.end_at,
            participants=new_data.participants
        )

        # Gera o evento de Update
        outbox_event = OutboxEvent(
            event_type=EventType.BOOKING_UPDATED, payload=payload
        )

        await self.database_session.execute(statement)
        self.database_session.add(outbox_event)

        await self.database_session.commit()

    async def cancel_booking(self, booking_id: int, payload: dict) -> None:
        # Cancela (Soft Delete)
        statement = update(Booking).where(Booking.id == booking_id).values(
            status=BookingStatus.CANCELED
        )

        # Gera o evento de Cancelamento
        outbox_event = OutboxEvent(
            event_type=EventType.BOOKING_CANCELED, payload=payload
        )

        await self.database_session.execute(statement)
        self.database_session.add(outbox_event)

        await self.database_session.commit()

    async def get_bookings(self) -> LimitOffsetPage[BookingResponse]:
        statement = (
            select(
                Booking.id,
                Booking.room_id,
                Booking.status,
                Booking.start_at,
                Booking.end_at,
                Booking.title,
                Room.name.label("room_name"),
                Booking.participants,
            )
            .join(Room, Room.id == Booking.room_id)
            .order_by(Booking.id)
        )

        return await paginate(self.database_session, statement, unique=False)

    async def get_booking_by_id(self, booking_id: int) -> BookingDetailResponse | None:
        statement = (
            select(
                Booking.id,
                Booking.status,
                Booking.start_at,
                Booking.end_at,
                Booking.title,
                Booking.participants,
                User.user_name,
                Room.name.label("room_name"),
                Booking.room_id,
            )
            .join(User, User.id == Booking.user_id)
            .join(Room, Room.id == Booking.room_id)
            .where(Booking.id == booking_id)
        )

        return (await self.database_session.execute(statement)).one_or_none()

    async def get_room_data(self, room_id: int) -> object | None:
        statement = select(Room.capacity, Room.name).where(Room.id == room_id)
        return (await self.database_session.execute(statement)).one_or_none()
