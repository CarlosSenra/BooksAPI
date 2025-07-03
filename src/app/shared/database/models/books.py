from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from app.shared.database.base import Base


class Books(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    price = Column(Float)
    availability = Column(String(100))
    rating = Column(Integer)
    image_url = Column(String(500))
    link = Column(String(500))
    category = Column(String(100))
