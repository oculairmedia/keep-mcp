"""
MCP plugin for Google Keep integration.
Provides tools for interacting with Google Keep notes through MCP.
"""

import json
from mcp.server.fastmcp import FastMCP
from .keep_api import get_client

mcp = FastMCP("keep")

@mcp.tool()
def find(query=None, labels=None, colors=None, pinned=None, archived=None, trashed=False) -> str:
    """
    Find notes based on various criteria.
    
    Args:
        query (str, optional): A string to match against the title and text
        labels (list, optional): A list of label IDs to match
        colors (list, optional): A list of colors to match
        pinned (bool, optional): Whether to match pinned notes
        archived (bool, optional): Whether to match archived notes
        trashed (bool, optional): Whether to match trashed notes (default: False)
        
    Returns:
        str: JSON string containing the matching notes
    """
    keep = get_client()
    notes = keep.find(query=query, labels=labels, colors=colors, pinned=pinned, archived=archived, trashed=trashed)
    return notes


def main():
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
    