import bcrypt
import jwt
from datetime import datetime, timedelta
from app.core.settings import settings

def get_password_hash(password: str) -> str:
    """Gera o hash da senha usando bcrypt nativo."""
    # bcrypt exige que a senha seja convertida para bytes
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    
    # Retornamos como string (decode) para salvar no banco de dados (Postgres)
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compara a senha em texto plano com o hash do banco."""
    password_bytes = plain_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    
    return bcrypt.checkpw(password=password_bytes, hashed_password=hashed_password_bytes)

def create_access_token(data: dict) -> str:
    """Gera o token JWT."""
    to_encode = data.copy()
    expire = datetime.now() + timedelta(hours=settings.JWT_EXPIRES_IN_HOURS)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm="HS256")
    return encoded_jwt