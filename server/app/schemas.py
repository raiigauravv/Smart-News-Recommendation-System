from pydantic import BaseModel
from typing import List, Optional

class RecommendRequest(BaseModel):
    user_id: str
    k: Optional[int] = 10
    recent_clicks: Optional[List[str]] = None
    locale: Optional[str] = "en"

class RecItem(BaseModel):
    item_id: str
    score: float
    title: Optional[str] = None
    reason: Optional[str] = None

class RecommendResponse(BaseModel):
    user_id: str
    items: List[RecItem]

class SearchQuery(BaseModel):
    q: str
    k: Optional[int] = 20
    category: Optional[str] = None  # New: category filter

class SummarizeRequest(BaseModel):
    title: Optional[str] = None
    abstract: Optional[str] = None
    max_tokens: Optional[int] = 128