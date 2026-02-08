import inspect
from mcp.server import FastMCP

# Create an instance to check the method
server = FastMCP(name="test")

# Check the signature of add_tool
sig = inspect.signature(server.add_tool)
print(f"FastMCP.add_tool signature: {sig}")

# Check what arguments add_tool expects
print("add_tool method docstring:", server.add_tool.__doc__ if server.add_tool.__doc__ else "No docstring")