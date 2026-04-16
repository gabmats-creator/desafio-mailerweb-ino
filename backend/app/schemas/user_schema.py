from pydantic import EmailStr, ConfigDict, Field
from typing import Optional
from app.schemas.base import BaseDTO

class UserBase(BaseDTO):
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="A senha deve ter no mínimo 6 caracteres.")

class UserUpdate(BaseDTO):
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)

class TokenResponse(BaseDTO):
    access_token: str
    token_type: str = "bearer"

class UserResponse(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)