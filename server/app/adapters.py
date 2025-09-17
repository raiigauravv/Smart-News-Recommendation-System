from typing import List, Dict, Any, Optional
from utils import recommenders as R
from utils import pdf_utils as PDF

def _ensure_loaded():
    try:
        R.load_mind_data()
    except Exception:
        pass

def get_trending(k: int = 20) -> List[Dict[str, Any]]:
    _ensure_loaded()
    return R.get_trending_articles(k=k)

def recommend(user_id: str, k: int = 10, recent_clicks: Optional[list] = None, locale: str = "en") -> List[Dict[str, Any]]:
    _ensure_loaded()
    return R.recommend_for_user(user_id=user_id, k=k, recent_clicks=recent_clicks, locale=locale)

def keyword_search(q: str, k: int = 20) -> List[Dict[str, Any]]:
    _ensure_loaded()
    return R.search_by_keywords(q=q, k=k)

def export_pdf(articles: List[Dict[str, Any]]) -> str:
    """Return an absolute/relative file path to the generated PDF."""
    return PDF.generate_pdf_from_articles(articles)
