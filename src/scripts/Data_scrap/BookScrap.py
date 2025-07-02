import requests
from bs4 import BeautifulSoup, Tag
import pandas as pd
import time
import logging
from typing import List, Dict, Union
from urllib.parse import urljoin

# Configuração de logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("BookScraping")


class BookScraper:
    """Web scraper completo para https://books.toscrape.com/"""

    def __init__(self):
        self.base_url = "https://books.toscrape.com/"
        self.session = requests.Session()
        self.books_data = []

    def get_page(self, url: str) -> Union[BeautifulSoup, None]:
        """Faz requisição e retorna BeautifulSoup object"""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except Exception as e:
            logger.error(f"Erro ao acessar {url}: {e}")
            return None

    def get_categories(self) -> Dict[str, str]:
        """Extrai todas as categorias de livros"""
        soup = self.get_page(self.base_url)
        if not soup:
            return {}

        categories = {}
        sidebar = soup.find("div", class_="side_categories")
        logger.debug(f"A side bar é {sidebar}")
        if sidebar and isinstance(sidebar, Tag):
            links = sidebar.find_all("a", href=True)
            logger.debug(f"Tem {len(links)}, exemplo : {links[5]}")
            for link in links:
                if isinstance(link, Tag):
                    href = link.get("href")
                    if href and isinstance(href, str) and "catalogue/category" in href:
                        category_name = link.text.strip()
                        category_url = urljoin(self.base_url, href)
                    categories[category_name] = category_url

        logger.info(f"Encontradas {len(categories)} categorias")
        return categories

    def extract_book_info(self, book_element) -> Dict:
        """Extrai informações de um livro"""
        book_data = {}

        # Título
        title_element = book_element.find("h3").find("a")
        book_data["title"] = title_element.get("title", "") if title_element else ""

        # Preço
        price_element = book_element.find("p", class_="price_color")
        book_data["price"] = price_element.text.strip() if price_element else ""

        # Disponibilidade
        stock_element = book_element.find("p", class_="instock availability")
        book_data["availability"] = stock_element.text.strip() if stock_element else ""

        # Rating (estrelas)
        rating_element = book_element.find("p", class_="star-rating")
        if rating_element:
            rating_classes = rating_element.get("class", [])
            rating_words = ["Zero", "One", "Two", "Three", "Four", "Five"]
            for word in rating_words:
                if word in rating_classes:
                    book_data["rating"] = rating_words.index(word)
                    break
        else:
            book_data["rating"] = 0

        # Imagem do livro
        image_element = book_element.find("div", class_="image_container").find("img")
        if image_element:
            image_src = image_element.get("src", "")
            book_data["image_url"] = urljoin(self.base_url, image_src)
        else:
            book_data["image_url"] = ""

        # Link do livro
        if title_element:
            book_data["link"] = urljoin(self.base_url, title_element.get("href", ""))

        return book_data

    def get_books_from_page(self, page_url: str) -> List[Dict]:
        """Extrai todos os livros de uma página"""
        soup = self.get_page(page_url)
        if not soup:
            return []

        books = []
        book_elements = soup.find_all("article", class_="product_pod")

        for book_element in book_elements:
            book_info = self.extract_book_info(book_element)
            if book_info["title"]:  # Só adiciona se tiver título
                books.append(book_info)

        return books

    def get_all_pages_from_category(self, category_url: str) -> List[Dict]:
        """Percorre todas as páginas de uma categoria"""
        all_books = []
        current_url = category_url
        page_num = 1

        while current_url:
            logger.info(f"Processando página {page_num} - {current_url}")

            books = self.get_books_from_page(current_url)
            all_books.extend(books)

            # Verifica se há próxima página
            soup = self.get_page(current_url)
            if soup:
                next_link = soup.find("li", class_="next")
                logger.debug(f"pagina {page_num} : {next_link}")
                if next_link and isinstance(next_link, Tag) and next_link.find("a"):
                    next_a = next_link.find("a")
                    if isinstance(next_a, Tag):
                        next_url = next_a.get("href")
                        if next_url and isinstance(next_url, str):
                            current_url = urljoin(current_url, next_url)
                    page_num += 1
                else:
                    current_url = None
            else:
                break

            time.sleep(0.5)

        return all_books

    def scrape_category(self, category_name: str, category_url: str) -> List[Dict]:
        """Faz scraping de uma categoria específica"""
        logger.info(f"Iniciando scraping da categoria: {category_name}")

        books = self.get_all_pages_from_category(category_url)

        for book in books:
            book["category"] = category_name

        logger.info(f"Categoria {category_name}: {len(books)} livros encontrados")
        return books


def main():
    """Função principal para executar o scraping"""
    scraper = BookScraper()

    categories = scraper.get_categories()
    print("Categorias disponíveis:")
    for i, (name, url) in enumerate(categories.items(), 1):
        print(f"{i}. {name}")

    if categories:
        first_category = list(categories.items())[0]
        logger.debug(first_category)
        sample_books = scraper.scrape_category(first_category[0], first_category[1])

        df_sample = pd.DataFrame(sample_books)
        print(f"\nAmostra da categoria '{first_category[0]}':")
        print(df_sample.head())

        df_sample.to_csv(
            f"src/data/raw/books/{first_category[0]}_books.csv",
            index=False,
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
