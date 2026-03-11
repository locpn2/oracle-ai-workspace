import { useState } from 'react';
import { chatApi } from '../services/api';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  sql?: string;
  result?: unknown[];
}

export default function ChatPage() {
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [sessionId] = useState(() => `session_${Date.now()}`);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) return;

    const userMessage: Message = { role: 'user', content: question };
    setMessages((prev) => [...prev, userMessage]);
    setQuestion('');
    setError('');
    setLoading(true);

    try {
      const response = await chatApi.query({ question, sessionId });
      if (response.data?.success && response.data.data) {
        const data = response.data.data;
        const assistantMessage: Message = {
          role: 'assistant',
          content: data.message || 'Query executed successfully',
          sql: data.sql,
          result: data.result,
        };
        setMessages((prev) => [...prev, assistantMessage]);
      } else {
        setError(response.data?.message || 'Failed to process query');
      }
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-200px)]">
      <h1 className="text-2xl font-bold text-gray-800 mb-4">Chat AI - Text to SQL</h1>

      <div className="bg-white rounded-lg shadow flex-1 flex flex-col overflow-hidden">
        <div className="flex-1 overflow-auto p-4 space-y-4">
          {messages.length === 0 && (
            <div className="text-center text-gray-500 py-8">
              <p className="text-lg mb-2">💬 Ask questions about your database</p>
              <p className="text-sm">Example: "Show me all employees in the sales department"</p>
            </div>
          )}

          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[70%] rounded-lg p-4 ${
                  msg.role === 'user'
                    ? 'bg-indigo-600 text-white'
                    : 'bg-gray-100 text-gray-800'
                }`}
              >
                <p className="whitespace-pre-wrap">{msg.content}</p>
                {msg.sql && (
                  <div className="mt-3 p-3 bg-gray-800 rounded text-green-400 text-sm font-mono overflow-x-auto">
                    <pre>{msg.sql}</pre>
                  </div>
                )}
                {msg.result && Array.isArray(msg.result) && msg.result.length > 0 && (
                  <div className="mt-3 overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead>
                        <tr className="border-b border-gray-600">
                          {Object.keys(msg.result[0] as object).map((key) => (
                            <th key={key} className="px-2 py-1 text-left">
                              {key}
                            </th>
                          ))}
                        </tr>
                      </thead>
                      <tbody>
                        {msg.result.slice(0, 10).map((row, i) => (
                          <tr key={i} className="border-b border-gray-700">
                            {Object.values(row as object).map((val, j) => (
                              <td key={j} className="px-2 py-1">
                                {String(val)}
                              </td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                    {msg.result.length > 10 && (
                      <p className="text-xs text-gray-400 mt-2">
                        Showing 10 of {msg.result.length} rows
                      </p>
                    )}
                  </div>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex justify-start">
              <div className="bg-gray-100 rounded-lg p-4">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
              </div>
            </div>
          )}
        </div>

        {error && (
          <div className="mx-4 mb-2 p-3 bg-red-50 text-red-600 rounded-md text-sm">{error}</div>
        )}

        <form onSubmit={handleSubmit} className="border-t p-4">
          <div className="flex gap-2">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask a question about your data..."
              className="flex-1 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading || !question.trim()}
              className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Send
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
