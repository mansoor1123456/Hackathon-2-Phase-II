import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import TodoItem from '../components/TodoItem';
import { Todo } from '../../shared/types/todo';

describe('TodoItem Component', () => {
  const mockTodo: Todo = {
    id: '1',
    title: 'Test Todo',
    description: 'Test Description',
    completed: false,
    userId: 'user1',
    createdAt: '2023-01-01T00:00:00Z',
    updatedAt: '2023-01-01T00:00:00Z',
  };

  const mockOnToggleComplete = jest.fn();
  const mockOnDelete = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders todo title and description', () => {
    const { getByText } = render(
      <TodoItem
        todo={mockTodo}
        onToggleComplete={mockOnToggleComplete}
        onDelete={mockOnDelete}
      />
    );

    expect(getByText('Test Todo')).toBeInTheDocument();
    expect(getByText('Test Description')).toBeInTheDocument();
  });

  it('calls onToggleComplete when checkbox is clicked', () => {
    const { getByRole } = render(
      <TodoItem
        todo={mockTodo}
        onToggleComplete={mockOnToggleComplete}
        onDelete={mockOnDelete}
      />
    );

    const checkbox = getByRole('checkbox');
    fireEvent.click(checkbox);

    expect(mockOnToggleComplete).toHaveBeenCalledWith(mockTodo);
  });

  it('calls onDelete when delete button is clicked', () => {
    const { getByText } = render(
      <TodoItem
        todo={mockTodo}
        onToggleComplete={mockOnToggleComplete}
        onDelete={mockOnDelete}
      />
    );

    const deleteButton = getByText('Delete');
    fireEvent.click(deleteButton);

    expect(mockOnDelete).toHaveBeenCalledWith('1');
  });

  it('displays completed todos with strikethrough', () => {
    const completedTodo = { ...mockTodo, completed: true };

    const { getByText } = render(
      <TodoItem
        todo={completedTodo}
        onToggleComplete={mockOnToggleComplete}
        onDelete={mockOnDelete}
      />
    );

    const titleElement = getByText('Test Todo');
    expect(titleElement).toHaveClass('line-through');
  });

  it('does not show description if not provided', () => {
    const todoWithoutDescription = { ...mockTodo, description: undefined };

    const { queryByText } = render(
      <TodoItem
        todo={todoWithoutDescription}
        onToggleComplete={mockOnToggleComplete}
        onDelete={mockOnDelete}
      />
    );

    expect(queryByText('Test Description')).not.toBeInTheDocument();
  });
});