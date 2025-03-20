from sqlalchemy import Column, Integer, String, Text
from db.base_class import Baseclass
from sqlalchemy.orm import relationship

class Book(Baseclass):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    genre = Column(String(100))
    year_published = Column(Integer)
    summary = Column(Text)
    reviews = relationship("Review", back_populates="book",  cascade="all, delete")