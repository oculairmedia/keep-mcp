#!/usr/bin/env python3
"""
Standalone HTTP server for Google Keep MCP.
This can be used to run the server as an HTTP service.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from server.cli import mcp

async def run_http_server():
    """Run the Google Keep MCP server with HTTP transport."""
    host = os.getenv("MCP_HOST", "0.0.0.0")  # Default to 0.0.0.0 for Docker
    port = int(os.getenv("MCP_PORT", "8000"))
    path = os.getenv("MCP_PATH", "/mcp")
    
    print(f"Starting Google Keep MCP Server with HTTP transport")
    print(f"MCP endpoint: http://{host}:{port}/mcp/")
    
    try:
        # FastMCP uses settings to configure host and port
        # We need to update the settings before running
        mcp.settings.host = host
        mcp.settings.port = port
        
        # Use FastMCP's built-in streamable HTTP transport
        await mcp.run_streamable_http_async()
        
    except KeyboardInterrupt:
        print("\nShutting down server...")
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(run_http_server())