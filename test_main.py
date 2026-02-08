import sys
import os

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Set environment variable to prevent table creation during import
os.environ['CREATE_TABLES_ON_IMPORT'] = 'false'

try:
    # Try importing the main app
    from backend.mcp.main import app
    print(f'FastAPI app created successfully!')
    print(f'App title: {app.title}')

    # Check that the routes are mounted
    route_names = [route.name for route in app.routes if hasattr(route, 'name') and route.name]
    path_names = [route.path for route in app.routes]

    print(f'Available paths: {path_names[:10]}...')  # First 10 paths

    print('Main app loaded successfully.')

except Exception as e:
    print(f'Error importing main app: {e}')
    import traceback
    traceback.print_exc()