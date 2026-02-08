export default function TypingIndicator() {
  return (
    <div className="flex justify-start animate-slideIn">
      <div className="bg-white text-gray-800 rounded-2xl px-4 py-3 rounded-bl-none max-w-[85%] border border-gray-200/50 shadow-md">
        <div className="flex items-center">
          <span className="mr-2 text-sm text-gray-500">AI Assistant is typing</span>
          <div className="flex space-x-1">
            <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
            <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
            <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
          </div>
        </div>
      </div>
    </div>
  );
}