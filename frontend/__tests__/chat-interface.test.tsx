// Mock the jwt-decode module
jest.mock('jwt-decode', () => ({
  jwtDecode: jest.fn()
}));

import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { jwtDecode } from 'jwt-decode';
import ChatInterface from '../src/components/chat/ChatInterface';

// Mock localStorage
const mockLocalStorage = (() => {
  let store: { [key: string]: string } = {};
  return {
    getItem: (key: string) => store[key] || null,
    setItem: (key: string, value: string) => {
      store[key] = value.toString();
    },
    removeItem: (key: string) => {
      delete store[key];
    },
    clear: () => {
      store = {};
    }
  };
})();

Object.defineProperty(window, 'localStorage', {
  value: mockLocalStorage
});

describe('ChatInterface', () => {
  beforeEach(() => {
    (jwtDecode as jest.Mock).mockReturnValue({
      user_id: 'test-user-id',
      exp: Math.floor(Date.now() / 1000) + 60 * 60 // 1 hour from now
    });
    mockLocalStorage.setItem('token', 'test-token');
  });

  afterEach(() => {
    jest.clearAllMocks();
    mockLocalStorage.clear();
  });

  it('renders chat interface correctly', () => {
    render(<ChatInterface />);

    // Check if the main elements are present
    expect(screen.getByText('AI Assistant')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Type your message here...')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Send' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'New Conversation' })).toBeInTheDocument();
  });

  it('allows user to type and submit a message', async () => {
    render(<ChatInterface />);

    // Mock fetch
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: jest.fn().mockResolvedValue({
        conversation_id: 'test-conversation-id',
        response: 'Test response from AI'
      })
    }) as jest.Mock;

    const input = screen.getByPlaceholderText('Type your message here...');
    const sendButton = screen.getByRole('button', { name: 'Send' });

    // Type a message
    fireEvent.change(input, { target: { value: 'Hello, AI!' } });

    // Submit the message
    fireEvent.click(sendButton);

    // Wait for the message to be processed
    await waitFor(() => {
      expect(fetch).toHaveBeenCalled();
    });

    // Check if fetch was called with correct parameters
    expect(fetch).toHaveBeenCalledWith(
      'http://localhost:8000/api/test-user-id/chat',
      expect.objectContaining({
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer test-token'
        },
        body: JSON.stringify({
          message: 'Hello, AI!',
          conversation_id: undefined
        })
      })
    );
  });

  it('displays messages correctly', async () => {
    render(<ChatInterface />);

    // Mock fetch to return a response
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: jest.fn().mockResolvedValue({
        conversation_id: 'test-conversation-id',
        response: 'Test response from AI'
      })
    }) as jest.Mock;

    const input = screen.getByPlaceholderText('Type your message here...');
    const sendButton = screen.getByRole('button', { name: 'Send' });

    fireEvent.change(input, { target: { value: 'Test message' } });
    fireEvent.click(sendButton);

    // Wait for the messages to be displayed
    await waitFor(() => {
      expect(screen.getByText('Test message')).toBeInTheDocument();
    });

    await waitFor(() => {
      expect(screen.getByText('Test response from AI')).toBeInTheDocument();
    });
  });

  it('handles API errors gracefully', async () => {
    render(<ChatInterface />);

    // Mock fetch to simulate an error
    global.fetch = jest.fn().mockResolvedValue({
      ok: false,
      json: jest.fn().mockResolvedValue({
        detail: 'API Error occurred'
      })
    }) as jest.Mock;

    const input = screen.getByPlaceholderText('Type your message here...');
    const sendButton = screen.getByRole('button', { name: 'Send' });

    fireEvent.change(input, { target: { value: 'Test message' } });
    fireEvent.click(sendButton);

    // Wait for the error to be handled
    await waitFor(() => {
      expect(screen.getByText(/Error:/)).toBeInTheDocument();
    });
  });

  it('supports enter key submission', async () => {
    render(<ChatInterface />);

    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: jest.fn().mockResolvedValue({
        conversation_id: 'test-conversation-id',
        response: 'Test response'
      })
    }) as jest.Mock;

    const input = screen.getByPlaceholderText('Type your message here...');

    // Type message
    fireEvent.change(input, { target: { value: 'Test message' } });

    // Simulate pressing Enter
    fireEvent.keyDown(input, { key: 'Enter', shiftKey: false });

    // Wait for the fetch call
    await waitFor(() => {
      expect(fetch).toHaveBeenCalled();
    });
  });
});