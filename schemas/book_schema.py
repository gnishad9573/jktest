from pydantic import BaseModel, ConfigDict
from typing import Optional

class BookBase(BaseModel):
    title: str
    author: str
    genre: Optional[str] = None
    year_published: Optional[int] = None
    summary: Optional[str] = None

class BookCreate(BookBase):
    """Schema for creating a new book"""
    pass


class BookUpdate(BaseModel):
    """Schema for updating an existing book (allows partial updates)"""
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    year_published: Optional[int] = None
    summary: Optional[str] = None

class Book(BookBase):
    """Schema representing a book with an ID"""
    id: int
    model_config = ConfigDict(from_attributes=True)
