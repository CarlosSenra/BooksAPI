import pandas as pd
from typing import List, Dict, Union

# from app.shared.database.models.books import Book
from app.shared.database.connection import get_db

session = next(get_db())


class CsvToDb:
    def __init__(self, csv_file: str):
        self.csv_file = csv_file
        self.df = pd.read_csv(self.csv_file)

    def convert_unit_price(self) -> None:
        """Converte o preço unitário para float"""
        try:
            self.df["price"] = self.df["price"].str.replace("Â£", "").astype(float)
            print(self.df.head())
        except Exception as e:
            print(f"Erro ao converter o preço unitário: {e}")

    def create_db(self):
        pass


if __name__ == "__main__":
    csv_to_db = CsvToDb("src/data/raw/books/Books_books.csv")
    csv_to_db.convert_unit_price()
