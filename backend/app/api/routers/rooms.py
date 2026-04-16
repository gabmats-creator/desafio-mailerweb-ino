from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.services.room_service import RoomService
from app.schemas.room_schema import RoomCreate, RoomResponse
from app.repositories.room_repo import RoomRepository
from app.schemas.base import SuccessOutputResponse
from fastapi_pagination import LimitOffsetPage
from app.exceptions.exception_decorator import handle_route_errors

router = APIRouter()


# TODO colocar tratamento de erro em um decorator
@router.post("/", status_code=status.HTTP_201_CREATED)
@handle_route_errors
async def create_room(
    room: RoomCreate,
    db: AsyncSession = Depends(get_db),
) -> SuccessOutputResponse:
    # try:
    service = RoomService(RoomRepository(database=db))
    # user_id viria do token JWT (dependência de auth)
    room_id = await service.create_room(room)
    # TODO retornar o id ao invés de coroutine
    return SuccessOutputResponse(message=f"Sala de ID {room_id} criada com sucesso")
    # except ValueError as e:
    #     raise HTTPException(status_code=409, detail=str(e))
    # except Exception as e:
    #     import traceback

    #     traceback.print_exc()
    #     raise HTTPException(status_code=500, detail=str(e))


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
