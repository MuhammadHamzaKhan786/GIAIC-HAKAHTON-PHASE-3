import sys
import os

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Now try importing the server
try:
    from backend.mcp.tool_implementations import server
    print(f'MCP Server created successfully with {len(server._tools)} tools registered')
    print('Tools registered:', list(server._tools.keys()))
except Exception as e:
    print(f'Error importing server: {e}')
    import traceback
    traceback.print_exc()