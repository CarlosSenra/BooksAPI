from nest.core import Module, PyNestFactory
from .modules.usuario import UsuarioModule
from .modules.books import BooksModule
from .modules.categories import CategoriesModule
from .modules.health import HealthModule


@Module(imports=[UsuarioModule, BooksModule, CategoriesModule, HealthModule])
class AppModule:
    pass


app = PyNestFactory.create(
    AppModule,
    description="Esta é minha aplicação FastAPI com PyNest",
    title="Minha App",
    version="1.0.0",
    debug=True,
)

http_server = app.get_server()
