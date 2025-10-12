#!/usr/bin/env python3
"""
REST API wrapper for Google Keep MCP server.
Provides standard REST endpoints with proper health checks.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import os
import json
from datetime import datetime
from .keep_api import get_client, serialize_note, can_modify_note

app = FastAPI(
    title="Google Keep REST API",
    description="REST API for Google Keep MCP Server",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response validation
class NoteSearchRequest(BaseModel):
    query: Optional[str] = Field(default="", description="Search query string")

class NoteCreateRequest(BaseModel):
    title: Optional[str] = Field(None, description="Note title")
    text: Optional[str] = Field(None, description="Note text content")

class NoteUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, description="New title")
    text: Optional[str] = Field(None, description="New text content")

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    service: str
    google_keep_connected: bool
    version: str = "1.0.0"

class NoteResponse(BaseModel):
    id: str
    title: Optional[str]
    text: Optional[str]
    pinned: bool
    color: Optional[str]
    labels: List[Dict[str, str]]

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint that verifies Google Keep connection.
    """
    try:
        # Try to initialize the Keep client
        keep = get_client()
        connected = True
        status = "healthy"
    except Exception as e:
        connected = False
        status = "unhealthy"

    return {
        "status": status,
        "timestamp": datetime.utcnow().isoformat(),
        "service": "google-keep-rest-api",
        "google_keep_connected": connected
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "service": "Google Keep REST API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health or /api/health",
            "search": "GET /api/notes/search?query=...",
            "create": "POST /api/notes",
            "get": "GET /api/notes/{note_id}",
            "update": "PUT /api/notes/{note_id}",
            "delete": "DELETE /api/notes/{note_id}",
            "list": "GET /api/notes"
        },
        "docs": "/docs"
    }

# Search/find notes
@app.get("/api/notes/search")
async def search_notes(query: str = ""):
    """
    Search for notes matching the query string.

    Args:
        query: Search query string

    Returns:
        List of matching notes
    """
    try:
        keep = get_client()
        notes = keep.find(query=query, archived=False, trashed=False)
        notes_data = [serialize_note(note) for note in notes]
        return {"notes": notes_data, "count": len(notes_data)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# List all notes (same as search with empty query)
@app.get("/api/notes")
async def list_notes():
    """
    List all notes (non-archived, non-trashed).

    Returns:
        List of all notes
    """
    return await search_notes(query="")

# Get a specific note
@app.get("/api/notes/{note_id}")
async def get_note(note_id: str):
    """
    Get a specific note by ID.

    Args:
        note_id: The ID of the note

    Returns:
        Note details
    """
    try:
        keep = get_client()
        note = keep.get(note_id)

        if not note:
            raise HTTPException(status_code=404, detail=f"Note with ID {note_id} not found")

        return serialize_note(note)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Create a new note
@app.post("/api/notes", response_model=NoteResponse)
async def create_note(note: NoteCreateRequest):
    """
    Create a new note with title and text.

    Args:
        note: Note creation request with title and text

    Returns:
        Created note details
    """
    try:
        keep = get_client()
        new_note = keep.createNote(title=note.title, text=note.text)

        # Get or create the keep-mcp label
        label = keep.findLabel('keep-mcp')
        if not label:
            label = keep.createLabel('keep-mcp')

        # Add the label to the note
        new_note.labels.add(label)
        keep.sync()  # Ensure the note is created and labeled on the server

        return serialize_note(new_note)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Update a note
@app.put("/api/notes/{note_id}", response_model=NoteResponse)
async def update_note(note_id: str, note_update: NoteUpdateRequest):
    """
    Update a note's title and/or text.

    Args:
        note_id: The ID of the note to update
        note_update: Updated note data

    Returns:
        Updated note details
    """
    try:
        keep = get_client()
        note = keep.get(note_id)

        if not note:
            raise HTTPException(status_code=404, detail=f"Note with ID {note_id} not found")

        if not can_modify_note(note):
            raise HTTPException(
                status_code=403,
                detail=f"Note with ID {note_id} cannot be modified (missing keep-mcp label and UNSAFE_MODE is not enabled)"
            )

        if note_update.title is not None:
            note.title = note_update.title
        if note_update.text is not None:
            note.text = note_update.text

        keep.sync()  # Ensure changes are saved to the server
        return serialize_note(note)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Delete a note
@app.delete("/api/notes/{note_id}")
async def delete_note(note_id: str):
    """
    Delete a note (mark for deletion).

    Args:
        note_id: The ID of the note to delete

    Returns:
        Success message
    """
    try:
        keep = get_client()
        note = keep.get(note_id)

        if not note:
            raise HTTPException(status_code=404, detail=f"Note with ID {note_id} not found")

        if not can_modify_note(note):
            raise HTTPException(
                status_code=403,
                detail=f"Note with ID {note_id} cannot be modified (missing keep-mcp label and UNSAFE_MODE is not enabled)"
            )

        note.delete()
        keep.sync()  # Ensure deletion is saved to the server
        return {"message": f"Note {note_id} marked for deletion", "status": "success"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn

    host = os.getenv("REST_API_HOST", "0.0.0.0")
    port = int(os.getenv("REST_API_PORT", "8001"))

    print(f"Starting Google Keep REST API server on {host}:{port}")
    print(f"Documentation available at http://{host}:{port}/docs")

    uvicorn.run(app, host=host, port=port)
