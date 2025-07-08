from pydantic import BaseModel, Field
from typing import Optional


class BookResponse(BaseModel):
    title: str
    price: Optional[float] = None
    availability: Optional[str] = None
    rating: Optional[int] = None
    category: Optional[str] = None


class BookListResponse(BaseModel):
    title: str


class BookNumberLimiter(BaseModel):
    limit: int = Field(..., ge=1, le=50, description="Número de livros (entre 1 e 50)")


class BookRateLimiter(BaseModel):
    rate_min: float = Field(..., ge=0, le=5, description="Nota mínima (entre 0 e 5)")
