"""
MCP plugin for Google Keep integration.
Provides tools for interacting with Google Keep notes through MCP.
"""

import json
from mcp.server.fastmcp import FastMCP
from .keep_api import get_client

mcp = FastMCP("keep")

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

@mcp.resource("notes://all")
def get_all_notes() -> str:
    """Get all Google Keep notes as a resource"""
    keep = get_client()
    notes = keep.all()
    
    # Convert notes to a serializable format
    notes_data = []
    for note in notes:
        notes_data.append({
            'id': note.id,
            'title': note.title,
            'text': note.text,
            'pinned': note.pinned,
            'archived': note.archived,
            'color': note.color.value if note.color else None,
            'labels': [label.name for label in note.labels.all()]
        })
    
    return json.dumps(notes_data)

@mcp.tool()
def create_keep_note(title: str, text: str, pinned: bool = False) -> str:
    """
    Create a new Google Keep note.
    
    Args:
        title (str): The title of the note
        text (str): The content of the note
        pinned (bool, optional): Whether the note should be pinned. Defaults to False.
        
    Returns:
        str: JSON string containing the created note's data
    """
    keep = get_client()
    
    # Create a new note
    note = keep.createNote(title, text)
    note.pinned = pinned
    
    # Sync changes
    keep.sync()
    
    # Return the created note's data
    return json.dumps({
        'id': note.id,
        'title': note.title,
        'text': note.text,
        'pinned': note.pinned,
        'archived': note.archived,
        'color': note.color.value if note.color else None,
        'labels': [label.name for label in note.labels.all()]
    })


def main():
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
    