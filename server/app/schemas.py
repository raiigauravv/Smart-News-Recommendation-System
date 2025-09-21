from typing import List, Optional

from pydantic import BaseModel


class RecommendRequest(BaseModel):
    user_id: str
    k: Optional[int] = 10
    recent_clicks: Optional[List[str]] = None
    locale: Optional[str] = "en"
    algorithm: Optional[str] = "hybrid"  # "hybrid", "collaborative", "content", "bert"


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


class ExportPdfRequest(BaseModel):
    articles: List[RecItem]  # or a leaner schema; keep keys used in pdf_utils
    user_id: Optional[str] = "guest"  # Add user_id field with default
