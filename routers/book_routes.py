from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.book_schema import Book, BookCreate, BookUpdate
from services.book_service import BookService
from repositories.book_repository import BookRepository
from database import get_db
from models.users import User
from auth.dependencies import get_current_user
from typing import List
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(prefix="/books", tags=["books"])

async def get_book_service(db: AsyncSession = Depends(get_db)) -> BookService:
    return BookService(BookRepository(db))

@router.post("/", response_model=Book, status_code=201)
async def create_book(book: BookCreate, service: BookService = Depends(get_book_service), user: User = Depends(get_current_user)):
    """Create a new book"""
    try:
        return await service.create_book(book)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/", response_model=List[Book])
async def get_book(service: BookService = Depends(get_book_service), user: User = Depends(get_current_user)):
    """Getall book"""
    book = await service.get_book()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.get("/{id}", response_model=Book)
async def get_book_id(id: int, service: BookService = Depends(get_book_service), user: User = Depends(get_current_user)):
    """Get a specific book by ID"""
    book = await service.get_book_id(id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/{id}", response_model=Book)
async def update_book(id: int, book: BookUpdate, service: BookService = Depends(get_book_service), user: User = Depends(get_current_user)):
    """Update a book by ID"""
    updated_book = await service.update_book(id, book)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book

@router.delete("/{id}", response_model=dict)
async def delete_book(id: int, service: BookService = Depends(get_book_service), user: User = Depends(get_current_user)):
    """Delete a book by ID"""
    success = await service.delete_book(id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}




