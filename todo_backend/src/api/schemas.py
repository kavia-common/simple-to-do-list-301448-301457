"""
Pydantic schemas for Todo API

This module defines the request and response models for the Todo API endpoints.
"""
from pydantic import BaseModel, Field
from typing import Optional


class TodoBase(BaseModel):
    """Base schema for Todo with common fields"""
    title: str = Field(..., description="Title of the todo item", min_length=1, max_length=500)
    description: Optional[str] = Field(default="", description="Description of the todo item", max_length=2000)
    completed: bool = Field(default=False, description="Whether the todo is completed")


# PUBLIC_INTERFACE
class TodoCreate(TodoBase):
    """
    Schema for creating a new todo item
    
    Attributes:
        title: The title of the todo (required)
        description: Optional description of the todo
        completed: Whether the todo is completed (defaults to False)
    """
    pass


# PUBLIC_INTERFACE
class TodoUpdate(BaseModel):
    """
    Schema for updating an existing todo item
    
    All fields are optional to allow partial updates.
    
    Attributes:
        title: Optional new title for the todo
        description: Optional new description for the todo
        completed: Optional new completion status
    """
    title: Optional[str] = Field(None, description="Title of the todo item", min_length=1, max_length=500)
    description: Optional[str] = Field(None, description="Description of the todo item", max_length=2000)
    completed: Optional[bool] = Field(None, description="Whether the todo is completed")


# PUBLIC_INTERFACE
class TodoComplete(BaseModel):
    """
    Schema for marking a todo as complete/incomplete
    
    Attributes:
        completed: Whether the todo should be marked as completed
    """
    completed: bool = Field(..., description="Whether the todo is completed")


# PUBLIC_INTERFACE
class TodoResponse(TodoBase):
    """
    Schema for todo response
    
    This includes all todo fields plus system-generated fields like id and timestamps.
    
    Attributes:
        id: Unique identifier for the todo
        title: The title of the todo
        description: Description of the todo
        completed: Whether the todo is completed
        created_at: When the todo was created
        updated_at: When the todo was last updated
    """
    id: int = Field(..., description="Unique identifier for the todo")
    created_at: str = Field(..., description="When the todo was created")
    updated_at: str = Field(..., description="When the todo was last updated")

    class Config:
        from_attributes = True


# PUBLIC_INTERFACE
class TodoListResponse(BaseModel):
    """
    Schema for list of todos response
    
    Attributes:
        todos: List of todo items
        total: Total count of todos
    """
    todos: list[TodoResponse] = Field(default=[], description="List of todo items")
    total: int = Field(..., description="Total count of todos")


# PUBLIC_INTERFACE
class ErrorResponse(BaseModel):
    """
    Schema for error responses
    
    Attributes:
        detail: Error message describing what went wrong
    """
    detail: str = Field(..., description="Error message")
