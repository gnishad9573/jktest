import ollama
from typing import Optional
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from models.book_model import Book
from schemas.generate_book_summary import  BookSummaryGenerate

class BookGenRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def generate_summary(self, BookSummary: BookSummaryGenerate) -> Book:
        if not BookSummary.content:
            raise HTTPException(status_code=400, detail="Book content cannot be empty")
        prompt = f"{BookSummary.content}"
        response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
        summary = response.get("message", {}).get("content", "Failed to generate summary")
        existing_book = await self.db.execute(select(Book).where(Book.title == BookSummary.title, Book.author == BookSummary.author))
        existing_book = existing_book.scalars().first()
        if existing_book:
            existing_book.summary = summary
            existing_book.genre = BookSummary.genre 
            existing_book.year_published = BookSummary.year_published
        else:
            new_book = Book(
            title=BookSummary.title,
            author=BookSummary.author,
            genre=BookSummary.genre,
            year_published=BookSummary.year_published,
            summary=summary)
            db_book = Book(**{k: v for k, v in new_book.__dict__.items() if k != "_sa_instance_state"})
            self.db.add(db_book)
        try:
            await self.db.commit()
            if existing_book:
                await self.db.refresh(existing_book)
                return existing_book
            else:
                await self.db.refresh(db_book)
                return db_book
        except SQLAlchemyError:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail="Database error occurred")