"""
Smart News Recommendation System - Utils Package

This package contains utility modules for the recommendation system:
- recommenders.py: Core recommendation algorithms
- pdf_utils.py: PDF generation utilities
"""

__version__ = "1.0.0"
__author__ = "Smart News Recommendation System"

# Import key functions for easy access
try:
    from .recommenders import (
        get_user_recommendations,
        get_article_recommendations,
        get_hybrid_recommendations,
        get_news_metadata,
        get_bert4rec_recommendations,
        get_trending_articles,
        user_histories,
        unique_articles_df
    )
    from .pdf_utils import generate_pdf_from_articles
    
    __all__ = [
        'get_user_recommendations',
        'get_article_recommendations', 
        'get_hybrid_recommendations',
        'get_news_metadata',
        'get_bert4rec_recommendations',
        'get_trending_articles',
        'user_histories',
        'unique_articles_df',
        'generate_pdf_from_articles'
    ]
    
except ImportError as e:
    # Handle cases where dependencies are not installed
    print(f"Warning: Could not import all utils functions due to missing dependencies: {e}")
    print("Please install requirements.txt to use all features.")
    
    __all__ = []
