
from schemas.book_schema import BookCreate, BookUpdate
from repositories.book_repository import BookRepository
from typing import Optional

class BookService:
    def __init__(self, book_repo: BookRepository):
        self.book_repo = book_repo

    async def create_book(self, book: BookCreate):
        """Create a new book"""
        return await self.book_repo.create(book)

    async def get_book_id(self, book_id: int):
        """Retrieve a book by ID"""
        book = await self.book_repo.get_by_id(book_id)
        if not book:
            raise ValueError("Book not found")
        return book
    
    async def get_book(self):
        """Retrieve a book by ID"""
        book = await self.book_repo.get_all_book()
        if not book:
            raise ValueError("No Book present is to the DB currently not")
        return book

    async def update_book(self, book_id: int, book: BookUpdate):
        """Update an existing book"""
        updated_book = await self.book_repo.update(book_id, book)
        if not updated_book:
            raise ValueError("Book not found")
        return updated_book

    async def delete_book(self, book_id: int) -> bool:
        """Delete a book"""
        success = await self.book_repo.delete(book_id)
        if not success:
            raise ValueError("Book not found")
        return success
    
