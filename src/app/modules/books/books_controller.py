from tokenize import OP
from nest.core import Controller, Get
from typing import List, Optional
from app.modules.books.books_service import BooksService
from .dto.books_dto import BookListResponse, BookResponse


@Controller("/api/v1/books")
class BooksController:
    def __init__(self, books_service: BooksService):
        self.books_service = books_service

    @Get("/")
    def get_all_books(self) -> List[BookListResponse]:
        return self.books_service.get_all_books_in_stock()

    @Get("/search")
    def get_book_by_title_category(
        self, title: str, category: str
    ) -> List[BookResponse]:
        return self.books_service.get_book_by_title_category(title, category)

    @Get("/{book_id}")
    def get_book_by_id(self, book_id: int) -> Optional[BookResponse]:
        return self.books_service.get_book_by_id(book_id)

    @Get("/search/title/{title}")
    def get_book_by_title(self, title: str) -> List[BookResponse]:
        return self.books_service.get_book_by_title_category(title=title)

    @Get("/search/category/{category}")
    def get_book_by_category(self, category: str) -> List[BookResponse]:
        return self.books_service.get_book_by_title_category(category=category)
