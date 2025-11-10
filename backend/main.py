"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from api.v1 import routes as v1_routes

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API for scanning Pokemon cards and retrieving pricing information",
)

# Configure CORS - Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=False,  # Must be False when allow_origins is ["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add request logging middleware
from fastapi import Request

@app.middleware("http")
async def log_requests(request: Request, call_next):
    if request.url.path == "/api/v1/scan":
        print(f"[MIDDLEWARE] === INCOMING REQUEST TO /api/v1/scan ===")
        print(f"[MIDDLEWARE] Method: {request.method}")
        print(f"[MIDDLEWARE] Headers: {dict(request.headers)}")
        print(f"[MIDDLEWARE] Content-Type: {request.headers.get('content-type')}")

    response = await call_next(request)

    if request.url.path == "/api/v1/scan":
        print(f"[MIDDLEWARE] Response status: {response.status_code}")

    return response

# Include API routes
app.include_router(v1_routes.router, prefix="/api/v1", tags=["v1"])


@app.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/api/v1/health"
    }
