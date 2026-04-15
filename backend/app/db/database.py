from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.settings import settings

# 1. Criação da Engine Assíncrona
# echo=True faz o SQLAlchemy "printar" no terminal todas as queries SQL executadas (ótimo para debug)
engine = create_async_engine(
    settings.POSTGRES_URI, 
    echo=settings.DEBUG,
    pool_size=settings.POOL_SIZE,
    max_overflow=settings.MAX_OVERFLOW,
    pool_recycle=settings.POOL_RECYCLE
)

# 2. Configuração da Sessão
# expire_on_commit=False é CRUCIAL em conexões assíncronas no SQLAlchemy.
# Sem isso, ao fazer o commit, ele tentaria fazer um "lazy load" síncrono para atualizar
# os dados do objeto, o que causaria um erro.
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Base para criar os modelos
Base = declarative_base()

# 3. Dependência do FastAPI
# Essa função será injetada nas rotas.
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()