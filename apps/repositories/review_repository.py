
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from models.review_model import Review
from schemas.review_schema import ReviewCreate
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional

class ReviewRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, book_id: int, review: ReviewCreate) -> Review:
        """Create a new review for a book"""
        db_review = Review(book_id=book_id, **review.model_dump())
        self.db.add(db_review)
        try:
            await self.db.commit()
            await self.db.refresh(db_review)
            return db_review
        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def get_by_book_id(self, book_id: int) -> list[Review]:
        """Get all reviews for a specific book"""
        result = await self.db.execute(select(Review).filter(Review.book_id == book_id))
        return result.scalars().all()

    async def get_summary_stats(self, book_id: int) -> tuple[int, Optional[float]]:
        """Get count and average rating for a book's reviews"""
        result = await self.db.execute(
            select(func.count(Review.id), func.avg(Review.rating))
            .filter(Review.book_id == book_id)
        )
        count, avg_rating = result.first() or (0, None)  # Handle empty results safely
        return count, avg_rating

