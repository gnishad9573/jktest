from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.generate_book_summary import  BookSummaryGenerate
from schemas.book_schema import Book
from services.generate_summary import BookGeneService
from repositories.generate_summary import BookGenRepository
from models.users import User
from auth.dependencies import get_current_user
from database import get_db
from sqlalchemy.exc import SQLAlchemyError


router = APIRouter(prefix="/generate_summary", tags=["summary"])

async def get_book_service(db: AsyncSession = Depends(get_db)) -> BookGeneService:
    return BookGeneService(BookGenRepository(db))

@router.post("/", response_model=Book, status_code=201)
async def generate_summary(book: BookSummaryGenerate, service: BookGeneService = Depends(get_book_service), user: User = Depends(get_current_user)):
    """Generate the summary of the provided book"""
    try:
        return await service.create_summary(book)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=str(e))