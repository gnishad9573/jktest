from fastapi import Depends, HTTPException
from schemas.review_schema import Review, ReviewCreate, ReviewSummary
from services.review_service import ReviewService
from repositories.review_repository import ReviewRepository
from repositories.book_repository import BookRepository
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db


async def get_review_service(db: AsyncSession = Depends(get_db)) -> ReviewService:
    """Dependency injection for review service"""
    return ReviewService(
        ReviewRepository(db),
        BookRepository(db)
    )


class ReviewController:
    def __init__(self, service: ReviewService):
        self.service = service

    async def create_review_c(self, book_id: int, review: ReviewCreate) -> Review:
        """Controller method to create a review"""
        try:
            return await self.service.create_review_s(book_id, review)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    async def get_book_reviews(self, book_id: int) -> list[Review]:
        """Controller method to get all reviews for a book"""
        book_exists = await self.service.book_repo.get_by_id(book_id)
        if not book_exists:
            raise HTTPException(status_code=404, detail="Book not found")

        reviews = await self.service.get_book_reviews(book_id)
        return reviews

    async def get_book_summary(self, book_id: int) -> ReviewSummary:
        """Controller method to get book summary with stats"""
        book_exists = await self.service.book_repo.get_by_id(book_id)
        if not book_exists:
            raise HTTPException(status_code=404, detail="Book not found")

        summary = await self.service.get_book_summary(book_id)
        if not summary or summary["review_count"] == 0:
            raise HTTPException(status_code=404, detail="No reviews available for this book")

        return ReviewSummary(review_count=summary["review_count"], average_rating=summary["average_rating"])
