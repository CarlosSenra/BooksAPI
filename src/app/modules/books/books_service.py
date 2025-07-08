from nest.core import Injectable
from typing import List, Optional, Tuple
from sqlalchemy import or_
from sqlalchemy.engine import Row
from shared.database.connection import get_db, engine
from models.books import Books
from .dto.books_dto import (
    BookListResponse,
    BookResponse,
    BookNumberLimiter,
    BookRateLimiter,
)
from fastapi import HTTPException


@Injectable()
class BooksService:
    def __init__(self):
        self.db = next(get_db())

    def get_all_books_in_stock(self) -> List[BookListResponse]:
        """
        Get all books in stock
        """
        rows = self.db.query(Books.title).filter(Books.availability == "In stock").all()
        return [BookListResponse(title=row.title) for row in rows]

    def get_book_by_id(self, book_id: int) -> Optional[BookResponse]:
        """
        Get a book by its ID
        """
        row = (
            self.db.query(
                Books.title,
                Books.price,
                Books.availability,
                Books.rating,
                Books.category,
            )
            .filter(Books.id == book_id)
            .first()
        )

        if row is None:
            return None

        return BookResponse(
            title=row[0],
            price=row[1],
            availability=row[2],
            rating=row[3],
            category=row[4],
        )

    def get_book_by_title_category(
        self, title: Optional[str] = None, category: Optional[str] = None
    ):
        """
        Get a book by its title and category
        """
        query = self.db.query(
            Books.title, Books.price, Books.availability, Books.rating, Books.category
        )
        filters = []
        if title:
            filters.append(Books.title.ilike(f"%{title.strip()}%"))
        if category:
            filters.append(Books.category.ilike(f"%{category.strip()}%"))
        if filters:
            query = query.filter(or_(*filters))
        rows = query.all()

        return [
            BookResponse(
                title=row[0],
                price=row[1],
                availability=row[2],
                rating=row[3],
                category=row[4],
            )
            for row in rows
        ]

    def book_top_rated(self, limit: int, rate_min: float) -> List[BookResponse]:
        """
        Get the top rated books
        """
        try:
            query = self.db.query(
                Books.title,
                Books.price,
                Books.availability,
                Books.rating,
                Books.category,
            )

            if rate_min is not None:
                query = query.filter(Books.rating >= rate_min)

            query = query.order_by(Books.rating.desc())

            if limit is not None:
                query = query.limit(limit)

            rows = query.all()

            return [
                BookResponse(
                    title=row[0],
                    price=row[1],
                    availability=row[2],
                    rating=row[3],
                    category=row[4],
                )
                for row in rows
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def book_filter_by_price(
        self, price_min: Optional[float] = None, price_max: Optional[float] = None
    ) -> List[BookResponse]:
        query = self.db.query(
            Books.title, Books.price, Books.availability, Books.rating, Books.category
        )
        if price_min is None and price_max is not None:
            rows = query.filter(Books.price <= price_max)
        elif price_min is not None and price_max is None:
            rows = query.filter(Books.price >= price_min)
        elif price_min is not None and price_max is not None:
            rows = query.filter(Books.price >= price_min, Books.price <= price_max)
        rows = rows.order_by(Books.price.desc()).all()
        return [
            BookResponse(
                title=row[0],
                price=row[1],
                availability=row[2],
                rating=row[3],
                category=row[4],
            )
            for row in rows
        ]
