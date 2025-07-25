from nest.core import Controller, Post, Depends
from .usuario_service import UsuarioService
from .dto.usuario_dto import UsuarioCreate, UsuarioCreateResponse
from sqlalchemy.orm import Session
from shared.database.connection import get_db
from app.shared.config.config import API_PREFIX


@Controller(f"{API_PREFIX}/usuario")
class UsuarioController:
    def __init__(self, service: UsuarioService):
        self.service = service

    @Post("/create")
    def create_user(
        self, usuario: UsuarioCreate, db: Session = Depends(get_db)
    ) -> UsuarioCreateResponse:
        """Cria um novo usuário"""
        return self.service.create_user(db, usuario)
