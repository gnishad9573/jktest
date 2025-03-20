from pydantic import BaseModel, ConfigDict, conint
from typing import Optional  

class ReviewBase(BaseModel):
    review_text: str
    rating: conint(ge=1, le=5) 
    user_id: int

class ReviewCreate(ReviewBase):
    """Schema for creating a review"""
    pass

class Review(ReviewBase):
    """Schema representing a review with an ID and book association"""
    id: int
    book_id: int

    model_config = ConfigDict(from_attributes=True)


class ReviewSummary(BaseModel):
    """Schema for summarizing reviews of a book"""
    summary: Optional[str] = None
    review_count: int
    average_rating: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)
