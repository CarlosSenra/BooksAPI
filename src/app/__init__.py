from nest.core import Module, PyNestFactory
from .modules.usuario import UsuarioModule
from .modules.books import BooksModule
from .modules.categories import CategoriesModule


@Module(imports=[UsuarioModule, BooksModule, CategoriesModule])
class AppModule:
    pass


app = PyNestFactory.create(
    AppModule,
    description="Esta é minha aplicação FastAPI com PyNest",
    title="Minha App",
    version="1.0.0",
    debug=True,
)

# Esta é a linha crucial - get_server() retorna a instância FastAPI
http_server = app.get_server()
