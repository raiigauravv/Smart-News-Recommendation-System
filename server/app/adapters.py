from typing import List, Dict, Any, Optional
from utils import recommenders as R
from utils import pdf_utils as PDF

def _ensure_loaded():
    try:
        R._ensure_data_loaded()
    except Exception:
        pass

def get_trending(k: int = 20) -> List[Dict[str, Any]]:
    _ensure_loaded()
    return R.get_trending_articles(k=k)

def recommend(user_id: str, k: int = 10, recent_clicks: Optional[list] = None, locale: str = "en", algorithm: str = "hybrid") -> List[Dict[str, Any]]:
    _ensure_loaded()
    return R.recommend_for_user(user_id=user_id, k=k, recent_clicks=recent_clicks, locale=locale, algorithm=algorithm)

def keyword_search(q: str, k: int = 20, category: Optional[str] = None) -> List[Dict[str, Any]]:
    _ensure_loaded()
    return R.search_by_keywords(q=q, k=k, category=category)

def export_pdf(articles: List[Dict[str, Any]], user_id: str = "guest") -> str:
    """Return an absolute/relative file path to the generated PDF."""
    # Extract item IDs from the RecItem objects
    news_ids = [article.get('item_id') for article in articles if article.get('item_id')]
    
    # Get full article details for PDF generation
    full_articles = R.get_article_details(news_ids)
    
    return PDF.generate_pdf_from_articles(full_articles, user_id)
