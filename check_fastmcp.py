import inspect
from mcp.server import FastMCP

# Check the signature of FastMCP
sig = inspect.signature(FastMCP.__init__)
print(f"FastMCP.__init__ signature: {sig}")

# Check the docstring if available
print(f"FastMCP docstring: {FastMCP.__doc__}")