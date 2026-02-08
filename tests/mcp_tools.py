import pytest
from sqlmodel import create_engine, Session
from unittest.mock import patch
from backend.mcp.models.task import Task
from backend.mcp.tools import (
    AddTaskRequest, ListTasksRequest, CompleteTaskRequest,
    UpdateTaskRequest, DeleteTaskRequest, TaskStatus
)
from backend.mcp.tool_implementations import (
    add_task, list_tasks, complete_task, update_task, delete_task
)
from backend.mcp.errors import TaskNotFoundError, ValidationError


# Use an in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture
def mock_db_session():
    """Create a mock database session for testing"""
    engine = create_engine(TEST_DATABASE_URL, echo=True)
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


@pytest.fixture
def mock_user_id():
    """Mock user ID for testing"""
    return "test_user_123"


def test_add_task_success(mock_db_session, mock_user_id):
    """Test successful task creation"""
    # Patch the get_current_user_id_mock function
    with patch('backend.mcp.tool_implementations.get_current_user_id_mock', return_value=mock_user_id):
        request = AddTaskRequest(title="Test Task", description="Test Description")

        # We need to patch the get_session function to return our test session
        with patch('backend.mcp.tool_implementations.next') as mock_next:
            mock_next.return_value.__enter__.return_value = mock_db_session
            result = add_task(request)

        assert result.title == "Test Task"
        assert result.completed == False


def test_add_task_empty_title():
    """Test that adding a task with empty title raises ValidationError"""
    with patch('backend.mcp.tool_implementations.get_current_user_id_mock'):
        request = AddTaskRequest(title="", description="Test Description")

        with pytest.raises(ValidationError):
            add_task(request)


def test_list_tasks_success(mock_db_session, mock_user_id):
    """Test successful listing of tasks"""
    # Create a test task in the database
    test_task = Task(user_id=mock_user_id, title="Test Task", completed=False)
    mock_db_session.add(test_task)
    mock_db_session.commit()
    mock_db_session.refresh(test_task)

    # Patch the get_current_user_id_mock function
    with patch('backend.mcp.tool_implementations.get_current_user_id_mock', return_value=mock_user_id):
        request = ListTasksRequest(status=TaskStatus.ALL)

        # We need to patch the get_session function
        with patch('backend.mcp.tool_implementations.next') as mock_next:
            mock_next.return_value.__enter__.return_value = mock_db_session
            result = list_tasks(request)

        assert len(result.tasks) >= 1
        assert any(task.title == "Test Task" for task in result.tasks)


def test_complete_task_success(mock_db_session, mock_user_id):
    """Test successful task completion"""
    # Create a test task in the database
    test_task = Task(user_id=mock_user_id, title="Test Task", completed=False)
    mock_db_session.add(test_task)
    mock_db_session.commit()
    mock_db_session.refresh(test_task)

    # Patch the get_current_user_id_mock function
    with patch('backend.mcp.tool_implementations.get_current_user_id_mock', return_value=mock_user_id):
        request = CompleteTaskRequest(task_id=test_task.id)

        # We need to patch the get_session function
        with patch('backend.mcp.tool_implementations.next') as mock_next:
            mock_next.return_value.__enter__.return_value = mock_db_session
            result = complete_task(request)

        assert result.task_id == test_task.id
        assert result.completed == True


def test_complete_task_not_found(mock_db_session, mock_user_id):
    """Test that completing a non-existent task raises TaskNotFoundError"""
    with patch('backend.mcp.tool_implementations.get_current_user_id_mock', return_value=mock_user_id):
        request = CompleteTaskRequest(task_id=99999)

        # We need to patch the get_session function
        with patch('backend.mcp.tool_implementations.next') as mock_next:
            mock_next.return_value.__enter__.return_value = mock_db_session

            with pytest.raises(TaskNotFoundError):
                complete_task(request)


def test_update_task_success(mock_db_session, mock_user_id):
    """Test successful task update"""
    # Create a test task in the database
    test_task = Task(user_id=mock_user_id, title="Old Title", completed=False)
    mock_db_session.add(test_task)
    mock_db_session.commit()
    mock_db_session.refresh(test_task)

    # Patch the get_current_user_id_mock function
    with patch('backend.mcp.tool_implementations.get_current_user_id_mock', return_value=mock_user_id):
        request = UpdateTaskRequest(task_id=test_task.id, title="New Title")

        # We need to patch the get_session function
        with patch('backend.mcp.tool_implementations.next') as mock_next:
            mock_next.return_value.__enter__.return_value = mock_db_session
            result = update_task(request)

        assert result.task_id == test_task.id
        assert result.title == "New Title"


def test_update_task_no_fields(mock_db_session, mock_user_id):
    """Test that updating a task without any fields raises ValidationError"""
    with patch('backend.mcp.tool_implementations.get_current_user_id_mock', return_value=mock_user_id):
        request = UpdateTaskRequest(task_id=1, title=None, description=None)

        with pytest.raises(ValidationError):
            update_task(request)


def test_delete_task_success(mock_db_session, mock_user_id):
    """Test successful task deletion"""
    # Create a test task in the database
    test_task = Task(user_id=mock_user_id, title="Test Task", completed=False)
    mock_db_session.add(test_task)
    mock_db_session.commit()
    mock_db_session.refresh(test_task)

    # Verify task exists before deletion
    from sqlmodel import select
    stmt = select(Task).where(Task.id == test_task.id)
    existing_task = mock_db_session.exec(stmt).first()
    assert existing_task is not None

    # Patch the get_current_user_id_mock function
    with patch('backend.mcp.tool_implementations.get_current_user_id_mock', return_value=mock_user_id):
        request = DeleteTaskRequest(task_id=test_task.id)

        # We need to patch the get_session function
        with patch('backend.mcp.tool_implementations.next') as mock_next:
            mock_next.return_value.__enter__.return_value = mock_db_session
            result = delete_task(request)

        assert result.task_id == test_task.id
        assert result.status == "deleted"


def test_delete_task_not_found(mock_db_session, mock_user_id):
    """Test that deleting a non-existent task raises TaskNotFoundError"""
    with patch('backend.mcp.tool_implementations.get_current_user_id_mock', return_value=mock_user_id):
        request = DeleteTaskRequest(task_id=99999)

        # We need to patch the get_session function
        with patch('backend.mcp.tool_implementations.next') as mock_next:
            mock_next.return_value.__enter__.return_value = mock_db_session

            with pytest.raises(TaskNotFoundError):
                delete_task(request)