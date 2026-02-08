import inspect
from mcp.server import Server

# Let's examine the Server class to see what methods are available
server_instance = Server("test-server")

print("Server methods and attributes:")
for attr in dir(server_instance):
    if not attr.startswith('_'):  # Filter out private attributes
        print(f"- {attr}")

# Check if there's a decorator method
print("\nChecking for tool registration method...")
print(f"Has 'tool': {'tool' in dir(server_instance)}")
print(f"Has 'register_tool': {'register_tool' in dir(server_instance)}")
print(f"Has 'add_tool': {'add_tool' in dir(server_instance)}")
print(f"Has '__call__': {'__call__' in dir(server_instance)}")

# Try to inspect what methods are available
import mcp
print(f"\nMCP module contents: {[item for item in dir(mcp) if not item.startswith('_')]}")

import mcp.server
print(f"\nMCP server module contents: {[item for item in dir(mcp.server) if not item.startswith('_')]}")