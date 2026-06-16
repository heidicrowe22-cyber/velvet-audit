"""Velvet Hour Audit - Main FastAPI Application."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import init_db, close_db
from app.api import auth, audits, fixes, orders, admin, reports, websites


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup and shutdown events."""
    await init_db()
    yield
    await close_db()


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ─── Middleware ─────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routers ───────────────────────────────────────────────────

app.include_router(auth.router, prefix=f"{settings.API_PREFIX}/auth", tags=["Auth"])
app.include_router(websites.router, prefix=f"{settings.API_PREFIX}/websites", tags=["Websites"])
app.include_router(audits.router, prefix=f"{settings.API_PREFIX}/audits", tags=["Audits"])
app.include_router(reports.router, prefix=f"{settings.API_PREFIX}/reports", tags=["Reports"])
app.include_router(fixes.router, prefix=f"{settings.API_PREFIX}/fixes", tags=["Fixes"])
app.include_router(orders.router, prefix=f"{settings.API_PREFIX}/orders", tags=["Orders"])
app.include_router(admin.router, prefix=f"{settings.API_PREFIX}/admin", tags=["Admin"])


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "app": settings.APP_NAME, "version": "1.0.0"}