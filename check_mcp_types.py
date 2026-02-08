import mcp.server
import inspect

print("MCP Server types available:")
for item in dir(mcp.server):
    if not item.startswith('_'):
        obj = getattr(mcp.server, item)
        if inspect.isclass(obj):
            print(f"Class: {item}")
            print(f"  - Methods: {[m for m in dir(obj) if not m.startswith('_')][:10]}")  # Show first 10 methods