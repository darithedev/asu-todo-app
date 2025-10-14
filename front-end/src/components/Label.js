import { useState } from 'react';

export default function Label({ label, onUpdate, onDelete }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editedName, setEditedName] = useState(label.name);
  const [editedColor, setEditedColor] = useState(label.color || '#3B82F6'); // Default blue
  const [editedDescription, setEditedDescription] = useState(label.description || '');

  const handleSubmit = (e) => {
    e.preventDefault();

    // Validate color format
    const colorRegex = /^#[0-9A-Fa-f]{6}$/;
    if (!colorRegex.test(editedColor)) {
      alert('Please enter a valid hex color code (e.g., #FF5733)');
      return;
    }

    onUpdate(label.id, {
      name: editedName.trim(),
      color: editedColor,
      description: editedDescription.trim() || undefined
    });
    setIsEditing(false);
  };

  const labelStyle = {
    backgroundColor: label.color || '#3B82F6',
    color: isLightColor(label.color) ? '#1F2937' : '#FFFFFF'
  };

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

  if (isEditing) {
    return (
      <form onSubmit={handleSubmit} className="space-y-4 p-2">
        <div className="flex items-center space-x-2">
          <input
            type="text"
            value={editedName}
            onChange={(e) => setEditedName(e.target.value)}
            className="input-field py-1 px-2 text-sm flex-1"
            placeholder="Label name"
            maxLength={50}
            required
            autoFocus
          />
          <input
            type="color"
            value={editedColor}
            onChange={(e) => setEditedColor(e.target.value)}
            className="h-8 w-8 rounded cursor-pointer"
            title="Choose label color"
          />
        </div>
        <div>
          <textarea
            value={editedDescription}
            onChange={(e) => setEditedDescription(e.target.value)}
            className="input-field w-full py-1 px-2 text-sm"
            placeholder="Description (optional)"
            maxLength={200}
            rows={2}
          />
        </div>
        <div className="flex justify-end space-x-2">
          <button
            type="button"
            onClick={() => setIsEditing(false)}
            className="btn-secondary py-1 px-2 text-sm"
          >
            Cancel
          </button>
          <button
            type="submit"
            className="btn-primary py-1 px-2 text-sm"
          >
            Save
          </button>
        </div>
      </form>
    );
  }

  return (
    <div className="p-2 hover:bg-gray-50">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <span
            className="inline-flex items-center px-2.5 py-0.5 rounded-full text-sm font-medium"
            style={labelStyle}
          >
            {label.name}
          </span>
        </div>
        <div className="flex items-center space-x-2">
          <button
            onClick={() => setIsEditing(true)}
            className="text-gray-400 hover:text-gray-500"
            title="Edit label"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
              <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
            </svg>
          </button>
          <button
            onClick={() => onDelete(label.id)}
            className="text-red-400 hover:text-red-500"
            title="Delete label"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
          </button>
        </div>
      </div>
      {label.description && (
        <p className="mt-1 text-sm text-gray-500 pl-2">
          {label.description}
        </p>
      )}
    </div>
  );
}
