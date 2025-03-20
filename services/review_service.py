from schemas.review_schema import ReviewCreate
from models.review_model import Review
from repositories.review_repository import ReviewRepository
from repositories.book_repository import BookRepository
from typing import List, Dict, Optional

class ReviewService:
    def __init__(self, review_repo: ReviewRepository, book_repo: BookRepository):
        self.review_repo = review_repo
        self.book_repo = book_repo

    async def create_review_s(self, book_id: int, review: ReviewCreate) -> Review:
        """Create a new review for a book"""
        # Verify book exists
        book = await self.book_repo.get_by_id(book_id)
        print(book)
        if not book:
            raise ValueError("Book not found")
        return await self.review_repo.create(book_id, review)

    async def get_book_reviews(self, book_id: int) -> List[Review]:
        """Get all reviews for a book"""
        book = await self.book_repo.get_by_id(book_id)
        if not book:
            raise ValueError("Book not found")
        return await self.review_repo.get_by_book_id(book_id)

    async def get_book_summary(self, book_id: int) -> Dict[str, Optional[float]]:
        """Get book summary with aggregated rating"""
        book = await self.book_repo.get_by_id(book_id)
        if not book:
            raise ValueError("Book not found")
        
        review_count, avg_rating = await self.review_repo.get_summary_stats(book_id)
        return {
            "summary": book.summary,
            "review_count": review_count if review_count is not None else 0,
            "average_rating": float(avg_rating) if avg_rating is not None else None
        }
