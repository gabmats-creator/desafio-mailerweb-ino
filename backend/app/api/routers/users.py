from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.services.user_service import UserService
from app.repositories.user_repo import UserRepository
from app.schemas.user_schema import UserCreate, UserUpdate, TokenResponse
from app.schemas.base import SuccessOutputResponse
from app.exceptions.exception_decorator import handle_route_errors

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
@handle_route_errors
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> SuccessOutputResponse:
    service = UserService(UserRepository(database=db))
    user_id = await service.create_user(user)
    return SuccessOutputResponse(message=f"Usuário de ID {user_id} criado com sucesso")

@router.put("/{user_id}", status_code=status.HTTP_200_OK)
@handle_route_errors
async def update_user(
    user_id: int,
    user: UserUpdate,
    db: AsyncSession = Depends(get_db),
) -> SuccessOutputResponse:
    service = UserService(UserRepository(database=db))
    await service.update_user(user_id, user)
    return SuccessOutputResponse(message=f"Usuário de ID {user_id} atualizado com sucesso")

# Rota de Login (OAuth2 nativo do Swagger)
@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
@handle_route_errors
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    service = UserService(UserRepository(database=db))
    return await service.login(form_data)