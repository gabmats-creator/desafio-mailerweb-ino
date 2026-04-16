from pydantic import Field
from app.schemas.base import BaseDTO

# Classe base com os campos comuns
class RoomBase(BaseDTO):
    name: str = Field(..., min_length=3, max_length=100, description="Nome da sala")
    capacity: int = Field(..., gt=0, description="Capacidade máxima de pessoas")


class RoomCreate(RoomBase):
    pass


class RoomResponse(RoomBase):
    id: int
