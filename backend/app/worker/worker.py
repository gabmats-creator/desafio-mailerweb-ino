import asyncio
import logging
from sqlalchemy import select
from email.message import EmailMessage
import aiosmtplib

from app.db.database import get_db
from app.models.outbox import OutboxEvent
from app.core.settings import settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

async def send_real_email(to_emails: list[str], subject: str, body_content: str):
    """Monta e dispara o e-mail via SMTP de forma assíncrona."""
    message = EmailMessage()
    message["From"] = settings.FROM_EMAIL
    message["To"] = ", ".join(to_emails)
    message["Subject"] = subject
    message.set_content(body_content)

    # Disparo assíncrono
    await aiosmtplib.send(
        message,
        hostname=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
        username=settings.SMTP_USER,
        password=settings.SMTP_PASSWORD,
        use_tls=False, # Mude para True se usar o Gmail (porta 465)
        start_tls=True if settings.SMTP_PORT == 587 else False
    )

def _build_email_content(event_type: str, payload: dict) -> tuple[str, str]:
    """Cria o assunto e o corpo do e-mail com base no evento."""
    room_name = payload.get("room_name", "Sala")
    title = payload.get("title", "Reunião")
    start = payload.get("start_at", "")
    
    if event_type == "BOOKING_CREATED":
        subject = f"📅 Nova Reserva Confirmada: {title}"
        body = f"Olá!\n\nUma nova reserva foi criada para você.\nSala: {room_name}\nData/Hora: {start}\n\nAté logo!"
    elif event_type == "BOOKING_CANCELED":
        subject = f"❌ Reserva Cancelada: {title}"
        body = f"Olá,\n\nA reserva na sala '{room_name}' programada para {start} foi cancelada."
    else:
        subject = f"🔄 Reserva Atualizada: {title}"
        body = f"Olá,\n\nA reserva '{title}' sofreu alterações de horário ou sala."
        
    return subject, body

async def process_outbox_events():
    logger.info("Iniciando Worker de E-mails REAIS (Outbox)...")
    
    while True:
        async for db in get_db():
            try:
                query = select(OutboxEvent).where(OutboxEvent.processed == False).limit(50)
                events = (await db.execute(query)).scalars().all()

                for event in events:
                    payload = event.payload
                    participants = payload.get("participants", [])
                    
                    if not participants:
                        logger.warning(f"Evento {event.id} sem participantes. Ignorando envio.")
                        event.processed = True
                        continue

                    # Gera o texto do e-mail
                    event_type_str = event.event_type if isinstance(event.event_type, str) else event.event_type.name
                    subject, body = _build_email_content(event_type_str, payload)
                    
                    logger.info(f"📧 Disparando e-mail SMTP para: {participants}...")
                    
                    try:
                        # Chama a função que bate no servidor de e-mail real!
                        await send_real_email(participants, subject, body)
                        event.processed = True
                        logger.info(f"✅ E-mail enviado e Evento {event.id} processado!")
                    except Exception as email_err:
                        # Se o envio falhar (ex: sem internet), ele não marca como processado 
                        # para tentar de novo no próximo loop! (Padrão Resiliência)
                        logger.error(f"Falha ao enviar e-mail via SMTP do evento {event.id}: {email_err}")

                if events:
                    await db.commit()

            except Exception as e:
                logger.error(f"Erro no banco de dados do Worker: {e}")
                await db.rollback()

        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(process_outbox_events())