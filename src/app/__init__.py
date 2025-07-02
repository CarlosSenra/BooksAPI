from nest.core import Module, PyNestFactory
from .modules.usuario import UsuarioModule


@Module(imports=[UsuarioModule])
class AppModule:
    pass


app = PyNestFactory.create(AppModule)
