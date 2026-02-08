from mcp.server import Server
from mcp import Tool
from pydantic import BaseModel

# Create a test server
server = Server("explore-pattern-server")

# Let me try a different approach, maybe using the decorator pattern
# The fact that list_tools returns a decorator-like function suggests
# that we need to use decorators differently

# Define a test function
def sample_task_func():
    """A sample function to test decorator approach."""
    pass

# Look for the decorator approach in the server
print("Testing if we can use server decorators...")

# Try using the call_tool method
print(f"call_tool method: {server.call_tool}")

# Since the MCP framework is probably using a different pattern,
# let me check if there's a decorator attached to the server

# Let me see if the server itself can act as a decorator for tool functions
# Based on the MCP documentation and patterns, it might work like this:

# Define input/output models
class EchoInput(BaseModel):
    text: str

class EchoOutput(BaseModel):
    echoed_text: str

# Rather than using a decorator directly, we may need to register tools differently
# Let me check the server methods again for any hints

# Let's look for attributes/methods that might hold registered functions
server_attrs = [attr for attr in dir(server) if not attr.startswith('_')]
print("Server attributes:", server_attrs)

# Let's see if there are attributes that might indicate how tools are registered
possible_tool_attrs = [attr for attr in server_attrs if any(word in attr.lower() for word in ['tool', 'handler', 'func', 'call'])]
print("Possible tool-related attributes:", possible_tool_attrs)

# Let me also check if there are any methods for registering tool functions
import inspect

print("\nInspecting call_tool signature:")
try:
    sig = inspect.signature(server.call_tool)
    print(sig)
except:
    print("No signature available for call_tool")

print("\nInspecting list_tools signature:")
try:
    sig = inspect.signature(server.list_tools)
    print(sig)
except:
    print("No signature available for list_tools")

# The approach might be to use the server's request_handlers
print(f"\nrequest_handlers: {getattr(server, 'request_handlers', 'Not found')}")

# Let me try to see if there are any experimental or advanced methods
print(f"\nexperimental: {getattr(server, 'experimental', 'Not found')}")

# Actually, looking back at the output from earlier, list_tools returned
# a decorator function, which suggests we might need to do something like:
# @server.list_tools
# def my_tool_function(...):
#     ...
# But that doesn't seem right based on the return type.

# Let me check the MCP documentation approach by seeing if there are examples online
# Based on typical patterns, maybe it's like this:

# Create a proper tool
tool = Tool(
    name="echo_tool",
    title="Echo Tool",
    description="Repeats the input text",
    inputSchema=EchoInput.model_json_schema(),
    outputSchema=EchoOutput.model_json_schema()
)

print(f"\nCreated tool: {tool}")

# So maybe the pattern is different - maybe we register tools in a different way
# or maybe we need to register the function handlers separately