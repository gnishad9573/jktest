from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models.book_model import Book
from models.review_model import Review
from database import get_db
from repositories.book_recommendetion_repository import BookRecommendetion
from services.book_recommendetion_service import BookRecommendetionService
from auth.dependencies import get_current_user
from typing import List
from sqlalchemy.exc import SQLAlchemyError


router = APIRouter(prefix="/recommendations", tags=["/recommendations"])

async def get_recommendetion_service(db: AsyncSession = Depends(get_db)) -> BookRecommendetionService:
    return BookRecommendetionService(BookRecommendetion(db))

@router.get("/{user_id}", response_model= None )
async def get_book_recommendetion(user_id: int, service: BookRecommendetionService = Depends(get_recommendetion_service)):
    recommendede_book_list = await service.get_book_recommendetion(user_id)
    if not recommendede_book_list:
        raise HTTPException(status_code=404, detail="Book not found")
    return recommendede_book_list