#!/usr/bin/env python3
"""
Enhanced standalone HTTP server for Google Keep MCP with health check endpoint.
"""

import asyncio
import os
import sys
from pathlib import Path
from starlette.responses import JSONResponse

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from server.cli import mcp
from server.keep_api import get_client

# Add health check endpoint using FastMCP's decorator
@mcp.custom_route("/health", ["GET"])
async def health_check(request):
    """Health check endpoint for monitoring."""
    try:
        # Try to get the Keep client to verify connection
        keep = get_client()
        return JSONResponse({
            "status": "healthy",
            "service": "google-keep-mcp",
            "google_keep_connected": True
        })
    except Exception as e:
        return JSONResponse({
            "status": "unhealthy",
            "service": "google-keep-mcp",
            "google_keep_connected": False,
            "error": str(e)
        }, status_code=503)

@mcp.custom_route("/api/health", ["GET"])
async def api_health_check(request):
    """Alternative health check endpoint."""
    return await health_check(request)

async def run_http_server():
    """Run the Google Keep MCP server with HTTP transport and health endpoint."""
    host = os.getenv("MCP_HOST", "0.0.0.0")
    port = int(os.getenv("MCP_PORT", "8000"))
    path = os.getenv("MCP_PATH", "/mcp")

    print(f"Starting Google Keep MCP Server with HTTP transport")
    print(f"MCP endpoint: http://{host}:{port}{path}/")
    print(f"Health check: http://{host}:{port}/health")

    try:
        # Configure FastMCP settings
        mcp.settings.host = host
        mcp.settings.port = port

        # Run the streamable HTTP server
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
