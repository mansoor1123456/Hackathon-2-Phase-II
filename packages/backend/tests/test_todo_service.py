import pytest
from unittest.mock import Mock
from sqlmodel import Session, select
from app.models.todo import Todo, TodoCreate
from app.services.todo_service import TodoService
from uuid import UUID


def test_create_todo():
    """Test creating a todo"""
    # Mock session
    session = Mock(spec=Session)

    # Create test data
    todo_data = TodoCreate(
        title="Test Todo",
        description="Test Description",
        completed=False
    )
    user_id = UUID(int=1)

    # Mock the session.add and session.commit behavior
    created_todo = Todo(
        id=UUID(int=2),
        title=todo_data.title,
        description=todo_data.description,
        completed=todo_data.completed,
        user_id=user_id
    )

    session.add.return_value = None
    session.commit.return_value = None
    session.refresh.return_value = None

    # Call the service method
    result = TodoService.create_todo(session, todo_data, user_id)

    # Assertions
    assert result.title == "Test Todo"
    assert result.description == "Test Description"
    assert result.completed is False
    assert result.user_id == user_id
    session.add.assert_called_once()
    session.commit.assert_called_once()


def test_get_todo_by_id():
    """Test getting a todo by ID"""
    session = Mock(spec=Session)
    todo_id = UUID(int=1)
    user_id = UUID(int=2)

    # Create a mock todo
    expected_todo = Todo(
        id=todo_id,
        title="Test Todo",
        description="Test Description",
        completed=False,
        user_id=user_id
    )

    # Mock the exec method to return the todo
    mock_exec_result = Mock()
    mock_exec_result.first.return_value = expected_todo
    session.exec.return_value = mock_exec_result

    # Call the service method
    result = TodoService.get_todo_by_id(session, todo_id, user_id)

    # Assertions
    assert result == expected_todo
    assert result.id == todo_id
    assert result.user_id == user_id


def test_update_todo():
    """Test updating a todo"""
    session = Mock(spec=Session)
    todo_id = UUID(int=1)
    user_id = UUID(int=2)

    # Create an existing todo
    existing_todo = Todo(
        id=todo_id,
        title="Old Title",
        description="Old Description",
        completed=False,
        user_id=user_id
    )

    # Create update data
    update_data = TodoCreate(
        title="Updated Title",
        description="Updated Description",
        completed=True
    )

    # Mock the session behavior
    session.add.return_value = None
    session.commit.return_value = None
    session.refresh.return_value = None

    # Mock the get_todo_by_id to return the existing todo
    TodoService.get_todo_by_id = Mock(return_value=existing_todo)

    # Call the service method
    result = TodoService.update_todo(session, todo_id, update_data, user_id)

    # Assertions
    assert result is not None
    assert result.title == "Updated Title"
    assert result.description == "Updated Description"
    assert result.completed is True
    session.add.assert_called_once()
    session.commit.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__])