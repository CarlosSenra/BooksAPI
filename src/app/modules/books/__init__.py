from nest.core import Module
from .books_controller import BooksController
from .books_service import BooksService


@Module(controllers=[BooksController], providers=[BooksService])
class BooksModule:
    pass
