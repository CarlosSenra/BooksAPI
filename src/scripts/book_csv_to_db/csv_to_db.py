import pandas as pd
from app.shared.database.models.books import Books
from sqlalchemy.orm import Session

from app.shared.database.connection import get_db, engine
from app.shared.database.base import Base

Base.metadata.create_all(engine)
session = next(get_db())


class CsvToDb:
    def __init__(self, csv_file: str, session: Session):
        self.csv_file = csv_file
        self.session = session
        self.df = pd.read_csv(self.csv_file)

    def convert_unit_price(self) -> None:
        """Converte o preço unitário para float"""
        try:
            self.df["price"] = self.df["price"].str.replace("Â£", "").astype(float)
            print(self.df.head())
        except Exception as e:
            print(f"Erro ao converter o preço unitário: {e}")

    def convert_to_db(self) -> None:
        """converte o df para um modelo de DB"""
        self.convert_unit_price()
        for _, row in self.df.iterrows():
            existing_book = (
                self.session.query(Books)
                .filter(Books.title == row["title"], Books.category == row["category"])
                .first()
            )

            if not existing_book:
                book = Books(
                    title=row["title"],
                    price=row["price"],
                    availability=row["availability"],
                    rating=row["rating"],
                    image_url=row["image_url"],
                    link=row["link"],
                    category=row["category"],
                )
                self.session.add(book)
                self.session.commit()
                self.session.refresh(book)
                print(f"Livro inserido: {row['title']}")
            else:
                self.session.rollback()
                print(f"Livro já existe: {row['title']}")

        self.session.close()


if __name__ == "__main__":
    csv_to_db = CsvToDb("src/data/raw/books/books.csv", session=session)
    csv_to_db.convert_to_db()
