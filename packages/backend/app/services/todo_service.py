from sqlmodel import Session, select, func
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from ..models.todo import Todo, TodoCreate, TodoUpdate
from ..models.user import User


class TodoService:
    @staticmethod
    def get_todo_by_id(session: Session, todo_id: UUID, user_id: UUID) -> Optional[Todo]:
        """Get a todo by its ID for a specific user"""
        statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
        return session.exec(statement).first()

    @staticmethod
    def get_todos_for_user(
        session: Session,
        user_id: UUID,
        limit: int = 20,
        offset: int = 0,
        status: Optional[str] = None
    ) -> tuple[List[Todo], int]:
        """Get all todos for a specific user with optional filtering"""
        query = select(Todo).where(Todo.user_id == user_id)

        # Apply status filter if provided
        if status:
            if status.lower() == 'completed':
                query = query.where(Todo.completed == True)
            elif status.lower() == 'incomplete':
                query = query.where(Todo.completed == False)

        # Get total count for pagination
        count_query = select(func.count(Todo.id)).where(Todo.user_id == user_id)
        if status:
            if status.lower() == 'completed':
                count_query = count_query.where(Todo.completed == True)
            elif status.lower() == 'incomplete':
                count_query = count_query.where(Todo.completed == False)

        total_count = session.exec(count_query).first()

        # Apply ordering and pagination
        query = query.order_by(Todo.created_at.desc()).offset(offset).limit(limit)

        todos = session.exec(query).all()

        return todos, total_count

    @staticmethod
    def create_todo(session: Session, todo_data: TodoCreate, user_id: UUID) -> Todo:
        """Create a new todo for a specific user"""
        todo = Todo(
            title=todo_data.title,
            description=todo_data.description,
            completed=todo_data.completed,
            user_id=user_id
        )

        session.add(todo)
        session.commit()
        session.refresh(todo)

        return todo

    @staticmethod
    def update_todo(session: Session, todo_id: UUID, todo_data: TodoUpdate, user_id: UUID) -> Optional[Todo]:
        """Update a todo for a specific user"""
        todo = TodoService.get_todo_by_id(session, todo_id, user_id)

        if not todo:
            return None

        # Update fields if they are provided
        if todo_data.title is not None:
            todo.title = todo_data.title
        if todo_data.description is not None:
            todo.description = todo_data.description
        if todo_data.completed is not None:
            todo.completed = todo_data.completed

        # Update the timestamp
        todo.updated_at = datetime.utcnow()

        session.add(todo)
        session.commit()
        session.refresh(todo)

        return todo

    @staticmethod
    def delete_todo(session: Session, todo_id: UUID, user_id: UUID) -> bool:
        """Delete a todo for a specific user"""
        todo = TodoService.get_todo_by_id(session, todo_id, user_id)

        if not todo:
            return False

        session.delete(todo)
        session.commit()

        return True