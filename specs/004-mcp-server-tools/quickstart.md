# Quickstart: MCP Server & Task Tooling

## Overview

This guide helps you set up and run the MCP server that exposes task management functionality as stateless tools for OpenAI Agents.

## Prerequisites

- Python 3.11+
- PostgreSQL-compatible database (Neon recommended)
- OpenAI API key (for agent integration)
- MCP-compatible client (OpenAI Agents SDK)

## Setup Instructions

### 1. Clone and Navigate
```bash
# The MCP server will be in the mcp-server directory
cd mcp-server
```

### 2. Environment Configuration
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your specific configurations:
# - DATABASE_URL: PostgreSQL connection string
# - JWT_SECRET_KEY: Secret for JWT token verification
# - OPENAI_API_KEY: API key for OpenAI integration (if needed)
```

### 3. Virtual Environment and Dependencies
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Database Setup
```bash
# Run database migrations
python -m src.database.migrations

# Or if using alembic:
alembic upgrade head
```

### 5. Run the Server
```bash
# Start the MCP server
python -m src.main

# The server will start and expose the MCP tools
```

## Available Tools

Once running, the server exposes these MCP tools:

### add_task
```json
{
  "params": {
    "title": "Task title (required)",
    "description": "Task description (optional)"
  }
}
```

### list_tasks
```json
{
  "params": {
    "status": "Filter by status: all|pending|completed (optional, defaults to all)"
  }
}
```

### complete_task
```json
{
  "params": {
    "task_id": "ID of the task to complete (required)"
  }
}
```

### update_task
```json
{
  "params": {
    "task_id": "ID of the task to update (required)",
    "title": "New title (optional)",
    "description": "New description (optional)"
  }
}
```

### delete_task
```json
{
  "params": {
    "task_id": "ID of the task to delete (required)"
  }
}
```

## Testing the Server

### Run Unit Tests
```bash
pytest tests/unit/
```

### Run Integration Tests
```bash
pytest tests/integration/
```

### Manual Tool Testing
With the server running, you can test tools using the MCP client:

```bash
# Example: Test the add_task tool
curl -X POST http://localhost:8000/tools \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "tool": "add_task",
    "params": {
      "title": "Test task",
      "description": "Test description"
    }
  }'
```

## Development

### Adding New Tools
1. Create a new tool file in `src/tools/`
2. Define the tool using the MCP SDK
3. Register the tool in the main server configuration
4. Add tests for the new tool

### Running in Development Mode
```bash
# With auto-reload for development
uvicorn src.main:app --reload --port 8000
```

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify `DATABASE_URL` in your `.env` file
   - Ensure the database server is running
   - Check that your credentials are correct

2. **JWT Authentication Error**
   - Verify `JWT_SECRET_KEY` in your `.env` file
   - Ensure the JWT token is properly formatted and not expired
   - Confirm the token contains the required user_id

3. **Tool Not Found Error**
   - Check that the tool is properly registered in the server
   - Verify the tool name matches exactly what the agent expects

### Getting Help
- Check the server logs for detailed error messages
- Review the MCP specification for proper tool usage
- Consult the tool documentation in the main README