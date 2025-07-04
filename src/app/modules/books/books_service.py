from nest.core import Injectable
from typing import List, Optional, Tuple
from sqlalchemy import or_
from sqlalchemy.engine import Row
from shared.database.connection import get_db, engine
from models.books import Books
from .dto.books_dto import BookListResponse, BookResponse


@Injectable()
class BooksService:
    def __init__(self):
        self.db = next(get_db())

    def get_all_books_in_stock(self) -> List[BookListResponse]:
        rows = self.db.query(Books.title).filter(Books.availability == "In stock").all()
        return [BookListResponse(title=row.title) for row in rows]

    def get_book_by_id(self, book_id: int) -> Optional[BookResponse]:
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
