# Mock recommenders module for testing
import json
import os

# Sample mock data
MOCK_ARTICLES = [
    {
        "item_id": "N1001",
        "title": "Sample News Article 1",
        "abstract": "This is a sample news article for testing purposes.",
        "category": "Technology",
        "url": "https://example.com/article1",
        "score": 0.95
    },
    {
        "item_id": "N1002", 
        "title": "Sample News Article 2",
        "abstract": "Another sample news article for testing.",
        "category": "Sports",
        "url": "https://example.com/article2",
        "score": 0.87
    },
    {
        "item_id": "N1003",
        "title": "Sample News Article 3", 
        "abstract": "Yet another sample news article.",
        "category": "Politics",
        "url": "https://example.com/article3",
        "score": 0.78
    }
]

def _ensure_data_loaded():
    """Mock data loading function"""
    print("Mock data loaded")
    pass

def get_trending_articles(k=20):
    """Mock trending articles"""
    return MOCK_ARTICLES[:min(k, len(MOCK_ARTICLES))]

def recommend_for_user(user_id, k=10, recent_clicks=None, locale="en"):
    """Mock user recommendations"""
    print(f"Generating recommendations for user {user_id}")
    return MOCK_ARTICLES[:min(k, len(MOCK_ARTICLES))]

def search_by_keywords(q, k=20):
    """Mock keyword search"""
    print(f"Searching for: {q}")
    # Filter articles that contain the search query
    filtered = [article for article in MOCK_ARTICLES 
                if q.lower() in article['title'].lower() 
                or q.lower() in article['abstract'].lower()]
    return filtered[:min(k, len(filtered))]

def get_article_details(news_ids):
    """Mock article details retrieval"""
    return [article for article in MOCK_ARTICLES 
            if article['item_id'] in news_ids]