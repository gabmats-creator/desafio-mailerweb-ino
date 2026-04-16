from fastapi import APIRouter

from app.api.routers.health import router as health_router
from app.api.routers.bookings import router as booking_router
from app.api.routers.rooms import router as room_router

api_router = APIRouter()
api_router.include_router(health_router, prefix="/health", tags=["health"])
api_router.include_router(booking_router, prefix="/bookings", tags=["bookings"])
api_router.include_router(room_router, prefix="/rooms", tags=["rooms"])