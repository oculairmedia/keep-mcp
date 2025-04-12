"""
MCP plugin for Google Keep integration.
Provides tools for interacting with Google Keep notes through MCP.
"""

import json
from mcp.server.fastmcp import FastMCP
from .keep_api import get_client

mcp = FastMCP("keep")

@mcp.tool()
def find(query="") -> str:
    """
    Find notes based on a search query.
    
    Args:
        query (str, optional): A string to match against the title and text
        
    Returns:
        str: JSON string containing the matching notes with their id, title, text, pinned status, color and labels
    """
    keep = get_client()
    notes = keep.find(query=query, archived=False, trashed=False)
    
    notes_data = []
    for note in notes:
        note_data = {
            'id': note.id,
            'title': note.title,
            'text': note.text,
            'pinned': note.pinned,
            'color': note.color.value if note.color else None,
            'labels': [{'id': label.id, 'name': label.name} for label in note.labels.all()]
        }
        notes_data.append(note_data)
    
    return json.dumps(notes_data)


def main():
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
    