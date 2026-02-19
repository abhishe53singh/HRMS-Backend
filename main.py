"""
HRMS Lite Backend - Entry Point

This file serves as the entry point for the application.
The actual application logic is structured in the 'app' directory.
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
