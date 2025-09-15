from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import RecommendRequest, RecommendResponse, RecItem, SearchQuery, SummarizeRequest
from app.settings import settings
from app import adapters

app = FastAPI(title="Smart News Recommender API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/trending")
def trending(k: int = 20):
    try:
        items = adapters.get_trending(k=k)
        return {"items": items}
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/recommend", response_model=RecommendResponse)
def recommend(req: RecommendRequest):
    """BERT4Rec sequential recommendations (default)"""
    try:
        raw = adapters.recommend(req.user_id, k=req.k, recent_clicks=req.recent_clicks, locale=req.locale)
        items = [RecItem(**r) for r in raw]
        return {"user_id": req.user_id, "items": items}
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/recommend/hybrid", response_model=RecommendResponse)
def recommend_hybrid(req: RecommendRequest):
    """Hybrid collaborative + content-based recommendations"""
    try:
        raw = adapters.recommend_hybrid(req.user_id, k=req.k, recent_clicks=req.recent_clicks, locale=req.locale)
        items = [RecItem(**r) for r in raw]
        return {"user_id": req.user_id, "items": items}
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/recommend/bert4rec", response_model=RecommendResponse)
def recommend_bert4rec(req: RecommendRequest):
    """BERT4Rec sequential recommendations"""
    try:
        raw = adapters.recommend(req.user_id, k=req.k, recent_clicks=req.recent_clicks, locale=req.locale)
        items = [RecItem(**r) for r in raw]
        return {"user_id": req.user_id, "items": items}
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/recommend/hybrid", response_model=RecommendResponse)
def recommend_hybrid(req: RecommendRequest):
    """Hybrid collaborative + content-based recommendations"""
    try:
        from app import adapters
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
        from utils import recommenders as R
        
        raw = R.get_hybrid_recommendations(req.user_id, req.k)
        result = []
        for article in raw:
            score = article.get('Similarity', 0.5)
            result.append({
                "item_id": article.get('NewsID', ''),
                "score": float(score),
                "title": article.get('Title', ''),
                "reason": f"Hybrid: Based on your interest in {article.get('Category', 'general')}"
            })
        items = [RecItem(**r) for r in result]
        return {"user_id": req.user_id, "items": items}
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/categories")
def get_categories():
    """Get available news categories"""
    try:
        categories = adapters.get_available_categories()
        return {"categories": categories}
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/search")
def search(body: SearchQuery):
    try:
        items = adapters.keyword_search(body.q, k=body.k, category=body.category)
        return {"items": items}
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/summarize")
def summarize(body: SummarizeRequest):
    try:
        text = adapters.summarize(body.title, body.abstract, max_tokens=body.max_tokens or 128)
        return {"summary": text}
    except Exception as e:
        raise HTTPException(500, str(e))