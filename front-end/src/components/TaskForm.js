import { useState, useEffect } from 'react';
import { PRIORITY_LEVELS, PRIORITY_LABELS } from '../constants/taskPriorities';

export default function TaskForm({ task, onSubmit, onCancel }) {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    priority: PRIORITY_LEVELS.MEDIUM,
    deadline: new Date().toISOString().split('T')[0], // This will be converted to full ISO string on submit
    label_ids: []
  });

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
      label_ids: [] // Add any label handling here if needed
    };
    
    onSubmit(taskData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
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
