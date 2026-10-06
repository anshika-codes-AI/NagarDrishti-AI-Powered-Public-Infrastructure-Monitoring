from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.analyze_image import router as analyze_image_router
from app.api.analyze_video import router as analyze_video_router
from app.api.reports import router as reports_router

app = FastAPI(
    title="AI-Powered Public Infrastructure Monitoring",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze_image_router)
app.include_router(analyze_video_router)
app.include_router(reports_router)


@app.get("/")
def root():
    return {
        "success": True,
        "message": "AI-Powered Public Infrastructure Monitoring API",
    }


@app.get("/api/health")
def health():
    return {
        "success": True,
        "status": "healthy",
    }