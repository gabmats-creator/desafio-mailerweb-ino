from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.exceptions.base import BusinessRuleError

class UserRepository:
    def __init__(self, database: AsyncSession) -> None:
        self.database_session = database

    async def get_user_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        return (await self.database_session.execute(statement)).scalar_one_or_none()

    async def get_user_by_id(self, user_id: int) -> User | None:
        statement = select(User).where(User.id == user_id)
        return (await self.database_session.execute(statement)).scalar_one_or_none()

    async def create_user(self, email: str, password_hash: str, user_name: str) -> int:
        statement = (
            insert(User)
            .values(email=email, password_hash=password_hash, user_name=user_name)
            .returning(User.id)
        )
        try:
            user_id = (await self.database_session.execute(statement)).scalar_one()
            await self.database_session.commit()
            return user_id
        except IntegrityError:
            await self.database_session.rollback()
            raise BusinessRuleError("Já existe um usuário com este e-mail.")

    async def update_user(self, user: User) -> None:
        self.database_session.add(user)
        try:
            await self.database_session.commit()
            await self.database_session.refresh(user)
        except IntegrityError:
            await self.database_session.rollback()
            raise BusinessRuleError("E-mail informado já está em uso por outra conta.")