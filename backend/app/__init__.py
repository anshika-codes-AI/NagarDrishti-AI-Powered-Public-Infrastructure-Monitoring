from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from .api.health import router as health_router
from .api.reports import router as reports_router
from .api.analyze_image import router as analyze_image_router
from .api.analyze_video import router as analyze_video_router

app = FastAPI(
    title="AI-Powered Public Infrastructure Monitoring API",
    description="Backend for AI-powered public infrastructure monitoring system",
    version="0.1.0",
)

# CORS - allow frontend origin during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(health_router, prefix="/api", tags=["health"])
app.include_router(reports_router, prefix="/api", tags=["reports"])
app.include_router(analyze_image_router, prefix="/api", tags=["analysis"])
app.include_router(analyze_video_router, prefix="/api", tags=["analysis"])


@app.get("/")
async def root() -> dict:
    return {"message": "AI-Powered Public Infrastructure Monitoring API", "version": "0.1.0"}