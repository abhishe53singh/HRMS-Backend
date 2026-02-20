from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from app.routers import employees_router, attendance_router

# Create FastAPI application
app = FastAPI(
    title="HRMS Lite API",
    description="Employee Management & Attendance Tracking System",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"  # Allow all origins for production
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Include routers
app.include_router(employees_router)
app.include_router(attendance_router)


@app.get("/")
def root():
    """
    Root endpoint
    
    Returns basic information about the API.
    """
    return {
        "message": "HRMS Lite API",
        "version": "2.0.0",
        "description": "Employee Management & Attendance Tracking System",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint
    
    Returns the current health status of the API.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "api_version": "2.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
