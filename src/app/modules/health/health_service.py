from nest.core import Injectable
from datetime import datetime
from shared.database.connection import get_db
from models.books import Books
from .dto.health_dto import HealthDto

session = next(get_db())


@Injectable()
class HealthService:
    def __init__(self):
        self.session = session

    def get_health(self) -> HealthDto:
        books = self.session.query(Books).count()
        return HealthDto(
            status="ok",
            timestamp=f"{datetime.now().isoformat()}",
            BooksTable=f"{str(books)} books",
        )
