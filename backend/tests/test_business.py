import pytest
from unittest.mock import AsyncMock
from datetime import datetime
from app.services.booking_service import BookingService
from app.schemas.booking_schema import BookingCreate
from app.exceptions.base import BusinessRuleError

@pytest.fixture
def mock_repo():
    repo = AsyncMock()
    # Simula que a sala existe
    class FakeRoom:
        name = "Sala 1"
        capacity = 10
    repo.get_room_data.return_value = FakeRoom()
    repo.check_overlap.return_value = False # Padrão: sem conflito
    return repo

@pytest.fixture
def service(mock_repo):
    return BookingService(mock_repo)

@pytest.mark.asyncio
async def test_validacao_de_datas_inicio_maior_que_fim(service):
    """Requisito: Validação de datas"""
    booking = BookingCreate(
        title="Erro Data", room_id=1,
        start_at=datetime(2026, 4, 16, 12, 0),
        end_at=datetime(2026, 4, 16, 11, 0),
        participants=["teste@teste.com"]
    )
    with pytest.raises(BusinessRuleError, match="anterior ao término"):
        await service.create_booking(booking, user_id=1)

@pytest.mark.asyncio
async def test_conflito_de_reserva(service, mock_repo):
    """Requisito: Conflito de reserva"""
    mock_repo.check_overlap.return_value = True 
    
    booking = BookingCreate(
        title="Conflito", room_id=1,
        start_at=datetime(2026, 4, 16, 10, 0),
        end_at=datetime(2026, 4, 16, 11, 0),
        participants=["teste@teste.com"]
    )
    with pytest.raises(BusinessRuleError, match="já está reservada"):
        await service.create_booking(booking, user_id=1)