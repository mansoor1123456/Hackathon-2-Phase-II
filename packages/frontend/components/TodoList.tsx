'use client';

import React, { useState, useEffect } from 'react';
import { Todo, TodoUpdate } from '../../shared/types/todo';
import TodoItem from './TodoItem';

interface TodoListProps {
  onTodoUpdate?: (todo: Todo) => void;
  onTodoDelete?: (todoId: string) => void;
}

const TodoList: React.FC<TodoListProps> = ({ onTodoUpdate, onTodoDelete }) => {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<'all' | 'completed' | 'incomplete'>('all');
  const [limit, setLimit] = useState(20);
  const [offset, setOffset] = useState(0);

  useEffect(() => {
    loadTodos();
  }, [filter, limit, offset]);

  const loadTodos = async () => {
    try {
      setLoading(true);
      setError(null);

      // 🔹 Get token from cookie
      const token = document.cookie
        .split('; ')
        .find(row => row.startsWith('todo_app_token='))
        ?.split('=')[1];

      if (!token) throw new Error('Unauthorized: No token found');

      // 🔹 Fetch todos with Authorization header
      const res = await fetch(
        `http://127.0.0.1:8000/todos/?limit=${limit}&offset=${offset}&filter=${filter}`,
        {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`, // Token sent here
          },
        }
      );

      if (!res.ok) {
        throw new Error(`API request failed: ${res.status}`);
      }

      const data = await res.json();
      setTodos(data.todos || []);
    } catch (err: any) {
      setError(err.message || 'Failed to load todos');
    } finally {
      setLoading(false);
    }
  };

  const handleToggleComplete = async (todo: Todo) => {
    try {
      const token = document.cookie
        .split('; ')
        .find(row => row.startsWith('todo_app_token='))
        ?.split('=')[1];

      if (!token) throw new Error('Unauthorized: No token found');

      const updatedData: TodoUpdate = { completed: !todo.completed };

      const res = await fetch(`http://127.0.0.1:8000/todos/${todo.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(updatedData),
      });

      if (!res.ok) throw new Error('Failed to update todo');

      const updatedTodo = await res.json();
      setTodos(todos.map(t => (t.id === todo.id ? updatedTodo : t)));

      if (onTodoUpdate) onTodoUpdate(updatedTodo);
    } catch (err: any) {
      setError(err.message || 'Failed to update todo');
    }
  };

  const handleDelete = async (todoId: string) => {
    try {
      const token = document.cookie
        .split('; ')
        .find(row => row.startsWith('todo_app_token='))
        ?.split('=')[1];

      if (!token) throw new Error('Unauthorized: No token found');

      const res = await fetch(`http://127.0.0.1:8000/todos/${todoId}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
      });

      if (!res.ok) throw new Error('Failed to delete todo');

      setTodos(todos.filter(todo => todo.id !== todoId));

      if (onTodoDelete) onTodoDelete(todoId);
    } catch (err: any) {
      setError(err.message || 'Failed to delete todo');
    }
  };

  if (loading) {
    return <div className="text-center py-4">Loading todos...</div>;
  }

  if (error) {
    return <div className="text-center py-4 text-red-500">Error: {error}</div>;
  }

  return (
    <div className="bg-white shadow overflow-hidden sm:rounded-md">
      <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
        <h3 className="text-lg leading-6 font-medium text-gray-900">Your Todos</h3>
        <p className="mt-1 max-w-2xl text-sm text-gray-500">
          Manage your tasks and stay organized
        </p>
      </div>

      <div className="flex flex-col sm:flex-row items-center justify-between px-4 py-3 bg-gray-50 sm:px-6">
        <div className="flex space-x-2 mb-2 sm:mb-0">
          <button
            onClick={() => setFilter('all')}
            className={`px-3 py-1 text-sm rounded-md ${
              filter === 'all' ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            All
          </button>
          <button
            onClick={() => setFilter('completed')}
            className={`px-3 py-1 text-sm rounded-md ${
              filter === 'completed' ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            Completed
          </button>
          <button
            onClick={() => setFilter('incomplete')}
            className={`px-3 py-1 text-sm rounded-md ${
              filter === 'incomplete' ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            Incomplete
          </button>
        </div>
      </div>

      <ul className="divide-y divide-gray-200">
        {todos.length === 0 ? (
          <li className="px-4 py-4 sm:px-6">
            <p className="text-center text-gray-500">No todos found. Add one to get started!</p>
          </li>
        ) : (
          todos.map((todo) => (
            <TodoItem
              key={todo.id}
              todo={todo}
              onToggleComplete={handleToggleComplete}
              onDelete={handleDelete}
            />
          ))
        )}
      </ul>
    </div>
  );
};

export default TodoList;
