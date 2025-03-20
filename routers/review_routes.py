
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.review_schema import Review, ReviewCreate, ReviewSummary
from controllers.review_controller import ReviewController
from services.review_service import ReviewService
from repositories.book_repository import BookRepository
from repositories.review_repository import ReviewRepository
from models.users import User
from auth.dependencies import get_current_user
from database import get_db
from typing import List

router = APIRouter(prefix="/books", tags=["reviews"])


async def get_review_controller(db: AsyncSession = Depends(get_db)) -> ReviewController:
    """Dependency injection for ReviewController"""
    review_service = ReviewService(
        ReviewRepository(db), 
        BookRepository(db) 
    )
    return ReviewController(review_service)

@router.post("/{id}/reviews", response_model=Review, status_code=201)
async def create_review(
    id: int,
    review: ReviewCreate,
    controller: ReviewController = Depends(get_review_controller),
    user: User = Depends(get_current_user)
):
    """Add a review for a book"""
    print("ganesh")
    created_review = await controller.create_review_c(id, review)
    print(created_review)
    if not created_review:
        raise HTTPException(status_code=404, detail="Book not found")
    return created_review

@router.get("/{id}/reviews", response_model=List[Review])
async def get_book_reviews(
    id: int,
    controller: ReviewController = Depends(get_review_controller),
    user: User = Depends(get_current_user)
):
    """Retrieve all reviews for a book"""
    reviews = await controller.get_book_reviews(id)
    if not reviews:
        raise HTTPException(status_code=404, detail="Book not found or no reviews found")
    return reviews

@router.get("/{id}/summary", response_model=ReviewSummary)
async def get_book_summary(
    id: int,
    controller: ReviewController = Depends(get_review_controller),
    user: User = Depends(get_current_user)
):
    """Get summary and aggregated rating for a book"""
    summary = await controller.get_book_summary(id)
    if not summary:
        raise HTTPException(status_code=404, detail="Book not found or no reviews available")
    return summary
