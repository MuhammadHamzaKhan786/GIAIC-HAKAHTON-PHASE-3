from mcp.server import Server
from mcp import Tool
from pydantic import BaseModel
import inspect

# Create a test server
server = Server("test-task-server")

# Define a simple input and output model
class TestInput(BaseModel):
    message: str

class TestOutput(BaseModel):
    response: str

# Create a simple test function
def test_function(input_data: TestInput) -> TestOutput:
    return TestOutput(response=f"Received: {input_data.message}")

# Try to create a tool definition using the Tool class
print("Creating a test tool...")
try:
    # Create tool using the Tool constructor
    test_tool = Tool(
        name="test_tool",
        title="Test Tool",
        description="A test tool for verification",
        inputSchema=TestInput.model_json_schema(),
        outputSchema=TestOutput.model_json_schema()
    )

    print(f"Tool created: {test_tool}")
    print(f"Tool name: {test_tool.name}")

    # Check if we can register this tool with the server
    # Let's see how to register tools

    # Check the methods again
    print(f"\nServer methods containing 'tool': {[method for method in dir(server) if 'tool' in method.lower()]}")

    # It looks like the server might automatically discover tools that are registered
    # Let's look at the implementation more closely
    print(f"\nServer has call_tool method: {hasattr(server, 'call_tool')}")
    print(f"Server has list_tools method: {hasattr(server, 'list_tools')}")

    # Try to see how to register a function as a tool
    tools_before = server.list_tools()
    print(f"Tools before: {tools_before}")

except Exception as e:
    print(f"Error creating tool: {e}")
    import traceback
    traceback.print_exc()

# Let's see if there are examples in the documentation or if we need to approach it differently
print("\nInvestigating the correct approach...")
print("Based on the available methods, we might need to register tools differently.")
print("Let's check how other MCP servers register tools.")

# Since the typical @server.tool() decorator approach didn't work,
# let's try a different approach by manually adding to the server