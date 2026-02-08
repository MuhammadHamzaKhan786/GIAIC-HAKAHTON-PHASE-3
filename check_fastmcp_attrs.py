import inspect
from mcp.server import FastMCP

# Create an instance to check its attributes
server = FastMCP(name="test")

print("FastMCP attributes:")
attrs = [attr for attr in dir(server) if not attr.startswith('_')]
for attr in attrs:
    print(f"  {attr}")

print("\nFastMCP methods:")
methods = [attr for attr in dir(server) if not attr.startswith('_') and callable(getattr(server, attr))]
for method in methods:
    print(f"  {method}")

print(f"\nHas 'app' attribute: {hasattr(server, 'app')}")
print(f"Has 'mount' attribute: {hasattr(server, 'mount')}")
print(f"Has 'routes' attribute: {hasattr(server, 'routes')}")

# Check for any attribute that might be related to mounting or serving
relevant_attrs = [attr for attr in attrs if any(keyword in attr.lower() for keyword in ['mount', 'serve', 'router', 'handler', 'route', 'api'])]
print(f"\nPotentially relevant attributes: {relevant_attrs}")