import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_criar_reserva_sem_token_retorna_401():
    """Requisito: Permissões - Acesso negado sem token"""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        payload = {
            "title": "Reunião Secreta",
            "roomId": 1,
            "startAt": "2026-04-16T10:00:00Z",
            "endAt": "2026-04-16T11:00:00Z",
            "participants": ["teste@teste.com"],
        }
        response = await client.post("/mailerweb/v1/bookings/", json=payload)

        assert response.status_code == 401
        assert response.json()["detail"] == "Not authenticated"
