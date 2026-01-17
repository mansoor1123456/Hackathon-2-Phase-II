from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List, Optional
from ...database.session import get_session
from ...models.todo import Todo, TodoCreate, TodoUpdate, TodoPublic
from ...models.user import User
from ...auth.middleware import get_current_user
from ...services.todo_service import TodoService
from uuid import UUID
import re

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("/", response_model=List[TodoPublic])
def get_todos(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    status: Optional[str] = Query(None, regex="^(all|completed|incomplete)$")
):
    """
    Retrieve all todos for the authenticated user.
    """
    todos, total_count = TodoService.get_todos_for_user(
        session=session,
        user_id=current_user['id'],
        limit=limit,
        offset=offset,
        status=status
    )

    return todos


@router.post("/", response_model=TodoPublic)
def create_todo(
    todo: TodoCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new todo for the authenticated user.
    """
    created_todo = TodoService.create_todo(
        session=session,
        todo_data=todo,
        user_id=current_user['id']
    )

    return created_todo


@router.get("/{todo_id}", response_model=TodoPublic)
def get_todo(
    todo_id: UUID,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve a specific todo for the authenticated user.
    """
    todo = TodoService.get_todo_by_id(
        session=session,
        todo_id=todo_id,
        user_id=current_user['id']
    )

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    return todo


@router.put("/{todo_id}", response_model=TodoPublic)
def update_todo(
    todo_id: UUID,
    todo_update: TodoUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Update a specific todo for the authenticated user.
    """
    updated_todo = TodoService.update_todo(
        session=session,
        todo_id=todo_id,
        todo_data=todo_update,
        user_id=current_user['id']
    )

    if not updated_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    return updated_todo


@router.delete("/{todo_id}")
def delete_todo(
    todo_id: UUID,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a specific todo for the authenticated user.
    """
    success = TodoService.delete_todo(
        session=session,
        todo_id=todo_id,
        user_id=current_user['id']
    )

    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")

    return {"message": "Todo deleted successfully"}