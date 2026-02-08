#!/bin/bash

# Start the MCP Task Server
echo "Starting MCP Task Server..."

# Change to the MCP directory
cd backend/mcp

# Start the server using uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

echo "MCP Task Server stopped."