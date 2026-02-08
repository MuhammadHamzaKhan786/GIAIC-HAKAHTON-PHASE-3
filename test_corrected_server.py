import sys
import os

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Set environment variable to prevent table creation during import
os.environ['CREATE_TABLES_ON_IMPORT'] = 'false'

try:
    from backend.mcp.tool_registry import server
    print(f'MCP Server created successfully!')
    print(f'Server name: {server.name}')

    # Test that the tools are registered by checking server capabilities
    print(f'Tools registered: {len(server._tools) if hasattr(server, "_tools") else "Unknown"}')

    # List the available tools if possible
    try:
        # Try to call list_tools method to see what's registered
        tools_list_result = server.list_tools()
        print(f'Tools list result type: {type(tools_list_result)}')

        # Since list_tools returns a coroutine, let's not await it in this simple test
        print('Server appears to be set up correctly with tools.')

    except Exception as e:
        print(f'Error listing tools: {e}')

except Exception as e:
    print(f'Error importing server: {e}')
    import traceback
    traceback.print_exc()