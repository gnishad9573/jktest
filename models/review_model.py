from sqlalchemy import Column, Integer, String, Text, ForeignKey, CheckConstraint
from db.base_class import Baseclass
from sqlalchemy.orm import relationship

class Review(Baseclass):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, nullable=False)
    review_text = Column(Text, nullable=False)
    rating = Column(Integer, CheckConstraint('rating >= 1 AND rating <= 5'))
    book = relationship("Book", back_populates="reviews")