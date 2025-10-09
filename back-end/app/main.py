from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .database import init_db, close_db
from .routes import users, tasks, labels, auth
from config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    """
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()


app = FastAPI(
    title=settings.APP_NAME,
    description="A comprehensive Todo application with user authentication, tasks, and labels",
    version=settings.APP_VERSION,
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(labels.router)


@app.get(
    "/",
    tags=["Health"],
    summary="Health check endpoint",
    description="Returns application status and basic information"
)
async def read_root():
    """
    Root endpoint for health checks and basic API information.
    """
    return {
        "message": "Welcome to Todo App API!",
        "status": "healthy",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get(
    "/health",
    tags=["Health"],
    summary="Detailed health check",
    description="Returns detailed application and database health status"
)
async def health_check():
    """
    Detailed health check endpoint.
    """
    from .database import database
    
    # Check database health
    db_healthy = await database.health_check()
    
    return {
        "status": "healthy" if db_healthy else "unhealthy",
        "database": "connected" if db_healthy else "disconnected",
        "api": "running"
    }