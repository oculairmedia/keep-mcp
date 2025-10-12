FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy all project files
COPY . .

# Install Python dependencies
RUN pip install -e .

# Create data directory for persistent storage
RUN mkdir -p /app/data

# Expose port
EXPOSE 8000

# Set default environment variables
ENV MCP_HOST=0.0.0.0
ENV MCP_PORT=8000
ENV MCP_PATH=/mcp

# Run the HTTP server with health endpoint
CMD ["python", "src/server/standalone_http.py"]