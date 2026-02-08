import mcp
from mcp import Tool
import inspect

print("Available MCP Tool info:")
print(f"Tool type: {type(Tool)}")
print(f"Tool dir: {[item for item in dir(Tool) if not item.startswith('__')]}")

# Check how to create a tool using the Tool class
print("\nTrying to understand Tool signature:")
try:
    sig = inspect.signature(Tool)
    print(f"Tool signature: {sig}")
except Exception as e:
    print(f"Error getting Tool signature: {e}")

# Look at the server more carefully
from mcp.server import Server
server_instance = Server("test-server")

print(f"\nServer instance type: {type(server_instance)}")
print(f"Has 'tools' attribute: {hasattr(server_instance, 'tools')}")

# Check if there's an attribute where we can register tools
print("\nServer attributes that might be relevant:")
for attr in ['tools', 'registered_tools', '_tools', 'handlers', '_handlers', 'capabilities']:
    has_attr = hasattr(server_instance, attr)
    print(f"- {attr}: {has_attr}")
    if has_attr:
        try:
            val = getattr(server_instance, attr)
            print(f"  Value: {val}")
            print(f"  Type: {type(val)}")
        except Exception as e:
            print(f"  Error accessing: {e}")

print("\nTrying to check the Server class directly:")
server_class = Server
print(f"Server class methods that might be for tools: {[method for method in dir(server_class) if 'tool' in method.lower()]}")

# Let's also see if there's a decorator approach by looking for methods that might work as decorators
print(f"\nMethods that might be decorators: {[method for method in dir(server_class) if method in ['__call__', 'add_tool', 'register', 'tool', 'bind', 'handle', 'on_tool']]}")

# Maybe tools need to be added differently
print("\nExamining the list_tools method:")
if hasattr(server_instance, 'list_tools'):
    list_tools_method = getattr(server_instance, 'list_tools')
    print(f"list_tools method: {list_tools_method}")
    try:
        sig = inspect.signature(list_tools_method)
        print(f"list_tools signature: {sig}")
    except Exception as e:
        print(f"Error getting list_tools signature: {e}")