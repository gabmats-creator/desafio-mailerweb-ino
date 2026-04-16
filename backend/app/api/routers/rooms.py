from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.services.room_service import RoomService
from app.schemas.room_schema import RoomCreate, RoomResponse
from app.repositories.room_repo import RoomRepository
from app.schemas.base import SuccessOutputResponse
from fastapi_pagination import LimitOffsetPage
from app.exceptions.exception_decorator import handle_route_errors

router = APIRouter()


# TODO autenticar rotas
@router.post("/", status_code=status.HTTP_201_CREATED)
@handle_route_errors
async def create_room(
    room: RoomCreate,
    db: AsyncSession = Depends(get_db),
) -> SuccessOutputResponse:
    service = RoomService(RoomRepository(database=db))
    room_id = await service.create_room(room)
    return SuccessOutputResponse(message=f"Sala de ID {room_id} criada com sucesso")


@router.get("/", status_code=status.HTTP_200_OK)
@handle_route_errors
async def get_rooms(
    db: AsyncSession = Depends(get_db),
) -> LimitOffsetPage[RoomResponse]:
    service = RoomService(RoomRepository(database=db))
    return await service.get_rooms()


@router.get("/{room_id}", status_code=status.HTTP_200_OK)
@handle_route_errors
async def get_room_by_id(
    room_id: int,
    db: AsyncSession = Depends(get_db),
) -> RoomResponse:
    service = RoomService(RoomRepository(database=db))
    return await service.get_room_by_id(room_id)
