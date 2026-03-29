import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.adapters.routers import auth, health
from app.database import create_db_and_tables

# CORS configuration
CORS_ORIGINS = os.getenv(
    "CORS_ORIGINS", "http://localhost:3000,http://localhost:5173"
).split(",")

# Create FastAPI app
app = FastAPI(
    title="Sports Championship API",
    description="High-integrity sports championship management system",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Event handlers
@app.on_event("startup")
async def on_startup() -> None:
    """Initialize database on startup."""
    create_db_and_tables()


# Include routers
app.include_router(health.router)
app.include_router(auth.router)


# Root endpoint
@app.get("/")
async def root() -> dict:
    """Root endpoint."""
    return {
        "message": "Sports Championship API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/api/health",
    }
