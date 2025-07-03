import pytest
from unittest.mock import Mock, patch, MagicMock

# Mock dos modelos SQLAlchemy
with patch.dict(
    "sys.modules",
    {
        "src.app.shared.database.models.books": MagicMock(),
        "src.app.shared.database.models.usuario": MagicMock(),
    },
):
    from src.app.modules.books.books_service import BooksService
    from src.app.modules.categories.categories_service import CategoriesService
    from src.app.modules.usuario.usuario_service import UsuarioService


@pytest.fixture
def mock_db():
    return Mock()


class TestBooksService:

    def test_get_all_books_in_stock(self, mock_db):
        with patch(
            "src.app.modules.books.books_service.get_db", return_value=iter([mock_db])
        ):
            service = BooksService()
            service.db = mock_db

            mock_db.query.return_value.filter.return_value.all.return_value = [
                Mock(title="Test Book")
            ]

            result = service.get_all_books_in_stock()

            assert len(result) == 1
            mock_db.query.assert_called_once()

    def test_get_book_by_id(self, mock_db):
        with patch(
            "src.app.modules.books.books_service.get_db", return_value=iter([mock_db])
        ):
            service = BooksService()
            service.db = mock_db

            mock_db.query.return_value.filter.return_value.first.return_value = (
                "Title",
                50.0,
                "In stock",
                4.0,
                "Category",
            )

            result = service.get_book_by_id(1)

            assert result is not None
            assert result.title == "Title"


class TestCategoriesService:

    def test_service_exists(self):
        with patch("src.app.modules.categories.categories_service.get_db"):
            service = CategoriesService()
            assert service is not None
