from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

# Importa a dependência que criamos no database.py
from app.db.database import get_db

router = APIRouter()


@router.get("/health", status_code=200)
async def health_check(db: AsyncSession = Depends(get_db)):
    """
    Verifica se a API está online e se consegue comunicar com o banco de dados assíncrono.
    """
    try:
        # Note o uso do 'await' aqui.
        # Ele avisa o Python para não travar a aplicação enquanto o banco responde.
        await db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        # Opcional: Em um cenário real, você usaria o logger aqui para registrar o erro 'e'
        db_status = "disconnected"

    return {"status": "ok", "database": db_status}
