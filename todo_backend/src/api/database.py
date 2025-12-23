"""
Database connection utilities for SQLite

This module provides the database connection and dependency injection for FastAPI.
"""
import sqlite3
import os
from typing import Generator
from contextlib import contextmanager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database path from environment variable
SQLITE_DB_PATH = os.getenv("SQLITE_DB")

if not SQLITE_DB_PATH:
    raise ValueError("SQLITE_DB environment variable is not set. Please configure the database path in .env file.")

if not os.path.exists(SQLITE_DB_PATH):
    raise FileNotFoundError(f"SQLite database file not found at {SQLITE_DB_PATH}. Please ensure the database is initialized.")


@contextmanager
def get_db_connection():
    """
    Context manager for database connections
    
    Yields a SQLite connection with row factory enabled for dictionary-like access.
    Automatically commits on success and closes the connection.
    
    Yields:
        sqlite3.Connection: Database connection with row factory enabled
        
    Raises:
        sqlite3.Error: If database connection or operations fail
    """
    conn = None
    try:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        conn.row_factory = sqlite3.Row  # Enable dictionary-like access to rows
        yield conn
        conn.commit()
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()


# PUBLIC_INTERFACE
def get_db() -> Generator[sqlite3.Connection, None, None]:
    """
    FastAPI dependency for database connection
    
    This function is used as a dependency in FastAPI route handlers to provide
    a database connection. It ensures proper connection lifecycle management.
    
    Yields:
        sqlite3.Connection: Database connection with row factory enabled
        
    Example:
        @app.get("/todos")
        def get_todos(db: sqlite3.Connection = Depends(get_db)):
            cursor = db.cursor()
            cursor.execute("SELECT * FROM todos")
            return cursor.fetchall()
    """
    with get_db_connection() as conn:
        yield conn
