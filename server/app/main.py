from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app import adapters
from app.schemas import (
    RecItem,
    RecommendRequest,
    RecommendResponse,
    SearchQuery,
    SummarizeRequest,
    ExportPdfRequest,
)
from app.settings import settings

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
    """Personalized recommendations using existing algorithms"""
    try:
        raw = adapters.recommend(
            req.user_id, k=req.k, recent_clicks=req.recent_clicks, locale=req.locale
        )
        items = [RecItem(**r) for r in raw]
        return {"user_id": req.user_id, "items": items}
    except Exception as e:
        raise HTTPException(500, str(e))


@app.post("/search")
def search(body: SearchQuery):
    try:
        items = adapters.keyword_search(body.q, k=body.k)
        return {"items": items}
    except Exception as e:
        raise HTTPException(500, str(e))


@app.post("/export/pdf")
def export_pdf(body: ExportPdfRequest):
    try:
        path = adapters.export_pdf([i.model_dump() for i in body.articles])
        return FileResponse(path, filename="smart_news_report.pdf", media_type="application/pdf")
    except Exception as e:
        raise HTTPException(500, str(e))
