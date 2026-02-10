#!/usr/bin/env python3
"""
Mock Google Keep MCP server for testing HTTP transport
"""

import json
import asyncio
from mcp.server.fastmcp import FastMCP

# Mock data
mock_notes = [
    {
        "id": "mock-1",
        "title": "Test Note 1",
        "text": "This is a mock note for testing",
        "pinned": False,
        "color": None,
        "labels": [{"id": "label-1", "name": "keep-mcp"}]
    },
    {
        "id": "mock-2", 
        "title": "Shopping List",
        "text": "- Milk\n- Bread\n- Eggs",
        "pinned": True,
        "color": "BLUE",
        "labels": []
    }
]

mcp = FastMCP("mock-keep")

@mcp.tool()
def find(query="") -> str:
    """Find mock notes based on query."""
    filtered_notes = [note for note in mock_notes if query.lower() in note['title'].lower() or query.lower() in note['text'].lower()]
    return json.dumps(filtered_notes)

@mcp.tool()
def create_note(title: str = None, text: str = None) -> str:
    """Create a mock note."""
    new_note = {
        "id": f"mock-{len(mock_notes) + 1}",
        "title": title or "Untitled",
        "text": text or "",
        "pinned": False,
        "color": None,
        "labels": [{"id": "label-1", "name": "keep-mcp"}]
    }
    mock_notes.append(new_note)
    return json.dumps(new_note)

@mcp.tool()
def update_note(note_id: str, title: str = None, text: str = None) -> str:
    """Update a mock note."""
    for note in mock_notes:
        if note['id'] == note_id:
            if title is not None:
                note['title'] = title
            if text is not None:
                note['text'] = text
            return json.dumps(note)
    raise ValueError(f"Note {note_id} not found")

@mcp.tool()
def delete_note(note_id: str) -> str:
    """Delete a mock note."""
    global mock_notes
    mock_notes = [note for note in mock_notes if note['id'] != note_id]
    return json.dumps({"message": f"Note {note_id} deleted"})

async def main():
    print("🧪 Starting Mock Google Keep MCP Server")
    print("This allows you to test the HTTP transport without Google authentication")
    print("Available at: http://localhost:8000/mcp")
    print("Health check: http://localhost:8000/health")
    print()
    await mcp.run_sse_async(host="127.0.0.1", port=8000)

if __name__ == "__main__":
    asyncio.run(main())