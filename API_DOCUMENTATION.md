# Google Keep MCP & REST API Documentation

## Overview

This project now includes both:
1. **Google Keep MCP Server** - Model Context Protocol server for AI assistants
2. **Google Keep REST API** - Full REST API for standard HTTP access

## Services

### 1. Google Keep MCP Server
- **Port**: 8000
- **MCP Endpoint**: `http://localhost:8000/mcp/`
- **Protocol**: MCP over HTTP (Server-Sent Events)
- **Use Case**: Integration with AI assistants like Claude Code

### 2. Google Keep REST API
- **Port**: 8001
- **Base URL**: `http://localhost:8001`
- **Health Check**: `http://localhost:8001/health`
- **Documentation**: `http://localhost:8001/docs` (Swagger UI)
- **Use Case**: Standard REST API access for any HTTP client

## REST API Endpoints

### Health Check
```bash
GET /health
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-12T14:11:15.474034",
  "service": "google-keep-rest-api",
  "google_keep_connected": true,
  "version": "1.0.0"
}
```

### List All Notes
```bash
GET /api/notes
```

**Response:**
```json
{
  "notes": [
    {
      "id": "1753881285774.973567934",
      "title": "My Note",
      "text": "Note content",
      "pinned": false,
      "color": "DEFAULT",
      "labels": []
    }
  ],
  "count": 1
}
```

### Search Notes
```bash
GET /api/notes/search?query=search_term
```

**Example:**
```bash
curl "http://localhost:8001/api/notes/search?query=important"
```

### Get Specific Note
```bash
GET /api/notes/{note_id}
```

**Example:**
```bash
curl http://localhost:8001/api/notes/1753881285774.973567934
```

### Create Note
```bash
POST /api/notes
Content-Type: application/json

{
  "title": "New Note",
  "text": "Note content"
}
```

**Example:**
```bash
curl -X POST http://localhost:8001/api/notes \
  -H "Content-Type: application/json" \
  -d '{"title": "Shopping List", "text": "Milk, Eggs, Bread"}'
```

### Update Note
```bash
PUT /api/notes/{note_id}
Content-Type: application/json

{
  "title": "Updated Title",
  "text": "Updated content"
}
```

**Example:**
```bash
curl -X PUT http://localhost:8001/api/notes/1753881285774.973567934 \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Shopping List", "text": "Milk, Eggs, Bread, Cheese"}'
```

### Delete Note
```bash
DELETE /api/notes/{note_id}
```

**Example:**
```bash
curl -X DELETE http://localhost:8001/api/notes/1753881285774.973567934
```

## Security Features

### Keep-MCP Label Protection
By default, the API can only modify notes that have the `keep-mcp` label. This prevents accidental modification of important notes.

- Notes created via the API automatically get the `keep-mcp` label
- To allow modification of all notes, set `UNSAFE_MODE=true` in `.env`

## Docker Management

### Start Services
```bash
cd "/opt/stacks/Google Keep MCP"
docker-compose up -d
```

### Stop Services
```bash
docker-compose down
```

### View Logs
```bash
# MCP Server logs
docker logs keep-mcp-server

# REST API logs
docker logs keep-rest-api

# Follow logs in real-time
docker logs -f keep-rest-api
```

### Restart Services
```bash
# Restart both services
docker-compose restart

# Restart specific service
docker restart keep-rest-api
```

### Check Service Health
```bash
# Check container status
docker ps | grep keep

# Check health endpoints
curl http://localhost:8001/health
```

## Configuration

### Environment Variables (.env)
```bash
# MCP Server Configuration
MCP_HOST=127.0.0.1
MCP_PORT=8000

# REST API Configuration
REST_API_PORT=8001

# Google Keep Credentials
GOOGLE_EMAIL=your-email@gmail.com
GOOGLE_MASTER_TOKEN=your_master_token_here

# Safety Mode
UNSAFE_MODE=false  # Set to 'true' to allow modification of all notes
```

### Docker Compose Services

Both services are configured in `docker-compose.yml`:
- **keep-mcp**: MCP protocol server on port 8000
- **keep-rest-api**: REST API on port 8001

Both services include:
- Health checks every 30 seconds
- Automatic restart on failure
- Shared data volume for persistence
- Access to Google Keep via same credentials

## Testing the APIs

### Test REST API
```bash
# Health check
curl http://localhost:8001/health | jq .

# List all notes
curl http://localhost:8001/api/notes | jq .

# Search for notes
curl "http://localhost:8001/api/notes/search?query=todo" | jq .

# Create a test note
curl -X POST http://localhost:8001/api/notes \
  -H "Content-Type: application/json" \
  -d '{"title": "Test", "text": "This is a test note"}' | jq .
```

### Interactive API Documentation
Visit `http://localhost:8001/docs` for interactive Swagger UI documentation where you can:
- View all endpoints
- Test API calls directly in the browser
- See request/response schemas
- Try out different parameters

## Troubleshooting

### Port Already in Use
```bash
# Check what's using the port
lsof -i :8001

# Change the port in .env if needed
REST_API_PORT=8002
```

### Container Won't Start
```bash
# Check logs for errors
docker logs keep-rest-api

# Rebuild the container
docker-compose down
docker-compose build --no-cache keep-rest-api
docker-compose up -d
```

### Google Keep Authentication Issues
```bash
# Verify credentials in .env
cat .env | grep GOOGLE

# Test authentication
docker exec keep-rest-api python -c "from server.keep_api import get_client; get_client(); print('Auth successful')"
```

### Health Check Failures
```bash
# Check if service is running
docker ps | grep keep

# Check health endpoint directly
curl -v http://localhost:8001/health

# View detailed logs
docker logs keep-rest-api --tail 50
```

## MCP Server Integration

The MCP server on port 8000 provides the same functionality but using the Model Context Protocol, which is designed for AI assistant integration.

To use with Claude Code or other MCP clients, add the server configuration:
```json
{
  "name": "google-keep",
  "url": "http://localhost:8000/mcp/",
  "transport": "sse"
}
```

## Architecture

```
┌─────────────────────────────────────────┐
│         Docker Compose Stack            │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────────────────────────────┐   │
│  │   keep-mcp-server               │   │
│  │   Port: 8000                    │   │
│  │   Protocol: MCP/SSE             │   │
│  └──────────┬──────────────────────┘   │
│             │                           │
│  ┌──────────▼──────────────────────┐   │
│  │   Google Keep API Layer         │   │
│  │   (gkeepapi)                    │   │
│  └──────────┬──────────────────────┘   │
│             │                           │
│  ┌──────────▼──────────────────────┐   │
│  │   keep-rest-api                 │   │
│  │   Port: 8001                    │   │
│  │   Protocol: HTTP/REST           │   │
│  └─────────────────────────────────┘   │
│                                         │
└─────────────────────────────────────────┘
```

## Files Structure

```
/opt/stacks/Google Keep MCP/
├── docker-compose.yml          # Service definitions
├── Dockerfile                  # Container build config
├── .env                        # Environment variables
├── src/
│   └── server/
│       ├── cli.py              # MCP server implementation
│       ├── keep_api.py         # Google Keep client
│       ├── rest_api.py         # REST API implementation
│       └── standalone_http.py  # MCP HTTP server entry point
├── start_rest_api.sh           # REST API startup script
└── API_DOCUMENTATION.md        # This file
```

## Next Steps

1. **Access the interactive docs**: http://localhost:8001/docs
2. **Test the health endpoint**: `curl http://localhost:8001/health`
3. **List your notes**: `curl http://localhost:8001/api/notes`
4. **Create your first note via API**: See examples above
5. **Integrate with your application**: Use the REST API endpoints

## Support

For issues or questions:
1. Check the logs: `docker logs keep-rest-api`
2. Verify health: `curl http://localhost:8001/health`
3. Review this documentation
4. Check the original project: https://github.com/feuerdev/keep-mcp
