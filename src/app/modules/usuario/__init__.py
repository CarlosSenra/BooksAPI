from nest.core import Module
from .usuario_controller import UsuarioController
from .usuario_service import UsuarioService


@Module(controllers=[UsuarioController], providers=[UsuarioService])
class UsuarioModule:
    pass
