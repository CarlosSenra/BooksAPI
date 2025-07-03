from nest.core import Injectable
from app.shared.database.connection import get_db
from app.shared.database.models.books import Books
from .dto.dto_categories import CategoryListResponse
from typing import List


@Injectable()
class CategoriesService:
    def __init__(self):
        self.db = next(get_db())

    def get_all_categories(self) -> List[CategoryListResponse]:
        rows = self.db.query(Books.category).distinct().all()
        return [CategoryListResponse(category=row.category) for row in rows]
