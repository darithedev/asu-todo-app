import { useState } from 'react';
import Label from './Label';

export default function LabelList({ labels, onCreateLabel, onUpdateLabel, onDeleteLabel }) {
  const [newLabelName, setNewLabelName] = useState('');
  const [newLabelColor, setNewLabelColor] = useState('#3B82F6'); // Default blue
  const [newLabelDescription, setNewLabelDescription] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!newLabelName.trim()) return;

    // Validate color format
    const colorRegex = /^#[0-9A-Fa-f]{6}$/;
    if (!colorRegex.test(newLabelColor)) {
      alert('Please enter a valid hex color code (e.g., #FF5733)');
      return;
    }

    const success = await onCreateLabel({
      name: newLabelName.trim(),
      color: newLabelColor,
      description: newLabelDescription.trim() || undefined
    });

    if (success) {
      setNewLabelName('');
      setNewLabelColor('#3B82F6');
      setNewLabelDescription('');
    }
  };

  return (
    <div className="space-y-4">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="flex items-center space-x-2">
          <input
            type="text"
            value={newLabelName}
            onChange={(e) => setNewLabelName(e.target.value)}
            placeholder="Label name (required)"
            maxLength={50}
            className="input-field flex-1"
            required
          />
          <input
            type="color"
            value={newLabelColor}
            onChange={(e) => setNewLabelColor(e.target.value)}
            className="h-10 w-10 rounded cursor-pointer"
            title="Choose label color"
          />
        </div>
        <div>
          <textarea
            value={newLabelDescription}
            onChange={(e) => setNewLabelDescription(e.target.value)}
            placeholder="Description (optional)"
            maxLength={200}
            rows={2}
            className="input-field w-full"
          />
        </div>
        <div className="flex justify-end">
          <button
            type="submit"
            disabled={!newLabelName.trim()}
            className="btn-primary"
          >
            Add Label
          </button>
        </div>
      </form>

      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        {labels.length === 0 ? (
          <div className="text-center py-4 text-gray-500">
            No labels yet. Create one above!
          </div>
        ) : (
          <ul className="divide-y divide-gray-200">
            {labels.map((label) => (
              <li key={label.id}>
                <Label
                  label={label}
                  onUpdate={onUpdateLabel}
                  onDelete={onDeleteLabel}
                />
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
