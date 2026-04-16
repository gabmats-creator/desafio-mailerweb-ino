from fastapi import APIRouter, Depends
from app.api.dependencies import get_current_user

from app.api.routers.health import router as health_router
from app.api.routers.bookings import router as booking_router
from app.api.routers.rooms import router as room_router
from app.api.routers.users import router as user_router

api_router = APIRouter()
api_router.include_router(health_router, prefix="/health", tags=["health"])
api_router.include_router(
    booking_router,
    prefix="/bookings",
    tags=["bookings"],
    dependencies=[Depends(get_current_user)],
)
api_router.include_router(
    room_router,
    prefix="/rooms",
    tags=["rooms"],
    dependencies=[Depends(get_current_user)],
)
api_router.include_router(user_router, prefix="/users", tags=["users"])
