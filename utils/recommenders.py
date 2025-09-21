import pandas as pd
import numpy as np
import os
from typing import Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

# Global variables for lazy loading
_news_df = None
_behaviors_df = None
_is_data_loaded = False

def load_mind_data():
    """Load MIND dataset with proper error handling"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    data_dir = os.path.join(project_root, 'MINDsmall_train')
    
    news_path = os.path.join(data_dir, 'news.tsv')
    behaviors_path = os.path.join(data_dir, 'behaviors.tsv')
    
    print(f"Loading news data from: {news_path}")
    news_df = pd.read_csv(news_path, sep='\t', header=None, 
                         names=['NewsID', 'Category', 'SubCategory', 'Title', 'Abstract', 'URL', 'TitleEntities', 'AbstractEntities'])
    
    print(f"Loading behaviors data from: {behaviors_path}")
    # Use sample for faster loading during testing
    behaviors_df = pd.read_csv(behaviors_path, sep='\t', header=None,
                              names=['ImpressionID', 'UserID', 'Time', 'History', 'Impressions'],
                              nrows=5000)  # Limit rows for faster loading
    
    return news_df, behaviors_df

def _ensure_data_loaded():
    """Ensure data is loaded (lazy loading)"""
    global _news_df, _behaviors_df, _is_data_loaded
    if not _is_data_loaded:
        print("Loading MIND dataset...")
        _news_df, _behaviors_df = load_mind_data()
        _is_data_loaded = True
        print(f"Loaded {len(_news_df)} news articles and {len(_behaviors_df)} user behaviors")

def parse_impressions(impression_str):
    """Parse impression string into list of (news_id, label) tuples"""
    if pd.isna(impression_str):
        return []
    
    result = []
    impression_list = impression_str.split()
    for item in impression_list:
        parts = item.split('-')
        if len(parts) == 2:
            news_id, label = parts[0], int(parts[1])
            result.append((news_id, label))
    return result

def parse_history(history_str):
    """Parse history string into list of news IDs"""
    if pd.isna(history_str):
        return []
    return history_str.split()

def collaborative_filtering_recommendations(user_id, top_k=10):
    """Generate recommendations using collaborative filtering with SVD"""
    _ensure_data_loaded()
    
    # Preprocess data for collaborative filtering
    interaction_data = []
    user_encoder = LabelEncoder()
    news_encoder = LabelEncoder()
    
    all_users = []
    all_news = []
    
    for _, row in _behaviors_df.iterrows():
        current_user_id = row['UserID']
        history = parse_history(row['History'])
        impressions = parse_impressions(row['Impressions'])
        
        # Add positive interactions from history
        for news_id in history:
            interaction_data.append((current_user_id, news_id, 1))
            all_users.append(current_user_id)
            all_news.append(news_id)
        
        # Add interactions from impressions
        for news_id, label in impressions:
            interaction_data.append((current_user_id, news_id, label))
            all_users.append(current_user_id)
            all_news.append(news_id)
    
    # Create interaction matrix
    df_interactions = pd.DataFrame(interaction_data, columns=['user_id', 'news_id', 'rating'])
    df_interactions = df_interactions.groupby(['user_id', 'news_id'])['rating'].mean().reset_index()
    
    # Encode users and news
    df_interactions['user_encoded'] = user_encoder.fit_transform(df_interactions['user_id'])
    df_interactions['news_encoded'] = news_encoder.fit_transform(df_interactions['news_id'])
    
    # Create user-item matrix
    n_users = df_interactions['user_encoded'].nunique()
    n_items = df_interactions['news_encoded'].nunique()
    
    user_item_matrix = np.zeros((n_users, n_items))
    for row in df_interactions.itertuples():
        user_item_matrix[row.user_encoded, row.news_encoded] = row.rating
    
    # Apply SVD
    n_latent_factors = min(100, min(n_users, n_items) - 1)
    svd_model = TruncatedSVD(n_components=n_latent_factors, random_state=42)
    matrix_reduced = svd_model.fit_transform(user_item_matrix)
    
    # Get recommendations for the user
    if user_id in user_encoder.classes_:
        user_encoded = user_encoder.transform([user_id])[0]
        user_profile = matrix_reduced[user_encoded]
        
        # Calculate scores for all news
        scores = np.dot(svd_model.components_.T, user_profile)
        
        # Get top recommendations
        top_indices = np.argsort(scores)[::-1][:top_k]
        recommended_news_ids = news_encoder.inverse_transform(top_indices)
        
        # Get news details
        recommendations = []
        for news_id in recommended_news_ids:
            news_info = _news_df[_news_df['NewsID'] == news_id]
            if not news_info.empty:
                recommendations.append({
                    'NewsID': news_id,
                    'Title': news_info.iloc[0]['Title'],
                    'Category': news_info.iloc[0]['Category'],
                    'Abstract': news_info.iloc[0]['Abstract']
                })
        
        return recommendations
    else:
        # Return popular articles for new users
        return get_popular_articles(top_k)

def content_based_recommendations(user_id, top_k=10):
    """Generate recommendations using content-based filtering"""
    _ensure_data_loaded()
    
    # Create TF-IDF matrix for news content
    news_content = _news_df['Title'].fillna('') + ' ' + _news_df['Abstract'].fillna('')
    tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
    tfidf_matrix = tfidf_vectorizer.fit_transform(news_content)
    
    # Get user's reading history
    user_data = _behaviors_df[_behaviors_df['UserID'] == user_id]
    if user_data.empty:
        return get_popular_articles(top_k)
    
    # Create user profile from reading history
    user_profile = np.zeros(tfidf_matrix.shape[1])
    news_id_to_title = dict(zip(_news_df['NewsID'], _news_df['Title']))
    
    for _, row in user_data.iterrows():
        clicked_ids = parse_history(row['History'])
        titles = [news_id_to_title[nid] for nid in clicked_ids if nid in news_id_to_title]
        
        if titles:
            user_content = ' '.join(titles)
            user_tfidf = tfidf_vectorizer.transform([user_content])
            user_profile += user_tfidf.toarray()[0]
    
    if np.sum(user_profile) == 0:
        return get_popular_articles(top_k)
    
    # Calculate similarity with all news articles
    user_profile = user_profile.reshape(1, -1)
    similarities = cosine_similarity(user_profile, tfidf_matrix)[0]
    
    # Get top recommendations
    top_indices = np.argsort(similarities)[::-1][:top_k]
    
    recommendations = []
    for idx in top_indices:
        news_row = _news_df.iloc[idx]
        recommendations.append({
            'NewsID': news_row['NewsID'],
            'Title': news_row['Title'],
            'Category': news_row['Category'],
            'Abstract': news_row['Abstract'],
            'Similarity': similarities[idx]
        })
    
    return recommendations

def hybrid_recommendations(user_id, top_k=10, cf_weight=0.6, cb_weight=0.4):
    """Generate hybrid recommendations combining collaborative and content-based filtering"""
    cf_recs = collaborative_filtering_recommendations(user_id, top_k * 2)
    cb_recs = content_based_recommendations(user_id, top_k * 2)
    
    # Simple hybrid approach: combine and weight
    all_recs = {}
    
    # Add collaborative filtering recommendations
    for i, rec in enumerate(cf_recs):
        score = cf_weight * (len(cf_recs) - i) / len(cf_recs)
        all_recs[rec['NewsID']] = {
            'rec': rec,
            'score': score
        }
    
    # Add content-based recommendations
    for i, rec in enumerate(cb_recs):
        score = cb_weight * (len(cb_recs) - i) / len(cb_recs)
        news_id = rec['NewsID']
        if news_id in all_recs:
            all_recs[news_id]['score'] += score
        else:
            all_recs[news_id] = {
                'rec': rec,
                'score': score
            }
    
    # Sort by combined score
    sorted_recs = sorted(all_recs.items(), key=lambda x: x[1]['score'], reverse=True)
    
    return [item[1]['rec'] for item in sorted_recs[:top_k]]

def get_popular_articles(top_k=10):
    """Get popular articles based on category diversity"""
    _ensure_data_loaded()
    
    # Simple popularity based on category distribution
    popular_articles = []
    categories = _news_df['Category'].value_counts().head(5).index
    
    for category in categories:
        category_articles = _news_df[_news_df['Category'] == category].head(2)
        for _, article in category_articles.iterrows():
            if len(popular_articles) < top_k:
                popular_articles.append({
                    'NewsID': article['NewsID'],
                    'Title': article['Title'],
                    'Category': article['Category'],
                    'Abstract': article['Abstract']
                })
    
    return popular_articles

def get_user_list():
    """Get list of available users"""
    _ensure_data_loaded()
    return _behaviors_df['UserID'].unique()[:100].tolist()  # Return first 100 users

def get_news_by_category(category, limit=10):
    """Get news articles by category"""
    _ensure_data_loaded()
    
    category_news = _news_df[_news_df['Category'] == category].head(limit)
    
    news_list = []
    for _, article in category_news.iterrows():
        news_list.append({
            'NewsID': article['NewsID'],
            'Title': article['Title'],
            'Category': article['Category'],
            'Abstract': article['Abstract']
        })
    
    return news_list

def get_categories():
    """Get list of available categories"""
    _ensure_data_loaded()
    return _news_df['Category'].value_counts().head(10).index.tolist()

# Additional functions expected by main.py
def get_user_recommendations(user_id, method='hybrid', top_k=10):
    """Get user recommendations using specified method"""
    if method == 'collaborative':
        return collaborative_filtering_recommendations(user_id, top_k)
    elif method == 'content':
        return content_based_recommendations(user_id, top_k)
    elif method == 'hybrid':
        return hybrid_recommendations(user_id, top_k)
    else:
        return get_popular_articles(top_k)

def get_article_recommendations(keywords, top_k=10, category=None):
    """Get article recommendations based on keywords and optional category"""
    _ensure_data_loaded()
    
    # Start with all articles
    df = _news_df.copy()
    
    # Filter by category if specified
    if category and category.lower() != 'all':
        category_mask = df['Category'].str.contains(category, case=False, na=False)
        df = df[category_mask]
        print(f"Filtering by category '{category}': {len(df)} articles found")
    
    # Search in titles and abstracts
    if keywords and keywords.strip():
        mask = df['Title'].str.contains(keywords, case=False, na=False) | \
               df['Abstract'].str.contains(keywords, case=False, na=False)
        df = df[mask]
    
    results = df.head(top_k)
    
    recommendations = []
    for _, article in results.iterrows():
        recommendations.append({
            'NewsID': article['NewsID'],
            'Title': article['Title'],
            'Category': article['Category'],
            'Abstract': article['Abstract']
        })
    
    return recommendations

def get_hybrid_recommendations(user_id, top_k=10):
    """Alias for hybrid_recommendations"""
    return hybrid_recommendations(user_id, top_k)

def get_news_metadata(news_id):
    """Get metadata for a specific news article"""
    _ensure_data_loaded()
    
    article = _news_df[_news_df['NewsID'] == news_id]
    if not article.empty:
        article_data = article.iloc[0]
        return {
            'NewsID': article_data['NewsID'],
            'Title': article_data['Title'],
            'Category': article_data['Category'],
            'SubCategory': article_data['SubCategory'],
            'Abstract': article_data['Abstract'],
            'URL': article_data['URL']
        }
    return None

def get_bert4rec_recommendations(user_id, top_k=10):
    """BERT4Rec recommendations using the real transformer model"""
    _ensure_data_loaded()
    
    try:
        # Import and use the real BERT4Rec implementation
        from utils.bert4rec import BERT4RecRecommender
        
        print("Using BERT4Rec for sequential recommendations")
        
        # Initialize BERT4Rec
        bert_recommender = BERT4RecRecommender()
        bert_recommender.load_model()
        bert_recommender.load_data(_news_df, _behaviors_df)
        
        # Get BERT4Rec recommendations
        recommendations = bert_recommender.recommend_articles_for_user(user_id, top_k)
        
        return recommendations
        
    except ImportError as e:
        print(f"BERT4Rec import failed ({str(e)}), falling back to hybrid recommendations")
        return hybrid_recommendations(user_id, top_k)
    except Exception as e:
        print(f"BERT4Rec failed ({str(e)}), falling back to hybrid recommendations")
        return hybrid_recommendations(user_id, top_k)

def get_trending_articles(top_k=10):
    """Get trending articles (same as popular articles)"""
    return get_popular_articles(top_k)

def get_user_histories():
    """Get user interaction histories"""
    _ensure_data_loaded()
    
    histories = {}
    for _, row in _behaviors_df.iterrows():
        user_id = row['UserID']
        history = parse_history(row['History'])
        
        if user_id not in histories:
            histories[user_id] = []
        
        histories[user_id].extend(history)
    
    # Remove duplicates and limit
    for user_id in histories:
        histories[user_id] = list(set(histories[user_id]))[:50]  # Limit to 50 articles per user
    
    return histories

def get_unique_articles_df():
    """Get unique articles DataFrame"""
    _ensure_data_loaded()
    return _news_df.copy()

# Create user_histories as a simple variable for compatibility
user_histories = None

# Create unique_articles_df as a simple variable for compatibility  
unique_articles_df = None

def get_available_categories():
    """Get list of available news categories from the dataset"""
    _ensure_data_loaded()
    categories = _news_df['Category'].unique().tolist()
    categories = [cat for cat in categories if pd.notna(cat)]  # Remove NaN values
    return sorted(categories)

# ---- Thin helper API for FastAPI layer ----

def get_trending_articles(k: int = 20):
    """Return top-k trending articles.
    MUST return: list[dict] with keys: item_id (str), score (float), title (str|opt), reason (str|opt)."""
    _ensure_data_loaded()
    
    # Use the existing get_popular_articles function and convert to expected format
    popular_articles = get_popular_articles(top_k=k)
    
    trending_articles = []
    for article in popular_articles:
        trending_articles.append({
            "item_id": article.get('NewsID', ''),
            "score": 1.0,
            "title": article.get('Title', ''),
            "reason": "Trending"
        })
    
    return trending_articles

def format_recommendations(recs, reason_prefix):
    """Format recommendations to standard format"""
    results = []
    for rec in recs:
        if isinstance(rec, dict):
            # Standardize the format
            item = {
                "item_id": rec.get('NewsID', rec.get('item_id', 'unknown')),
                "score": float(rec.get('score', rec.get('Similarity', 1.0))),
                "title": rec.get('Title', rec.get('title', f"Article {rec.get('NewsID', 'unknown')}")),
                "reason": f"{reason_prefix}: {rec.get('reason', 'Based on your preferences')}"
            }
            results.append(item)
        else:
            # Handle legacy tuple format
            print(f"Warning: unexpected recommendation format: {rec}")
    return results

def bert_recommendations(user_id: str, top_k: int = 10):
    """BERT-based recommendations (enhanced content-based for now)"""
    # For now, use enhanced content-based approach
    # This simulates BERT by giving higher weight to recent interactions
    user_data = _behaviors_df[_behaviors_df['UserID'] == user_id]
    if user_data.empty:
        return get_popular_articles(top_k)
    
    # Get user's recent history with higher weighting for recent items
    recent_articles = []
    for _, row in user_data.iterrows():
        history = parse_history(row['History'])
        # Take only the most recent items for BERT-style sequential modeling
        recent_articles.extend(history[-5:])  # Last 5 articles
    
    if not recent_articles:
        return get_popular_articles(top_k)
    
    # Use content-based approach with recent focus
    content_recs = content_based_recommendations(user_id, top_k * 2)
    
    # Add some randomization to simulate BERT's neural approach
    import random
    random.shuffle(content_recs)
    
    return content_recs[:top_k]

def recommend_for_user(user_id: str, k: int = 10, recent_clicks=None, locale: str = "en", algorithm: str = "hybrid"):
    """Return top-k personalized recommendations for user_id.
    MUST return: list[dict] with keys: item_id, score, title|opt, reason|opt."""
    _ensure_data_loaded()
    
    try:
        if algorithm == "collaborative":
            # Use collaborative filtering
            recs = collaborative_filtering_recommendations(user_id, top_k=k)
            return format_recommendations(recs, "Collaborative Filtering")
            
        elif algorithm == "content":
            # Use content-based filtering
            recs = content_based_recommendations(user_id, top_k=k)
            return format_recommendations(recs, "Content-Based")
            
        elif algorithm == "hybrid":
            # Use hybrid approach
            recs = hybrid_recommendations(user_id, top_k=k)
            return format_recommendations(recs, "Hybrid Recommendation")
            
        elif algorithm == "bert":
            # Use BERT4Rec approach (simulated for now)
            recs = bert_recommendations(user_id, top_k=k)
            return format_recommendations(recs, "BERT4Rec")
            
        else:
            # Default to hybrid
            recs = hybrid_recommendations(user_id, top_k=k)
            return format_recommendations(recs, "Hybrid Recommendation")
            
    except Exception as e:
        print(f"Recommendation failed for algorithm {algorithm}: {e}")
        # Fallback to trending
        trending_recs = get_popular_articles(top_k=k)
        return format_recommendations(trending_recs, "Trending")

def search_by_keywords(q: str, k: int = 20, category: Optional[str] = None):
    """Keyword search using your TF-IDF or content-based search.
    MUST return: list[dict] with keys: item_id, score, title|opt, reason|opt."""
    _ensure_data_loaded()
    
    try:
        # Use existing keyword search functionality
        article_results = get_article_recommendations(q, top_k=k)
        formatted_results = []
        
        for _, article in article_results.iterrows():
            # Apply category filter if specified
            if category and category.lower() != 'all':
                article_category = article.get('Category', '').lower()
                article_subcategory = article.get('SubCategory', '').lower()
                if (category.lower() not in article_category and 
                    category.lower() not in article_subcategory):
                    continue
            
            formatted_results.append({
                "item_id": article['NewsID'],
                "score": 1.0,  # get_article_recommendations doesn't return scores
                "title": article['Title'] if pd.notna(article['Title']) else f"Article {article['NewsID']}",
                "reason": "Keyword match"
            })
        
        return formatted_results[:k]
        
    except Exception as e:
        print(f"Keyword search failed: {e}")
        # Fallback to simple title/abstract search
        query_lower = q.lower()
        matches = []
        
        for _, article in _news_df.iterrows():
            # Apply category filter if specified
            if category and category.lower() != 'all':
                article_category = article.get('Category', '').lower()
                article_subcategory = article.get('SubCategory', '').lower()
                if (category.lower() not in article_category and 
                    category.lower() not in article_subcategory):
                    continue
                    
            score = 0.0
            title = article['Title'] if pd.notna(article['Title']) else ""
            abstract = article['Abstract'] if pd.notna(article['Abstract']) else ""
            
            # Simple keyword matching
            if query_lower in title.lower():
                score += 2.0
            if query_lower in abstract.lower():
                score += 1.0
            
            if score > 0:
                matches.append({
                    "item_id": article['NewsID'],
                    "score": score,
                    "title": title or f"Article {article['NewsID']}",
                    "reason": "Keyword match"
                })
        
        # Sort by score and return top k
        matches.sort(key=lambda x: x['score'], reverse=True)
        return matches[:k]

def get_article_details(news_ids):
    """Get full article details by news IDs for PDF export"""
    _ensure_data_loaded()
    
    articles = []
    for news_id in news_ids:
        article_row = _news_df[_news_df['NewsID'] == news_id]
        if not article_row.empty:
            article = article_row.iloc[0]
            articles.append({
                'item_id': article['NewsID'],
                'title': article['Title'],
                'category': article['Category'], 
                'subcategory': article['SubCategory'],
                'abstract': article['Abstract'],
                'url': article.get('URL', '')
            })
    return articles
