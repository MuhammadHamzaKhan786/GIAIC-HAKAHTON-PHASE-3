import { ReactNode } from 'react';

interface MessageBubbleProps {
  role: 'user' | 'assistant';
  children: ReactNode;
}

export default function MessageBubble({ role, children }: MessageBubbleProps) {
  return (
    <div className={`flex ${role === 'user' ? 'justify-end' : 'justify-start'} animate-slideIn`}>
      <div
        className={`max-w-[85%] rounded-2xl px-4 py-3 shadow-sm transition-all duration-200 ${
          role === 'user'
            ? 'bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-br-none'
            : 'bg-white text-gray-800 border border-gray-200/50 rounded-bl-none shadow-md'
        }`}
      >
        <div className="whitespace-pre-wrap break-words">{children}</div>
        {role === 'assistant' && (
          <div className="flex items-center mt-1 pt-1 border-t border-gray-100/50">
            <div className="w-2 h-2 bg-green-400 rounded-full mr-1"></div>
            <span className="text-xs opacity-70">AI Assistant</span>
          </div>
        )}
      </div>
    </div>
  );
}