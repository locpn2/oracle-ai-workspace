import { useState, useEffect } from 'react';
import { vectorApi, schemaApi } from '../services/api';
import type { SearchResult, TableDTO } from '../types';

export default function VectorSearchPage() {
  const [query, setQuery] = useState('');
  const [tableName, setTableName] = useState('');
  const [limit, setLimit] = useState(10);
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [embedLoading, setEmbedLoading] = useState(false);
  const [embedMessage, setEmbedMessage] = useState('');
  const [tables, setTables] = useState<TableDTO[]>([]);

  useEffect(() => {
    loadTables();
  }, []);

  const loadTables = async () => {
    try {
      const response = await schemaApi.getTables();
      if (response.data?.success && response.data.data) {
        setTables(response.data.data);
      }
    } catch (err) {
      console.error('Failed to load tables');
    }
  };

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError('');
    setResults([]);

    try {
      const response = await vectorApi.search({ query, tableName: tableName || undefined, limit });
      if (response.data?.success && response.data.data) {
        setResults(response.data.data);
      } else {
        setError(response.data?.message || 'Search failed');
      }
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleEmbed = async (table: string) => {
    setEmbedLoading(true);
    setEmbedMessage('');

    try {
      const response = await vectorApi.embedTable({ tableName: table });
      if (response.data?.success) {
        setEmbedMessage(`Embedding job started for ${table}. Job ID: ${response.data.data?.jobId}`);
      } else {
        setEmbedMessage(response.data?.message || 'Failed to start embedding');
      }
    } catch (err: unknown) {
      setEmbedMessage(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setEmbedLoading(false);
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Vector Search</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow p-6 mb-6">
            <h2 className="text-lg font-semibold mb-4">Semantic Search</h2>
            
            {error && (
              <div className="mb-4 p-3 bg-red-50 text-red-600 rounded-md text-sm">{error}</div>
            )}

            <form onSubmit={handleSearch}>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">Search Query</label>
                <input
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Enter your search query..."
                  className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-4 mb-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Table (optional)</label>
                  <select
                    value={tableName}
                    onChange={(e) => setTableName(e.target.value)}
                    className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500"
                  >
                    <option value="">All tables</option>
                    {tables.map((t) => (
                      <option key={t.name} value={t.name}>{t.name}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Limit</label>
                  <input
                    type="number"
                    value={limit}
                    onChange={(e) => setLimit(parseInt(e.target.value) || 10)}
                    min={1}
                    max={100}
                    className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500"
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={loading || !query.trim()}
                className="w-full py-2 px-4 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50"
              >
                {loading ? 'Searching...' : 'Search'}
              </button>
            </form>
          </div>

          {results.length > 0 && (
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold mb-4">Results ({results.length})</h2>
              <div className="space-y-4">
                {results.map((result, idx) => (
                  <div key={idx} className="border rounded-lg p-4 hover:bg-gray-50">
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <span className="font-medium text-indigo-600">{result.tableName}</span>
                        <span className="text-gray-400 mx-2">.</span>
                        <span className="text-gray-600">{result.columnName}</span>
                      </div>
                      <span className="text-sm text-gray-400">Score: {result.score.toFixed(4)}</span>
                    </div>
                    <pre className="bg-gray-50 p-3 rounded text-sm overflow-x-auto">
                      {JSON.stringify(result.rowData, null, 2)}
                    </pre>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        <div>
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold mb-4">Embed Tables</h2>
            <p className="text-sm text-gray-500 mb-4">
              Embed table data into vector database for semantic search.
            </p>
            
            {embedMessage && (
              <div className={`mb-4 p-3 rounded-md text-sm ${
                embedMessage.includes('Failed') || embedMessage.includes('Error')
                  ? 'bg-red-50 text-red-600'
                  : 'bg-green-50 text-green-600'
              }`}>
                {embedMessage}
              </div>
            )}

            <div className="space-y-2">
              {tables.map((table) => (
                <div key={table.name} className="flex items-center justify-between p-3 bg-gray-50 rounded">
                  <span className="text-sm font-medium">{table.name}</span>
                  <button
                    onClick={() => handleEmbed(table.name)}
                    disabled={embedLoading}
                    className="px-3 py-1 text-sm bg-indigo-100 text-indigo-700 rounded hover:bg-indigo-200 disabled:opacity-50"
                  >
                    Embed
                  </button>
                </div>
              ))}
              {tables.length === 0 && (
                <p className="text-sm text-gray-500">No tables available</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
