from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.booking_service import BookingService
from app.repositories.booking_repo import BookingRepository
from app.schemas.booking_schema import BookingCreate, BookingResponse, BookingDetailResponse
from app.schemas.base import SuccessOutputResponse
from app.exceptions.exception_decorator import handle_route_errors
from fastapi_pagination import LimitOffsetPage

# Importando o usuário e a dependência de autenticação que você criou
from app.models.user import User
from app.api.dependencies import get_current_user 

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
@handle_route_errors
async def create_booking(
    booking: BookingCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> SuccessOutputResponse:
    
    service = BookingService(BookingRepository(database=db))
    booking_id = await service.create_booking(booking, user_id=current_user.id)
    
    return SuccessOutputResponse(message=f"Reserva de ID {booking_id} criada com sucesso e notificação enfileirada.")

@router.put("/{booking_id}", status_code=status.HTTP_200_OK)
@handle_route_errors
async def update_booking(
    booking_id: int,
    booking: BookingCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> SuccessOutputResponse:
    
    service = BookingService(BookingRepository(database=db))
    await service.update_booking(booking_id, current_user.id, booking)
    
    return SuccessOutputResponse(message=f"Reserva de ID {booking_id} atualizada com sucesso.")

@router.patch("/{booking_id}/cancel", status_code=status.HTTP_200_OK)
@handle_route_errors
async def cancel_booking(
    booking_id: int,
    db: AsyncSession = Depends(get_db),
) -> SuccessOutputResponse:
    
    service = BookingService(BookingRepository(database=db))
    await service.cancel_booking(booking_id)
    
    return SuccessOutputResponse(message=f"Reserva de ID {booking_id} cancelada.")

@router.get("/", status_code=status.HTTP_200_OK)
@handle_route_errors
async def get_bookings(
    db: AsyncSession = Depends(get_db),
) -> LimitOffsetPage[BookingResponse]:
    service = BookingService(BookingRepository(database=db))
    return await service.get_bookings()

@router.get("/{booking_id}", status_code=status.HTTP_200_OK)
@handle_route_errors
async def get_booking_by_id(
    booking_id: int,
    db: AsyncSession = Depends(get_db),
) -> BookingDetailResponse:
    service = BookingService(BookingRepository(database=db))
    return await service.get_booking_by_id(booking_id)
