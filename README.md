# Meu Projeto de API de Livros

## Descrição

API para consulta, cadastro e gerenciamento de informações de livros, usuários e categorias. Os dados dos livros são obtidos via web scraping do site [Books to Scrape](https://books.toscrape.com/) e armazenados em um banco SQLite.

---

## Stack Utilizada

- **Python 3.12+**
- **[PyNest](https://github.com/luizalabs/pynest)** (estrutura inspirada no NestJS)
- **FastAPI** (via PyNest)
- **SQLAlchemy** (ORM)
- **Pydantic** (validação de dados)
- **Uvicorn** (ASGI server)
- **SQLite** (banco de dados local)

---

## Como rodar o projeto

1. **Instale as dependências**  
   Recomendado usar o Poetry:
   ```bash
   poetry install
   ```

2. **Execute as migrações/crie o banco**  
   O banco SQLite será criado automaticamente ao rodar a aplicação.

3. **Rode o servidor**
   ```bash
   poetry run python src/app/main.py
   ```
   Ou diretamente com Uvicorn:
   ```bash
   poetry run uvicorn src.app:app --reload
   ```

4. **Acesse a documentação automática**  
   - [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Endpoints Principais

### Livros (`/api/v1/books`)
- `GET /api/v1/books/`  
  Lista todos os livros em estoque.
- `GET /api/v1/books/{book_id}`  
  Detalhes de um livro por ID.
- `GET /api/v1/books/search?title={title}&category={category}`  
  Busca livros por título **ou** categoria (parâmetros opcionais).
- `GET /api/v1/books/search/title/{title}`  
  Busca livros pelo título.
- `GET /api/v1/books/search/category/{category}`  
  Busca livros pela categoria.

### Categorias (`/api/v1/categories`)
- `GET /api/v1/categories/`  
  Lista todas as categorias disponíveis.

### Usuários (`/api/v1/usuario`)
- `POST /api/v1/usuario/create`  
  Cria um novo usuário.

---

## Banco de Dados

- **SQLite**: arquivo `app.db` na raiz do projeto.
- Modelos principais: `Books`, `Usuario`.

---

## Scripts Úteis

- `src/scripts/Data_scrap/BookScrap.py`: realiza o scraping dos livros e salva em `data/raw/books/books.csv`.
- `src/scripts/book_csv_to_db/csv_to_db.py`: importa os dados do CSV para o banco de dados.

---

## Estrutura de Pastas

```
src/
  app/
    modules/
      books/         # Lógica e endpoints de livros
      usuario/       # Lógica e endpoints de usuários
      categories/    # Lógica e endpoints de categorias
    shared/
      database/      # Conexão, modelos e base do banco
  data/
    raw/books/       # Dados brutos dos livros (CSV)
  scripts/           # Scripts de scraping e importação
```

---

## Testes

- Testes unitários em `tests/` utilizando `pytest`.

---

## Observações

*Scripts*:
    - Data_scrap/BookScrap - é onde ocorre o scrap da informações dos livrom de https://books.toscrape.com/ que salva os dados em data/raw/books