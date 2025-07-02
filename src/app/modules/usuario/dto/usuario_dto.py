from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UsuarioCreate(BaseModel):
    """Objeto de Transferência de Dados para criação de um usuário"""

    email: EmailStr = Field(description="Email do usuário")
    username: str = Field(min_length=5, max_length=20, description="Nome de usuario")
    password: str = Field(min_length=8, max_length=20, description="Senha do usuário")
    nome: str = Field(min_length=3, max_length=50, description="Nome do usuário")


class UsuarioCreateResponse(BaseModel):
    """DTO para resposta da criação de um usuário"""

    id: int
    email: EmailStr
    username: str
    nome: str
    created_at: datetime
    updated_at: datetime
