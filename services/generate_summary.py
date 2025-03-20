from schemas.generate_book_summary import BookSummaryGenerate
from repositories.generate_summary import BookGenRepository
from typing import Optional

class BookGeneService:
    def __init__(self, book_repo: BookGenRepository):
        self.book_repo = book_repo

    async def create_summary(self, book: BookSummaryGenerate):
        """Create a new book"""
        return await self.book_repo.generate_summary(book)