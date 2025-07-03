from pydantic import BaseModel
from typing import Optional


class BookResponse(BaseModel):
    title: str
    price: Optional[float] = None
    availability: Optional[str] = None
    rating: Optional[int] = None
    category: Optional[str] = None


class BookListResponse(BaseModel):
    title: str
