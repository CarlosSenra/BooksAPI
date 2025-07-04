from pydantic import BaseModel


class HealthDto(BaseModel):
    status: str
    timestamp: str
    BooksTable: str
