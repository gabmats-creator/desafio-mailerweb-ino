import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.core.settings import settings
from app.repositories.user_repo import UserRepository
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.PREFIX}/users/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
) -> User:
    """
    Valida o token JWT e devolve o utilizador do banco de dados.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Poderia não validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decodifica o token usando a secret que está no settings.py
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        user_id: str = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except jwt.PyJWTError:
        raise credentials_exception

    repository = UserRepository(database=db)
    user = await repository.get_user_by_id(int(user_id))

    if user is None:
        raise credentials_exception

    return user
