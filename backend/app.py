"""FastAPI application for Ledgerly backend."""

from api.v1 import api_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Ledgerly Statement Parser API",
    description="API for processing financial statements",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {"message": "Ledgerly Statement Parser API", "status": "running"}


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "service": "backend"}


@app.get("/api/status")
async def api_status() -> dict[str, str]:
    """API status endpoint for frontend connectivity test."""
    return {"api": "online", "version": "1.0.0"}
