#!/bin/bash

# Google Keep MCP HTTP Server Startup Script

# Load environment variables if .env file exists
if [ -f .env ]; then
    echo "Loading environment variables from .env file..."
    export $(grep -v '^#' .env | xargs)
fi

# Set defaults if not set
export MCP_HOST=${MCP_HOST:-127.0.0.1}
export MCP_PORT=${MCP_PORT:-8000}
export MCP_PATH=${MCP_PATH:-/mcp}

echo "Starting Google Keep MCP Server..."
echo "Host: $MCP_HOST"
echo "Port: $MCP_PORT"
echo "Path: $MCP_PATH"
echo ""

# Check if Python dependencies are installed
if ! python -c "import mcp.server.fastmcp" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -e .
fi

# Start the server
python src/server/http_server.py