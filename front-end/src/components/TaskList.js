import Task from './Task';

export default function TaskList({ tasks, onUpdateTask, onDeleteTask, onToggleComplete }) {
  if (!tasks?.length) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">No tasks yet. Add one above!</p>
      </div>
    );
  }

  return (
    <div className="bg-white shadow overflow-hidden sm:rounded-md">
      <ul className="divide-y divide-gray-200">
        {tasks.map((task) => (
          <li key={task.id}>
            <Task
              task={task}
              onUpdate={onUpdateTask}
              onDelete={onDeleteTask}
              onToggleComplete={onToggleComplete}
            />
          </li>
        ))}
      </ul>
    </div>
  );
}
