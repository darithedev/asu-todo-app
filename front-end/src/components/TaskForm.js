import { useState, useEffect } from 'react';
import { PRIORITY_LEVELS, PRIORITY_LABELS } from '../constants/taskPriorities';
import { labelService } from '../services/labels';
import { useAuth } from '../context/AuthContext';

// Helper function to determine if a color is light
function isLightColor(color) {
  if (!color) return false;
  const hex = color.replace('#', '');
  const r = parseInt(hex.substr(0, 2), 16);
  const g = parseInt(hex.substr(2, 2), 16);
  const b = parseInt(hex.substr(4, 2), 16);
  const brightness = ((r * 299) + (g * 587) + (b * 114)) / 1000;
  return brightness > 155;
}

export default function TaskForm({ task, onSubmit, onCancel }) {
  const { user } = useAuth();
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    priority: PRIORITY_LEVELS.MEDIUM,
    deadline: new Date().toISOString().split('T')[0], // This will be converted to full ISO string on submit
    label_ids: []
  });
  const [availableLabels, setAvailableLabels] = useState([]);
  const [isLoadingLabels, setIsLoadingLabels] = useState(true);
  const [labelError, setLabelError] = useState('');

  useEffect(() => {
    const loadLabels = async () => {
      if (!user?.id) return;
      try {
        setLabelError('');
        const labels = await labelService.getAllLabels();
        setAvailableLabels(labels);
      } catch (error) {
        console.error('Error loading labels:', error);
        setLabelError('Failed to load labels');
      } finally {
        setIsLoadingLabels(false);
      }
    };
    loadLabels();
  }, [user?.id]);

  useEffect(() => {
    if (task) {
      setFormData({
        title: task.title || '',
        description: task.description || '',
        priority: task.priority || PRIORITY_LEVELS.MEDIUM,
        deadline: task.deadline ? new Date(task.deadline).toISOString().split('T')[0] : new Date().toISOString().split('T')[0],
        label_ids: task.label_ids || []
      });
    }
  }, [task]);

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Convert the date string to ISO format for the backend
    const taskData = {
      ...formData,
      deadline: new Date(formData.deadline).toISOString(),
      label_ids: formData.label_ids
    };
    
    onSubmit(taskData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Labels selection (moved to top) */}
      <div className="bg-white border rounded-md p-3">
        <span className="text-sm font-medium text-gray-700">Labels</span>
        <div className="mt-2 space-y-2">
          {labelError && (
            <p className="text-sm text-red-600 mb-2">{labelError}</p>
          )}
          {isLoadingLabels ? (
            <div className="text-sm text-gray-500">Loading labels...</div>
          ) : availableLabels.length === 0 ? (
            <div className="text-sm text-gray-500">
              No labels available.{' '}
              <a href="/labels" className="text-primary-600 hover:text-primary-500">
                Create some labels
              </a>
            </div>
          ) : (
            <div className="flex flex-wrap gap-2">
              {availableLabels.map((label) => (
                <label
                  key={label.id}
                  className="inline-flex items-center"
                >
                  <input
                    type="checkbox"
                    className="form-checkbox h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                    checked={formData.label_ids.includes(label.id)}
                    onChange={(e) => {
                      const newLabelIds = e.target.checked
                        ? [...formData.label_ids, label.id]
                        : formData.label_ids.filter(id => id !== label.id);
                      setFormData({ ...formData, label_ids: newLabelIds });
                    }}
                  />
                  <span
                    className="ml-2 text-sm font-medium rounded-full px-2 py-0.5"
                    style={{
                      backgroundColor: label.color || '#3B82F6',
                      color: isLightColor(label.color) ? '#1F2937' : '#FFFFFF'
                    }}
                  >
                    {label.name}
                  </span>
                </label>
              ))}
            </div>
          )}
        </div>
      </div>
      <div>
        <label htmlFor="title" className="block text-sm font-medium text-gray-700">
          Title *
        </label>
        <input
          type="text"
          id="title"
          required
          className="input-field mt-1"
          value={formData.title}
          onChange={(e) => setFormData({ ...formData, title: e.target.value })}
        />
      </div>

      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700">
          Description
        </label>
        <textarea
          id="description"
          rows={3}
          className="input-field mt-1"
          value={formData.description}
          onChange={(e) => setFormData({ ...formData, description: e.target.value })}
        />
      </div>

      <div>
        <label htmlFor="priority" className="block text-sm font-medium text-gray-700">
          Priority *
        </label>
        <select
          id="priority"
          required
          className="input-field mt-1"
          value={formData.priority}
          onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
        >
          {Object.entries(PRIORITY_LEVELS).map(([key, value]) => (
            <option key={value} value={value}>
              {PRIORITY_LABELS[key]}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label htmlFor="deadline" className="block text-sm font-medium text-gray-700">
          Deadline *
        </label>
        <input
          type="date"
          id="deadline"
          required
          className="input-field mt-1"
          value={formData.deadline}
          onChange={(e) => setFormData({ ...formData, deadline: e.target.value })}
          min={new Date().toISOString().split('T')[0]}
        />
      </div>

      

      <div className="flex justify-end space-x-3">
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            className="btn-secondary"
          >
            Cancel
          </button>
        )}
        <button
          type="submit"
          className="btn-primary"
        >
          {task ? 'Update Task' : 'Create Task'}
        </button>
      </div>
    </form>
  );
}
