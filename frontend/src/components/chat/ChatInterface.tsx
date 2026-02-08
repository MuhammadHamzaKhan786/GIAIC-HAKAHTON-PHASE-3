'use client';

import { useState, useRef, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';
import MessageBubble from './MessageBubble';
import TypingIndicator from './TypingIndicator';
import NewConversationBtn from './NewConversationBtn';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface ChatProps {}

export default function ChatInterface({}: ChatProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Get user ID from token
  const getUserIdFromToken = (): string => {
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('No authentication token found');
    }

    try {
      const decoded: any = jwtDecode(token);
      // Try multiple possible fields for user ID in the token
      return decoded.user_id || decoded.userId || decoded.sub || decoded.id;
    } catch (error) {
      console.error('Error decoding token:', error);
      throw new Error('Invalid token');
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    try {
      const userId = getUserIdFromToken();

      // Add user message to UI immediately
      const userMessage: Message = {
        id: Date.now().toString(),
        role: 'user',
        content: inputValue,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, userMessage]);
      setInputValue('');
      setIsLoading(true);

      // Log the API call for debugging
      console.log('Making API call to:', `${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'}/api/${userId}/chat`);
      console.log('Headers:', {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token') ? '***TOKEN_PRESENT***' : 'NO_TOKEN'}`
      });
      console.log('Payload:', {
        message: inputValue,
        conversation_id: conversationId || undefined
      });

      // Call the backend API
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'}/api/${userId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token') || ''}`
        },
        body: JSON.stringify({
          message: inputValue,
          conversation_id: conversationId || undefined
        })
      });

      console.log('Response status:', response.status);

      if (!response.ok) {
        const errorText = await response.text(); // Get raw text first
        console.error('Raw error response:', errorText);

        try {
          // Try to parse as JSON if possible
          const errorData = JSON.parse(errorText);
          throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        } catch (parseError) {
          // If not JSON, throw with raw text
          throw new Error(`HTTP error! status: ${response.status}, details: ${errorText}`);
        }
      }

      const data = await response.json();
      console.log('Response data:', data);

      // Add assistant message to UI
      const assistantMessage: Message = {
        id: Date.now().toString(),
        role: 'assistant',
        content: data.response,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);
      setConversationId(data.conversation_id);
    } catch (error: any) {
      console.error('Full error details:', error);
      console.error('Error message:', error.message);
      console.error('Error stack:', error.stack);

      // Add error message to UI
      const errorMessage: Message = {
        id: Date.now().toString(),
        role: 'assistant',
        content: `Error: ${error.message || 'An error occurred while sending your message'}`,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e as any);
    }
  };

  const startNewConversation = () => {
    setMessages([]);
    setConversationId(null);
  };

  return (
    <div className="flex flex-col h-full max-w-4xl mx-auto w-full bg-gradient-to-br from-indigo-50 to-blue-50 rounded-xl shadow-xl border border-gray-200 overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white p-5 flex justify-between items-center shadow-md">
        <div className="flex items-center space-x-3">
          <div className="relative">
            <div className="w-10 h-10 rounded-full bg-blue-400 flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
            </div>
            <div className="absolute bottom-0 right-0 w-3 h-3 bg-green-400 rounded-full border-2 border-white animate-pulse"></div>
          </div>
          <div>
            <h1 className="text-lg font-semibold">AI Task Assistant</h1>
            <p className="text-blue-200 text-xs">Online • Ready to help</p>
          </div>
        </div>
        <NewConversationBtn onClick={startNewConversation} />
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gradient-to-b from-transparent to-indigo-50/50">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center p-8">
            <div className="mb-6 transform hover:scale-105 transition-transform duration-300">
              <div className="w-24 h-24 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-full flex items-center justify-center mx-auto shadow-lg animate-bounce">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                </svg>
              </div>
            </div>
            <h3 className="text-xl font-semibold text-gray-800 mb-2">Welcome to AI Assistant</h3>
            <p className="text-gray-600 max-w-md">
              I can help you manage your tasks, answer questions, and boost your productivity.
              Start by asking me to create a task or asking any question!
            </p>
            <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-3 w-full max-w-md">
              <div className="bg-white/70 backdrop-blur-sm rounded-lg p-3 border border-gray-200/50 shadow-sm hover:shadow-md transition-shadow duration-200 cursor-pointer">
                <p className="text-sm text-gray-700">"Add a task to buy groceries"</p>
              </div>
              <div className="bg-white/70 backdrop-blur-sm rounded-lg p-3 border border-gray-200/50 shadow-sm hover:shadow-md transition-shadow duration-200 cursor-pointer">
                <p className="text-sm text-gray-700">"Show me my pending tasks"</p>
              </div>
              <div className="bg-white/70 backdrop-blur-sm rounded-lg p-3 border border-gray-200/50 shadow-sm hover:shadow-md transition-shadow duration-200 cursor-pointer">
                <p className="text-sm text-gray-700">"What's my schedule today?"</p>
              </div>
              <div className="bg-white/70 backdrop-blur-sm rounded-lg p-3 border border-gray-200/50 shadow-sm hover:shadow-md transition-shadow duration-200 cursor-pointer">
                <p className="text-sm text-gray-700">"Help me prioritize tasks"</p>
              </div>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            {messages.map((message, index) => (
              <div
                key={message.id}
                className={`transform transition-all duration-300 ease-out opacity-0 translate-y-4 animate-fadeIn`}
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <MessageBubble role={message.role}>
                  {message.content}
                </MessageBubble>
              </div>
            ))}
            {isLoading && (
              <div className="transform transition-all duration-300 ease-out opacity-0 translate-y-4 animate-fadeIn">
                <TypingIndicator />
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="border-t border-gray-200/50 bg-white/80 backdrop-blur-sm p-4">
        <form onSubmit={handleSubmit} className="flex gap-2">
          <div className="relative flex-1">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Message AI Assistant..."
              className="w-full border border-gray-300/50 rounded-xl py-3 px-4 pr-12 resize-none h-14 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500/50 transition-all duration-200 shadow-sm bg-white/80 backdrop-blur-sm"
              disabled={isLoading}
            />
            <div className="absolute right-3 bottom-3 text-xs text-gray-400">
              {inputValue.length}/500
            </div>
          </div>
          <button
            type="submit"
            disabled={!inputValue.trim() || isLoading}
            className={`self-end h-14 w-14 rounded-xl flex items-center justify-center transition-all duration-200 ${
              inputValue.trim() && !isLoading
                ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white hover:from-blue-700 hover:to-indigo-700 shadow-lg hover:shadow-xl transform hover:scale-105'
                : 'bg-gray-200 text-gray-400 cursor-not-allowed'
            }`}
          >
            {isLoading ? (
              <svg className="animate-spin h-5 w-5 text-current" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            ) : (
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            )}
          </button>
        </form>
        <p className="text-xs text-gray-500 mt-2 text-center">
          AI Assistant can help you manage tasks • Press Enter to send
        </p>
      </div>

      <style jsx global>{`
        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(4px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        @keyframes slideIn {
          from {
            opacity: 0;
            transform: translateY(10px) scale(0.95);
          }
          to {
            opacity: 1;
            transform: translateY(0) scale(1);
          }
        }
        .animate-fadeIn {
          animation: fadeIn 0.3s ease-out forwards;
        }
        .animate-slideIn {
          animation: slideIn 0.3s ease-out forwards;
        }
      `}</style>
    </div>
  );
}