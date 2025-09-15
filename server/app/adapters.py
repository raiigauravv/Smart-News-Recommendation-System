from typing import List, Dict, Any, Optional
import sys
import os

# Add the parent directory to sys.path to import utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from utils import recommenders as R
from utils import pdf_utils as PDF

# Ensure lazy load used by your recommenders
def ensure_data():
    # your recommenders.py already lazy-loads; call a safe function here if needed
    return True

def get_trending(k: int = 20) -> List[Dict[str, Any]]:
    ensure_data()
    # Use the existing get_trending_articles function
    articles = R.get_trending_articles(k)
    # Convert to the format expected by the API
    result = []
    for article in articles:
        result.append({
            "item_id": article.get('NewsID', ''),
            "score": 1.0,  # trending articles don't have scores
            "title": article.get('Title', ''),
            "reason": f"Trending in {article.get('Category', 'general')}"
        })
    return result

def recommend(user_id: str, k: int = 10, recent_clicks=None, locale="en") -> List[Dict[str, Any]]:
    ensure_data()
    # Use BERT4Rec for better sequential recommendations
    articles = R.get_bert4rec_recommendations(user_id, k)
    # Convert to the format expected by the API
    result = []
    for article in articles:
        # Some recommendations might have a similarity score, others might not
        score = article.get('Similarity', 0.8)  # Higher default score for BERT4Rec
        result.append({
            "item_id": article.get('NewsID', ''),
            "score": float(score),
            "title": article.get('Title', ''),
            "reason": f"BERT4Rec: Based on your reading sequence in {article.get('Category', 'general')}"
        })
    return result

def recommend_hybrid(user_id: str, k: int = 10, recent_clicks=None, locale="en") -> List[Dict[str, Any]]:
    ensure_data()
    # Use traditional hybrid approach (collaborative + content-based)
    articles = R.hybrid_recommendations(user_id, k)
    # Convert to the format expected by the API
    result = []
    for article in articles:
        score = article.get('Similarity', 0.6)  # Lower default score for hybrid
        result.append({
            "item_id": article.get('NewsID', ''),
            "score": float(score),
            "title": article.get('Title', ''),
            "reason": f"Hybrid: Collaborative + Content filtering in {article.get('Category', 'general')}"
        })
    return result

def get_available_categories() -> List[str]:
    """Get list of available news categories"""
    ensure_data()
    categories = R.get_available_categories()
    return categories

def keyword_search(q: str, k: int = 20, category: str = None) -> List[Dict[str, Any]]:
    ensure_data()
    # Use the existing get_article_recommendations function with category filter
    articles = R.get_article_recommendations(q, k, category)
    # Convert to the format expected by the API
    result = []
    for article in articles:
        result.append({
            "item_id": article.get('NewsID', ''),
            "score": 0.8,  # Fixed score for keyword matches
            "title": article.get('Title', ''),
            "reason": f"Matches search query: {q}" + (f" in {category}" if category else "")
        })
    return result

def summarize(title: Optional[str], abstract: Optional[str], max_tokens: int = 128) -> str:
    text = (title or "") + ". " + (abstract or "")
    if not text.strip():
        return ""
    try:
        from transformers import pipeline
        summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
        out = summarizer(text, max_length=max_tokens, min_length=max(32, max_tokens//4), do_sample=False)
        return out[0]["summary_text"]
    except Exception:
        # Fallback: simple heuristic summary
        return (abstract or title or "")[:max_tokens*3]

def export_pdf(articles: List[Dict[str, Any]]) -> str:
    # Use your existing utils/pdf_utils.py
    return PDF.generate_pdf_from_articles(articles)