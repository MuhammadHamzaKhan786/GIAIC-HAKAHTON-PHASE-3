'use client';

import { useState, useEffect } from 'react';
import { Search, Plus, Trash2, Calendar, Circle, CheckCircle, CircleDashed, Flag } from 'lucide-react';
import { apiClient } from '@/lib/api';

interface Todo {
  id: string;
  title: string;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

export default function PremiumDashboardPage() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [newTodo, setNewTodo] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    try {
      const data: Todo[] = await apiClient.get('/api/');
      setTodos(data);
    } catch (err: any) {
      setError(err.message || 'An error occurred while fetching tasks');
    } finally {
      setLoading(false);
    }
  };

  const totalTodos = todos.length;
  const completedTodos = todos.filter(todo => todo.completed).length;
  const pendingTodos = totalTodos - completedTodos;

  const addTodo = async () => {
    if (newTodo.trim() === '') return;

    try {
      const newTodoItem: Todo = await apiClient.post('/api/', { title: newTodo });
      setTodos([newTodoItem, ...todos]);
      setNewTodo('');
    } catch (err: any) {
      setError(err.message || 'An error occurred while adding the task');
    }
  };

  const toggleTodo = async (id: string) => {
    try {
      const response: { success: boolean; completed: boolean } = await apiClient.patch(`/api/${id}/complete`);
      if (response) {
        setTodos(todos.map(todo =>
          todo.id === id ? { ...todo, completed: response.completed } : todo
        ));
      }
    } catch (err: any) {
      setError(err.message || 'An error occurred while updating the task');
    }
  };

  const deleteTodo = async (id: string) => {
    try {
      await apiClient.delete(`/api/${id}`);
      setTodos(todos.filter(todo => todo.id !== id));
    } catch (err: any) {
      setError(err.message || 'An error occurred while deleting the task');
    }
  };

  const clearAllTodos = async () => {
    // We'll delete all todos one by one
    for (const todo of todos) {
      try {
        await apiClient.delete(`/api/${todo.id}`);
      } catch (err) {
        console.error('Error deleting todo:', err);
      }
    }
    setTodos([]);
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#F5FAFF] p-4 md:p-8 flex items-center justify-center">
        <div className="text-lg text-[#334155]">Loading tasks...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#F5FAFF] p-4 md:p-8">
      {/* Error Message Display */}
      {error && (
        <div className="mb-4 rounded-md bg-red-50 p-4 max-w-4xl mx-auto">
          <div className="text-sm text-red-700">{error}</div>
        </div>
      )}

      {/* Header Section - Top Center Title */}
      <div className="text-center mb-8">
        <h1 className="text-3xl md:text-4xl font-bold text-[#2563EB] uppercase tracking-wide">
          TRAKK 'EM ALL !!
        </h1>
      </div>

      <div className="max-w-4xl mx-auto">
        {/* Main Dashboard Card */}
        <div
          className="bg-white rounded-2xl shadow-lg p-6 border border-[#E6EFFA]"
          style={{ backgroundColor: '#FFFFFF', borderColor: '#E6EFFA' }}
        >
          {/* Header Inside Card */}
          <div className="flex justify-between items-center mb-8">
            <h2 className="text-2xl font-bold text-[#0F172A]">TODO-LIST</h2>
            <div className="w-10 h-10 rounded-full bg-[#E0ECFF] flex items-center justify-center">
              <span className="text-[#2563EB] font-semibold">U</span>
            </div>
          </div>

          {/* Stats/Badges Row */}
          <div className="flex gap-4 mb-8 flex-wrap">
            <div
              className="px-4 py-2 rounded-full text-sm font-medium flex items-center gap-2"
              style={{ backgroundColor: '#E0ECFF', color: '#2563EB' }}
            >
              <span>TOTAL</span>
              <span className="font-bold">{totalTodos}</span>
            </div>

            <div
              className="px-4 py-2 rounded-full text-sm font-medium flex items-center gap-2"
              style={{ backgroundColor: '#E0ECFF', color: '#16A34A' }}
            >
              <span>SUCCESS</span>
              <span className="font-bold">{completedTodos}</span>
            </div>

            <div
              className="px-4 py-2 rounded-full text-sm font-medium flex items-center gap-2"
              style={{ backgroundColor: '#E0ECFF', color: '#DC2626' }}
            >
              <span>PENDING</span>
              <span className="font-bold">{pendingTodos}</span>
            </div>
          </div>

          {/* Todo Input Section */}
          <div className="mb-8">
            <div className="flex items-center border-b border-[#E6EFFA] pb-2">
              <input
                type="text"
                value={newTodo}
                onChange={(e) => setNewTodo(e.target.value)}
                placeholder="Add a new task..."
                className="flex-grow bg-transparent outline-none text-[#334155] placeholder-[#94A3B8] text-base"
                onKeyDown={(e) => e.key === 'Enter' && addTodo()}
              />
              <button
                onClick={addTodo}
                className="text-[#2563EB] hover:text-[#1D4ED8] transition-colors"
              >
                <Plus className="w-5 h-5" />
              </button>
            </div>
          </div>

          {/* Todo List */}
          <div className="space-y-4 mb-8">
            {todos.length === 0 ? (
              <div className="text-center py-8 text-[#64748B]">
                <p>No tasks yet. Add a new task to get started!</p>
              </div>
            ) : (
              todos.map((todo) => (
                <div
                  key={todo.id}
                  className={`flex items-center justify-between p-4 rounded-lg transition-all duration-200 ${
                    todo.completed
                      ? 'opacity-60 bg-[#F8FAFC]'
                      : 'hover:bg-[#E0ECFF] bg-white'
                  }`}
                  style={{
                    borderColor: '#E6EFFA',
                    backgroundColor: todo.completed ? '#F8FAFC' : '#FFFFFF'
                  }}
                >
                  <div className="flex items-center gap-3 flex-grow">
                    <button
                      onClick={() => toggleTodo(todo.id)}
                      className="flex-shrink-0"
                    >
                      {todo.completed ? (
                        <CheckCircle className="w-5 h-5 text-[#16A34A]" />
                      ) : (
                        <CircleDashed className="w-5 h-5 text-[#64748B]" />
                      )}
                    </button>

                    <div className="flex items-center gap-2">
                      <span
                        className={`font-medium ${
                          todo.completed
                            ? 'line-through text-[#64748B]'
                            : 'text-[#334155]'
                        }`}
                      >
                        {todo.title}
                      </span>
                    </div>
                  </div>

                  <div className="flex items-center gap-4">
                    <div className="flex items-center gap-1 text-[#64748B] text-sm">
                      <Calendar className="w-4 h-4" />
                      <span>{formatDate(todo.created_at)}</span>
                    </div>

                    <button
                      onClick={() => deleteTodo(todo.id)}
                      className="text-[#DC2626] hover:text-[#B91C1C] transition-colors"
                    >
                      <Trash2 className="w-5 h-5" />
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>

          {/* Footer */}
          <div className="flex justify-end">
            <button
              onClick={clearAllTodos}
              className="px-4 py-2 text-sm font-medium text-[#DC2626] hover:text-[#B91C1C] transition-colors"
            >
              Clear All
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}