import os
from dotenv import load_dotenv
from fastapi import FastAPI
from .tool_registry import server as mcp_server

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="MCP Task Server", version="1.0.0")

# Import tools to register them with the server
from . import tool_registry

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "mcp-task-server"}

# Add a simple root endpoint
@app.get("/")
async def root():
    return {"message": "MCP Task Server - Ready to serve task management tools"}

# Mount the MCP server
# Get the streamable HTTP app from the MCP server
mcp_app = mcp_server.streamable_http_app()

# Add the MCP endpoints to FastAPI app
app.mount("/mcp", mcp_app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)