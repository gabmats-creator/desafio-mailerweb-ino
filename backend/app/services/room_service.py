from app.repositories.room_repo import RoomRepository
from app.schemas.room_schema import RoomCreate, RoomResponse
from fastapi_pagination import LimitOffsetPage
from app.exceptions.base import NotFoundError


class RoomService:
    def __init__(self, room_repository: RoomRepository) -> None:
        self.room_repository: RoomRepository = room_repository
    
    async def create_room(self, room: RoomCreate) -> int:
        return await self.room_repository.create_room(room)

    async def get_rooms(self) -> LimitOffsetPage[RoomResponse]:
        return await self.room_repository.get_rooms()
    
    async def get_room_by_id(self, room_id: int) -> RoomResponse:
        room = await self.room_repository.get_room_by_id(room_id)

        if room is None:
            raise NotFoundError(message=f"Sala de ID {room_id} não encontrada")

        return room