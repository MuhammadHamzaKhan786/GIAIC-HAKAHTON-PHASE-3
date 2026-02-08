import React from 'react';
import { Card, CardContent } from '@/components/ui/Card';

interface TaskCardProps {
  id: string;
  title: string;
  completed: boolean;
  createdAt: string;
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
}

const TaskCard: React.FC<TaskCardProps> = ({
  id,
  title,
  completed,
  createdAt,
  onToggle,
  onDelete
}) => {
  return (
    <Card className={`transition-all duration-200 ${completed ? 'bg-green-50 border-green-200' : 'bg-white'}`}>
      <CardContent className="p-4">
        <div className="flex items-start space-x-3">
          <input
            type="checkbox"
            checked={completed}
            onChange={() => onToggle(id)}
            className="mt-1 h-5 w-5 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
          />
          <div className="flex-1 min-w-0">
            <p className={`text-sm font-medium ${completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
              {title}
            </p>
            <p className="text-xs text-gray-500 mt-1">
              Created: {new Date(createdAt).toLocaleDateString()}
            </p>
          </div>
          <button
            onClick={() => onDelete(id)}
            className="ml-2 inline-flex items-center text-red-600 hover:text-red-900 text-sm font-medium"
          >
            Delete
          </button>
        </div>
      </CardContent>
    </Card>
  );
};

export default TaskCard;