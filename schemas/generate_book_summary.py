from pydantic import BaseModel, ConfigDict
from typing import Optional

class BookRequest(BaseModel):
    title: str
    author: str
    genre: str
    year_published: int
    content: str

class BookSummaryGenerate(BookRequest):
    pass
