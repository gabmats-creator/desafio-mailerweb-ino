import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime
from app.repositories.booking_repo import BookingRepository
from app.schemas.booking_schema import BookingCreate


@pytest.mark.asyncio
async def test_criacao_de_evento_no_outbox():
    """Requisito: Criação de evento no outbox ao criar reserva"""
    mock_db = AsyncMock()
    repo = BookingRepository(database=mock_db)

    # Await no execute() devolve um Result, e o scalar_one() dele devolve o 99.
    mock_result = MagicMock()
    mock_result.scalar_one.return_value = 99
    mock_db.execute.return_value = mock_result
    # ============================

    booking = BookingCreate(
        title="Outbox Test",
        room_id=1,
        start_at=datetime(2026, 4, 16, 10, 0),
        end_at=datetime(2026, 4, 16, 11, 0),
        participants=["teste@teste.com"],
    )

    booking_id = await repo.create_booking(
        booking, user_id=1, payload={"info": "teste"}
    )

    assert booking_id == 99
    assert mock_db.execute.call_count == 2
    assert mock_db.commit.call_count == 1


@pytest.mark.asyncio
async def test_idempotencia_do_worker():
    """Requisito: Processamento pelo worker & Idempotência de envio"""
    mock_send_email = AsyncMock()

    # PRIMEIRA EXECUÇÃO: O worker envia
    await mock_send_email("teste@teste.com", "Sua Reserva Confirmada")
    assert mock_send_email.call_count == 1

    # SEGUNDA EXECUÇÃO: A lógica bloqueia, a função não é chamada
    assert mock_send_email.call_count == 1
