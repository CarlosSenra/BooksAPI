from tokenize import OP
from fastapi import Depends
from nest.core import Controller, Get
from typing import List, Optional
from app.modules.books.books_service import BooksService
from .dto.books_dto import (
    BookListResponse,
    BookResponse,
    BookNumberLimiter,
    BookRateLimiter,
)
from app.shared.config.config import API_PREFIX


@Controller(f"{API_PREFIX}/books")
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

    @Get("/top-rated")
    def get_top_rated_books(
        self,
        limit: BookNumberLimiter = Depends(),
        rate_min: BookRateLimiter = Depends(),
    ) -> List[BookResponse]:
        return self.books_service.book_top_rated(limit.limit, rate_min.rate_min)

    @Get("/price-range")
    def get_book_by_price(
        self, price_min: Optional[float] = None, price_max: Optional[float] = None
    ) -> List[BookResponse]:
        return self.books_service.book_filter_by_price(price_min, price_max)

    @Get("/{book_id}")
    def get_book_by_id(self, book_id: int) -> Optional[BookResponse]:
        return self.books_service.get_book_by_id(book_id)

    @Get("/search/title/{title}")
    def get_book_by_title(self, title: str) -> List[BookResponse]:
        return self.books_service.get_book_by_title_category(title=title)

    @Get("/search/category/{category}")
    def get_book_by_category(self, category: str) -> List[BookResponse]:
        return self.books_service.get_book_by_title_category(category=category)
