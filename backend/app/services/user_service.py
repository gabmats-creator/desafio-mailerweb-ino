from fastapi.security import OAuth2PasswordRequestForm
from app.repositories.user_repo import UserRepository
from app.schemas.user_schema import UserCreate, UserUpdate, TokenResponse
from app.core.security import get_password_hash, verify_password, create_access_token
from app.exceptions.base import RequiresAuthError, NotFoundError

class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository: UserRepository = user_repository

    async def create_user(self, user_in: UserCreate) -> int:
        hashed_pwd = get_password_hash(user_in.password)
        return await self.user_repository.create_user(user_in.email, hashed_pwd)

    async def update_user(self, user_id: int, user_in: UserUpdate) -> None:
        user = await self.user_repository.get_user_by_id(user_id)
        
        if user is None:
            raise NotFoundError(message=f"Usuário de ID {user_id} não encontrado")

        if user_in.email:
            user.email = user_in.email
        if user_in.password:
            user.password_hash = get_password_hash(user_in.password)

        await self.user_repository.update_user(user)

    async def login(self, form_data: OAuth2PasswordRequestForm) -> TokenResponse:
        user = await self.user_repository.get_user_by_email(form_data.username)
        
        # Valida se o usuário existe e se a senha cruza com o hash do banco
        if not user or not verify_password(form_data.password, user.password_hash):
            raise RequiresAuthError("E-mail ou senha incorretos.")

        # Gera o token embutindo o ID do usuário como 'sub' (subject)
        access_token = create_access_token(data={"sub": str(user.id)})
        return TokenResponse(access_token=access_token, token_type="bearer")