from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # --- Configurações Gerais ---
    PRODUCTION: bool = False
    DEBUG: bool = True
    SERVICE_NAME: str = "mailerweb"
    
    PREFIX: str = f"/{SERVICE_NAME}/v1"

    # O valor default está configurado para o serviço 'db' do docker-compose
    POSTGRES_URI: str = "postgresql+asyncpg://mailer_user:mailer_pass@db:5432/mailerweb_db"
    
    # --- Segurança e Autenticação (JWT) ---
    # Em produção, o GitHub Secrets deve sobrescrever esta chave
    JWT_SECRET: str = "969824a6-93e4-11eb-8da1-51115a0d4746"
    JWT_EXPIRES_IN_HOURS: int = 24

    # --- Configurações de Pool (SQLAlchemy) ---
    POOL_SIZE: int = 5
    MAX_OVERFLOW: int = 10
    POOL_RECYCLE: int = 30

    # --- Configurações de SMTP ---
    # Em outros ambientes, o GitHub Secrets devem sobrescrever estas configurações
    SMTP_HOST: str = "sandbox.smtp.mailtrap.io"
    SMTP_PORT: int = 2525
    SMTP_USER: str = "1ba06f6f4f7ddc"
    SMTP_PASSWORD: str = "bc42b76c685bce"
    FROM_EMAIL: str = "noreply@mailerweb.com"

    # --- Configuração do Pydantic Settings ---
    # Prioridade: Variáveis de Ambiente do Sistema (GitHub Secrets) > Arquivo .env > Default no código
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"  # Ignora variáveis extras
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()