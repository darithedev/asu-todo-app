import { useState, useEffect } from 'react';
import Head from 'next/head';
import { useRouter } from 'next/router';
import { useAuth } from '../context/AuthContext';
import { labelService } from '../services/labels';
import { taskService } from '../services/tasks';
import TaskList from '../components/TaskList';
import TaskForm from '../components/TaskForm';

export default function Tasks() {
  const { user, isAuthenticated } = useAuth();
  const router = useRouter();
  const [tasks, setTasks] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  // Label filtering state
  const [labels, setLabels] = useState([]);
  const [isLoadingLabels, setIsLoadingLabels] = useState(true);
  const [selectedLabelIds, setSelectedLabelIds] = useState([]);
  // Quick filters state
  const [filterUrgent, setFilterUrgent] = useState(false);
  const [filterDueToday, setFilterDueToday] = useState(false);
  const [filterDueTomorrow, setFilterDueTomorrow] = useState(false);

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!isAuthenticated) {
      router.replace('/login');
    }
  }, [isAuthenticated, router]);

  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    if (!user?.id) {
      console.log('No user ID available:', user);
      return;
    }
    
    try {
      console.log('Loading tasks for user:', user.id);
      const data = await taskService.getAllTasks(user.id);
      console.log('Loaded tasks:', data);
      setTasks(data);
    } catch (err) {
      setError('Failed to load tasks');
      console.error('Error loading tasks:', err);
    } finally {
      setIsLoading(false);
    }
  };

  // Load available labels for filtering
  useEffect(() => {
    const loadLabels = async () => {
      if (!isAuthenticated) return;
      try {
        setIsLoadingLabels(true);
        const data = await labelService.getAllLabels();
        setLabels(data);
      } catch (e) {
        console.error('Failed to load labels', e);
      } finally {
        setIsLoadingLabels(false);
      }
    };
    loadLabels();
  }, [isAuthenticated]);

  // Reload tasks when user changes
  useEffect(() => {
    if (user?.id) {
      loadTasks();
    } else {
      console.log('Waiting for user data...');
    }
  }, [user?.id]);

  const handleCreateTask = async (taskData) => {
    try {
      const newTask = await taskService.createTask(taskData);
      setTasks([...tasks, newTask]);
    } catch (err) {
      setError('Failed to create task');
      console.error('Error creating task:', err);
    }
  };

  const handleUpdateTask = async (taskId, updates) => {
    try {
      const updatedTask = await taskService.updateTask(taskId, updates);
      setTasks(tasks.map(task => task.id === taskId ? updatedTask : task));
    } catch (err) {
      setError('Failed to update task');
      console.error('Error updating task:', err);
    }
  };

  const handleDeleteTask = async (taskId) => {
    try {
      await taskService.deleteTask(taskId);
      setTasks(tasks.filter(task => task.id !== taskId));
    } catch (err) {
      setError(err.message || 'Failed to delete task');
      console.error('Error deleting task:', err);
      // Refresh task list if we get a 403 error (task might belong to another user)
      if (err.response?.status === 403) {
        loadTasks();
      }
    }
  };

  const handleToggleComplete = async (taskId) => {
    try {
      const updatedTask = await taskService.toggleTaskComplete(taskId);
      setTasks(tasks.map(task => task.id === taskId ? updatedTask : task));
    } catch (err) {
      setError('Failed to update task');
      console.error('Error updating task:', err);
    }
  };

  // Derived: tasks to display after filtering by labels
  const displayedTasks = tasks.filter(t => {
    // Label filter
    if (selectedLabelIds.length > 0) {
      const taskLabelIds = t.label_ids || [];
      if (!selectedLabelIds.every(id => taskLabelIds.includes(id))) return false;
    }
    // Quick filters
    if (filterUrgent && t.priority !== 'High') return false;
    if (filterDueToday || filterDueTomorrow) {
      try {
        const today = new Date(); today.setHours(0,0,0,0);
        const deadline = new Date(t.deadline);
        const dl = new Date(deadline.getFullYear(), deadline.getMonth(), deadline.getDate());
        const diffDays = Math.round((dl - today) / (1000*60*60*24));
        if (filterDueToday && diffDays !== 0) return false;
        if (filterDueTomorrow && diffDays !== 1) return false;
      } catch {
        return false;
      }
    }
    return true;
  });

  return (
    <>
      <Head>
        <title>My Tasks - ASU Todo App</title>
        <meta name="description" content="Manage your tasks" />
      </Head>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="md:flex md:items-center md:justify-between">
          <div className="flex-1 min-w-0">
            <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
              My Tasks
            </h2>
          </div>
        </div>

        {/* Add new task form */}
        <div className="mt-8 mb-6">
          <TaskForm onSubmit={handleCreateTask} />
        </div>

        {/* Filters */}
        <div className="mb-6">
          <div className="bg-white border rounded-md p-4">
            <div className="flex items-start justify-between gap-3">
              <h3 className="text-sm font-semibold text-gray-900">Filters</h3>
              {(filterUrgent || filterDueToday || filterDueTomorrow || selectedLabelIds.length>0) && (
                <button
                  type="button"
                  className="px-2 py-1 rounded-md bg-gray-100 text-gray-700 hover:bg-gray-200 text-xs"
                  onClick={() => { setFilterUrgent(false); setFilterDueToday(false); setFilterDueTomorrow(false); setSelectedLabelIds([]); }}
                  aria-label="Clear all filters"
                >
                  Clear all
                </button>
              )}
            </div>
            {/* Quick filters */}
            <div className="mt-3 flex flex-wrap gap-3 text-xs">
              <button
                type="button"
                className={`px-2 py-1 rounded-md ${filterUrgent ? 'bg-red-600 text-white' : 'bg-red-100 text-red-700 hover:bg-red-200'}`}
                onClick={() => setFilterUrgent(v => !v)}
              >
                URGENT (High)
              </button>
              <button
                type="button"
                className={`px-2 py-1 rounded-md ${filterDueToday ? 'bg-yellow-600 text-white' : 'bg-yellow-100 text-yellow-800 hover:bg-yellow-200'}`}
                onClick={() => setFilterDueToday(v => !v)}
              >
                DUE TODAY
              </button>
              <button
                type="button"
                className={`px-2 py-1 rounded-md ${filterDueTomorrow ? 'bg-blue-600 text-white' : 'bg-blue-100 text-blue-700 hover:bg-blue-200'}`}
                onClick={() => setFilterDueTomorrow(v => !v)}
              >
                DUE TOMORROW
              </button>
            </div>

            {/* Label filters */}
            <h4 className="mt-4 text-xs font-medium text-gray-700">Labels</h4>
            {isLoadingLabels ? (
              <p className="text-sm text-gray-500">Loading labels...</p>
            ) : labels.length === 0 ? (
              <p className="text-sm text-gray-500">No labels available.</p>
            ) : (
              <div className="flex flex-wrap gap-3">
                {labels.map(label => (
                  <label key={label.id} className="inline-flex items-center">
                    <input
                      type="checkbox"
                      className="form-checkbox h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                      checked={selectedLabelIds.includes(label.id)}
                      onChange={(e) => {
                        setSelectedLabelIds(prev => (
                          e.target.checked
                            ? [...prev, label.id]
                            : prev.filter(id => id !== label.id)
                        ));
                      }}
                    />
                    <span
                      className="ml-2 text-sm font-medium rounded-full px-2 py-0.5"
                      style={{ backgroundColor: label.color || '#3B82F6', color: '#fff' }}
                    >
                      {label.name}
                    </span>
                  </label>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Error message */}
        {error && (
          <div className="rounded-md bg-red-50 p-4 mb-4">
            <div className="flex">
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">{error}</h3>
              </div>
            </div>
          </div>
        )}

        {/* Tasks list */}
        {isLoading ? (
          <div className="text-center py-8">
            <div className="inline-flex items-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-primary-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Loading tasks...
            </div>
          </div>
        ) : (
          <TaskList
            tasks={displayedTasks}
            onUpdateTask={handleUpdateTask}
            onDeleteTask={handleDeleteTask}
            onToggleComplete={handleToggleComplete}
          />
        )}
      </div>
    </>
  );
}
