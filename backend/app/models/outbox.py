from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, Boolean, func, Enum as SqlEnum
from sqlalchemy.dialects.postgresql import JSONB
from app.db.database import Base


class EventType(str, Enum):
    BOOKING_CREATED = "Reserva Criada"
    BOOKING_UPDATED = "Reserva Atualizada"
    BOOKING_CANCELED = "Reserva Cancelada"


class OutboxEvent(Base):
    __tablename__ = "outbox_events"

    id = Column(Integer, primary_key=True, index=True)

    # Tipo do evento (enumeração acima)
    event_type = Column(String(50), SqlEnum(EventType), nullable=False)

    # Payload contém os dados essenciais (ex: {"booking_id": 1, "room_name": "Sala A", "start_at": "..."})
    payload = Column(JSONB, nullable=False)

    # Controle do Worker
    processed = Column(Boolean, default=False, nullable=False, index=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Bônus Sênior: Controle de tentativas e log de erro em caso de falha no envio do e-mail
    retries = Column(Integer, default=0, nullable=False)
    error_message = Column(String, nullable=True)
