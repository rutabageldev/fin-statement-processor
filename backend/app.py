"""FastAPI application for Ledgerly backend."""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from api.v1 import api_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services.secure_vault.config_manager import initialize_config


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager with SecureVault initialization."""
    logger.info("Starting Ledgerly backend application...")

    # Initialize configuration with secret injection
    try:
        config_manager = await initialize_config()
        logger.info("Configuration initialized with SecureVault integration")

        if config_manager.is_vault_available():
            logger.info("SecureVault is available and ready for secret management")
        else:
            logger.warning("SecureVault unavailable - using environment variables only")

    except Exception:
        logger.exception("Failed to initialize configuration")
        raise

    yield

    logger.info("Shutting down Ledgerly backend application...")


app = FastAPI(
    title="Ledgerly Statement Parser API",
    description="API for processing financial statements with integrated SecureVault",
    version="1.0.0",
    lifespan=lifespan,
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
