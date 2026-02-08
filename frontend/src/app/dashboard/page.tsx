'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { apiClient } from '@/lib/api';
import { Button } from '@/components/ui/button';
import Input from '@/components/ui/Input';
import TaskCard from '@/components/TaskCard';
import StatsCard from '@/components/StatsCard';
import DashboardLayout from '@/components/DashboardLayout';
import ChatInterface from '@/components/chat/ChatInterface';

interface Task {
  id: string;
  title: string;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

export default function DashboardPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [newTask, setNewTask] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showChat, setShowChat] = useState(false);
  const router = useRouter();

  // Check if user is authenticated
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/signin');
    } else {
      fetchTasks();
    }
  }, []);

  const fetchTasks = async () => {
    try {
      const data: Task[] = await apiClient.get('/api/');
      setTasks(data);
    } catch (err: any) {
      setError(err.message || 'An error occurred while fetching tasks');
    } finally {
      setLoading(false);
    }
  };

  const handleAddTask = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!newTask.trim()) return;

    try {
      const newTaskData: Task = await apiClient.post('/api/', { title: newTask });
      setTasks([...tasks, newTaskData]);
      setNewTask('');
    } catch (err: any) {
      setError(err.message || 'An error occurred while adding the task');
    }
  };

  const handleToggleTask = async (taskId: string) => {
    try {
      const response: { success: boolean; completed: boolean } = await apiClient.patch(`/api/${taskId}/complete`);
      // Update the task in the local state
      setTasks(tasks.map(task =>
        task.id === taskId ? { ...task, completed: response.completed } : task
      ));
    } catch (err: any) {
      setError(err.message || 'An error occurred while updating the task');
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    try {
      await apiClient.delete(`/api/${taskId}`);
      setTasks(tasks.filter(task => task.id !== taskId));
    } catch (err: any) {
      setError(err.message || 'An error occurred while deleting the task');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    router.push('/signin');
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-lg">Loading tasks...</div>
      </div>
    );
  }

  // Calculate task statistics
  const totalTasks = tasks.length;
  const completedTasks = tasks.filter(task => task.completed).length;
  const pendingTasks = totalTasks - completedTasks;

  // Sidebar content
  const sidebarContent = (
    <>
      <a
        href="/dashboard"
        className="bg-blue-100 text-blue-700 group flex items-center px-2 py-2 text-sm font-medium rounded-md"
      >
        Dashboard
      </a>
      <button
        onClick={() => setShowChat(!showChat)}
        className={`${showChat ? 'bg-green-100 text-green-700' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'} group flex items-center px-2 py-2 text-sm font-medium rounded-md w-full text-left`}
      >
        Chat with AI
      </button>
      <a
        href="#"
        className="text-gray-600 hover:bg-gray-50 hover:text-gray-900 group flex items-center px-2 py-2 text-sm font-medium rounded-md"
      >
        Settings
      </a>
    </>
  );

  // Header content
  const headerContent = (
    <div className="border-b border-gray-200 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
        <div className="flex justify-between items-center py-4">
          <h1 className="text-2xl font-semibold text-gray-900">Dashboard</h1>
          <div className="flex space-x-2">
            <Button
              variant="outline"
              onClick={() => setShowChat(!showChat)}
              className="text-sm bg-blue-50 text-blue-600 hover:bg-blue-100 border-blue-300"
            >
              {showChat ? 'Hide Chat' : 'Show Chat'}
            </Button>
            <Button
              variant="outline"
              onClick={handleLogout}
              className="text-sm bg-red-50 text-red-600 hover:bg-red-100 border-red-300"
            >
              Logout
            </Button>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <DashboardLayout
      sidebarContent={sidebarContent}
      headerContent={headerContent}
    >
      {/* Stats Section - Responsive grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-6 sm:mb-8">
        <StatsCard
          title="Total Tasks"
          value={totalTasks}
          color="primary"
        />
        <StatsCard
          title="Completed"
          value={completedTasks}
          color="success"
        />
        <StatsCard
          title="Pending"
          value={pendingTasks}
          color="warning"
        />
      </div>

      {/* Add Task Section */}
      <div className="bg-white rounded-lg shadow p-4 sm:p-6 mb-6 sm:mb-8">
        <h2 className="text-lg font-medium text-gray-900 mb-3 sm:mb-4">Add New Task</h2>

        {error && (
          <div className="mb-4 rounded-md bg-red-50 p-4">
            <div className="text-sm text-red-700">{error}</div>
          </div>
        )}

        <form onSubmit={handleAddTask} className="flex flex-col sm:flex-row gap-2 sm:gap-3">
          <Input
            value={newTask}
            onChange={(e) => setNewTask(e.target.value)}
            placeholder="What needs to be done?"
            className="flex-grow"
          />
          <Button
            type="submit"
            variant="primary"
          >
            Add Task
          </Button>
        </form>
      </div>

      {/* Tasks List */}
      <div className={`bg-white rounded-lg shadow overflow-hidden ${showChat ? 'mb-80' : ''}`}>
        <div className="px-4 sm:px-6 py-3 sm:py-4 border-b border-gray-200">
          <h2 className="text-lg font-medium text-gray-900">My Tasks</h2>
        </div>

        <div className="divide-y divide-gray-200">
          {tasks.length === 0 ? (
            <div className="px-4 sm:px-6 py-12 text-center">
              <p className="text-gray-500">No tasks yet. Add a new task to get started!</p>
            </div>
          ) : (
            tasks.map((task) => (
              <TaskCard
                key={task.id}
                id={task.id}
                title={task.title}
                completed={task.completed}
                createdAt={task.created_at}
                onToggle={handleToggleTask}
                onDelete={handleDeleteTask}
              />
            ))
          )}
        </div>
      </div>

      {/* Embedded Chat Interface */}
      {showChat && (
        <div className="fixed bottom-4 right-4 w-full max-w-md h-[500px] z-50 bg-white rounded-lg shadow-xl border border-gray-200 overflow-hidden">
          <ChatInterface />
        </div>
      )}

      {/* Floating Action Button for Chat */}
      <button
        onClick={() => setShowChat(!showChat)}
        className="fixed bottom-6 right-6 bg-blue-600 text-white p-4 rounded-full shadow-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-300 z-50"
        aria-label={showChat ? "Close chat" : "Open chat"}
      >
        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={showChat ? "M6 18L18 6M6 6l12 12" : "M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"} />
        </svg>
      </button>
    </DashboardLayout>
  );
}