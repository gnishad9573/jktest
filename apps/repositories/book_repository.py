import ollama
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from models.book_model import Book
from schemas.book_schema import BookCreate, BookUpdate

class BookRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, book: BookCreate) -> Book:
        """Create a new book in the database"""
        db_book = Book(**book.model_dump())
        self.db.add(db_book)
        try:
            await self.db.commit()
            await self.db.refresh(db_book)
            return db_book
        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def get_by_id(self, book_id: int) -> Optional[Book]:
        """Get a book by its ID"""
        result = await self.db.execute(select(Book).filter(Book.id == book_id))
        return result.scalar_one_or_none()
    
    async def get_all_book(self) -> List[Book]:
        """Get a book all books"""
        result = await self.db.execute(select(Book))
        return result.scalars().all()

    async def update(self, book_id: int, book: BookUpdate) -> Optional[Book]:
        """Update an existing book"""
        db_book = await self.get_by_id(book_id)
        if not db_book:
            return None
        for key, value in book.model_dump(exclude_unset=True).items():
            setattr(db_book, key, value)
        try:
            await self.db.commit()
            await self.db.refresh(db_book)
            return db_book
        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def delete(self, book_id: int) -> bool:
        """Delete a book by its ID"""
        db_book = await self.get_by_id(book_id)
        if not db_book:
            return False
        try:
            await self.db.delete(db_book)
            await self.db.commit()
            return True
        except SQLAlchemyError:
            await self.db.rollback()
            raise
        
