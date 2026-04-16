from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError
from fastapi_pagination.ext.sqlalchemy import paginate
from app.models.room import Room
from app.schemas.room_schema import RoomCreate
from app.exceptions.base import BusinessRuleError


class RoomRepository:
    def __init__(self, database: AsyncSession) -> None:
        self.database_session = database

    async def create_room(self, room: RoomCreate) -> int:
        statement = (
            insert(Room)
            .values(
                name=room.name,
                capacity=room.capacity,
            )
            .returning(Room.id)
        )

        try:
            room_id = (await self.database_session.execute(statement)).scalar_one()
            await self.database_session.commit()
            return room_id

        except IntegrityError:
            await self.database_session.rollback()
            raise BusinessRuleError("Já existe uma sala com este nome.")

    async def get_rooms(self) -> list[Room]:
        statement = select(Room.id, Room.name, Room.capacity).order_by(Room.name)

        return await paginate(self.database_session, statement)

    async def get_room_by_id(self, room_id: int) -> Room | None:
        statement = select(Room.id, Room.name, Room.capacity).where(Room.id == room_id)
        return (await self.database_session.execute(statement)).one_or_none()
