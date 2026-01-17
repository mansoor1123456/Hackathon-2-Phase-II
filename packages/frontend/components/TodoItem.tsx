import React from 'react';
import { Todo } from '../../shared/types/todo';

interface TodoItemProps {
  todo: Todo;
  onToggleComplete: (todo: Todo) => void;
  onDelete: (todoId: string) => void;
}

const TodoItem: React.FC<TodoItemProps> = ({ todo, onToggleComplete, onDelete }) => {
  return (
    <li className="px-4 py-4 sm:px-6 hover:bg-gray-50">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between space-y-2 sm:space-y-0">
        <div className="flex items-center">
          <input
            type="checkbox"
            checked={todo.completed}
            onChange={() => onToggleComplete(todo)}
            className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
          />
          <div className="ml-3 min-w-0">
            <p
              className={`text-sm font-medium ${
                todo.completed ? 'text-gray-500 line-through' : 'text-gray-900'
              }`}
            >
              {todo.title}
            </p>
            {todo.description && (
              <p className="text-sm text-gray-500 truncate max-w-xs sm:max-w-md md:max-w-lg">{todo.description}</p>
            )}
          </div>
        </div>
        <div className="flex items-center space-x-2 sm:justify-end">
          <span className="text-xs text-gray-500">
            {new Date(todo.updatedAt).toLocaleDateString()}
          </span>
          <button
            onClick={() => onDelete(todo.id)}
            className="text-red-600 hover:text-red-900 text-sm font-medium"
          >
            Delete
          </button>
        </div>
      </div>
    </li>
  );
};

export default TodoItem;