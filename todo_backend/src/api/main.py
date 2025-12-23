"""
Todo Backend API

A FastAPI application for managing todo items with SQLite database integration.
Provides RESTful endpoints for creating, reading, updating, and deleting todos.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from .routes import router as todo_router

# Load environment variables
load_dotenv()

# Create FastAPI application with OpenAPI metadata
app = FastAPI(
    title="Todo API",
    description="A RESTful API for managing todo items with SQLite database backend",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Todos",
            "description": "Operations for managing todo items: create, read, update, delete, and mark as complete"
        },
        {
            "name": "Health",
            "description": "Health check endpoint to verify API availability"
        }
    ]
)

# Configure CORS
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
allowed_methods = os.getenv("ALLOWED_METHODS", "*").split(",")
allowed_headers = os.getenv("ALLOWED_HEADERS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if allowed_origins != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=allowed_methods if allowed_methods != ["*"] else ["*"],
    allow_headers=allowed_headers if allowed_headers != ["*"] else ["*"],
)

# Include todo routes
app.include_router(todo_router)


# PUBLIC_INTERFACE
@app.get(
    "/",
    tags=["Health"],
    summary="Health check",
    description="Verify that the API is running and accessible",
    responses={
        200: {
            "description": "API is healthy and running",
            "content": {
                "application/json": {
                    "example": {"message": "Healthy", "status": "ok"}
                }
            }
        }
    }
)
def health_check():
    """
    Health check endpoint
    
    Returns a simple response to indicate the API is running and accessible.
    This endpoint can be used for monitoring and load balancer health checks.
    
    Returns:
        dict: Status message indicating the API is healthy
    """
    return {"message": "Healthy", "status": "ok"}
