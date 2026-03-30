import { useState } from 'react'
import { useMutation, useQuery } from '@tanstack/react-query'
import { Send, Copy, Check, Loader2, Play, History, X, Plus } from 'lucide-react'
import { queryService } from '@/services/queryService'
import type { QueryResponse, ExecuteResponse } from '@/types/query'

interface SqlTab {
  id: string
  name: string
  query: string
  sqlResult: QueryResponse | null
  executeResult: ExecuteResponse | null
}

export function QueryPage() {
  const [query, setQuery] = useState('')
  const [tabs, setTabs] = useState<SqlTab[]>([
    { id: 'tab-1', name: 'Query 1', query: '', sqlResult: null, executeResult: null }
  ])
  const [activeTabId, setActiveTabId] = useState('tab-1')
  const [copied, setCopied] = useState(false)
  const [showHistory, setShowHistory] = useState(false)

  const activeTab = tabs.find(t => t.id === activeTabId) || tabs[0]

  const textToSqlMutation = useMutation({
    mutationFn: (naturalLanguage: string) =>
      queryService.textToSQL({ natural_language: naturalLanguage }),
    onSuccess: (data) => {
      setTabs(prev => prev.map(tab => 
        tab.id === activeTabId 
          ? { ...tab, sqlResult: data, executeResult: null }
          : tab
      ))
    },
  })

  const executeMutation = useMutation({
    mutationFn: (sql: string) =>
      queryService.execute({ sql, page: 1, pageSize: 100 }),
    onSuccess: (data) => {
      setTabs(prev => prev.map(tab => 
        tab.id === activeTabId 
          ? { ...tab, executeResult: data }
          : tab
      ))
    },
  })

  const historyQuery = useQuery({
    queryKey: ['queryHistory'],
    queryFn: () => queryService.getHistory(20),
    enabled: showHistory,
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (query.trim()) {
      textToSqlMutation.mutate(query)
    }
  }

  const handleCopy = () => {
    if (activeTab?.sqlResult?.sql) {
      navigator.clipboard.writeText(activeTab.sqlResult.sql)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  const handleExecute = () => {
    if (activeTab?.sqlResult?.sql && !activeTab.sqlResult.error) {
      executeMutation.mutate(activeTab.sqlResult.sql)
    }
  }

  const addNewTab = () => {
    const newId = `tab-${Date.now()}`
    const newTabNumber = tabs.length + 1
    setTabs(prev => [...prev, {
      id: newId,
      name: `Query ${newTabNumber}`,
      query: '',
      sqlResult: null,
      executeResult: null
    }])
    setActiveTabId(newId)
    setQuery('')
  }

  const closeTab = (tabId: string) => {
    if (tabs.length === 1) return
    const tabIndex = tabs.findIndex(t => t.id === tabId)
    const newTabs = tabs.filter(t => t.id !== tabId)
    setTabs(newTabs)
    if (activeTabId === tabId) {
      const newActiveIndex = Math.min(tabIndex, newTabs.length - 1)
      setActiveTabId(newTabs[newActiveIndex].id)
    }
  }

  const sqlResult = activeTab?.sqlResult
  const executeResult = activeTab?.executeResult

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Query Input */}
      <div className="space-y-4">
        <div className="bg-white rounded-xl border border-gray-200 p-4">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Natural Language Query</h2>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setShowHistory(!showHistory)}
                className="p-2 text-gray-500 hover:bg-gray-100 rounded-lg"
                title="History"
              >
                <History className="w-5 h-5" />
              </button>
            </div>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <textarea
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask a question about your data... e.g., 'Show me total sales by region for Q4'"
              className="w-full h-32 p-3 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            />
            <button
              type="submit"
              disabled={textToSqlMutation.isPending || !query.trim()}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition disabled:opacity-50"
            >
              {textToSqlMutation.isPending ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <Send className="w-5 h-5" />
              )}
              Generate SQL
            </button>
          </form>
        </div>

        {/* SQL Tabs */}
        <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
          <div className="flex items-center border-b border-gray-200 bg-gray-50 overflow-x-auto">
            {tabs.map((tab) => (
              <div
                key={tab.id}
                className={`flex items-center gap-2 px-4 py-2 text-sm cursor-pointer border-r border-gray-200 whitespace-nowrap ${
                  activeTabId === tab.id
                    ? 'bg-white text-blue-600 font-medium'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
                onClick={() => setActiveTabId(tab.id)}
              >
                <span>{tab.name}</span>
                {tabs.length > 1 && (
                  <button
                    onClick={(e) => {
                      e.stopPropagation()
                      closeTab(tab.id)
                    }}
                    className="p-0.5 hover:bg-gray-200 rounded"
                  >
                    <X className="w-3.5 h-3.5" />
                  </button>
                )}
              </div>
            ))}
            <button
              onClick={addNewTab}
              className="flex items-center gap-1 px-3 py-2 text-gray-500 hover:bg-gray-100 text-sm"
              title="New Tab"
            >
              <Plus className="w-4 h-4" />
            </button>
          </div>

          {/* SQL Result */}
          {sqlResult && (
            <div className="p-4 border-b border-gray-200">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  <h3 className="font-semibold text-gray-900">Generated SQL</h3>
                  {sqlResult.confidence && (
                    <span className={`px-2 py-0.5 text-xs rounded-full ${
                      sqlResult.confidence > 0.8 ? 'bg-green-100 text-green-700' :
                      sqlResult.confidence > 0.6 ? 'bg-yellow-100 text-yellow-700' :
                      'bg-red-100 text-red-700'
                    }`}>
                      {Math.round(sqlResult.confidence * 100)}% confidence
                    </span>
                  )}
                  {sqlResult.llm_used && sqlResult.model && (
                    <span className="px-2 py-0.5 text-xs rounded-full bg-blue-100 text-blue-700">
                      {sqlResult.model}
                    </span>
                  )}
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={handleCopy}
                    className="p-2 text-gray-500 hover:bg-gray-100 rounded-lg"
                    title="Copy SQL"
                  >
                    {copied ? <Check className="w-5 h-5 text-green-500" /> : <Copy className="w-5 h-5" />}
                  </button>
                  <button
                    onClick={handleExecute}
                    disabled={!!sqlResult.error || executeMutation.isPending}
                    className="flex items-center gap-2 px-3 py-1.5 bg-green-600 hover:bg-green-700 text-white text-sm font-medium rounded-lg transition disabled:opacity-50"
                  >
                    <Play className="w-4 h-4" />
                    Execute
                  </button>
                </div>
              </div>

              {sqlResult.error ? (
                <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm">
                  {sqlResult.error}
                </div>
              ) : (
                <pre className="p-3 bg-gray-900 text-gray-100 rounded-lg text-sm font-mono overflow-x-auto">
                  {sqlResult.sql}
                </pre>
              )}

              {sqlResult.explanation && (
                <p className="mt-3 text-sm text-gray-600">{sqlResult.explanation}</p>
              )}
            </div>
          )}

          {/* Execute Result */}
          {executeResult && (
            <div className="p-4">
              <div className="flex items-center justify-between mb-3">
                <h3 className="font-semibold text-gray-900">Results</h3>
                <span className="text-sm text-gray-500">
                  {executeResult.totalRows} rows ({executeResult.executionTime}ms)
                </span>
              </div>

              {executeResult.error ? (
                <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm">
                  {executeResult.error}
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="border-b">
                        {executeResult.columns.map((col) => (
                          <th key={col} className="text-left p-2 font-medium text-gray-700 bg-gray-50">
                            {col}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {executeResult.rows.slice(0, 20).map((row, idx) => (
                        <tr key={idx} className="border-b hover:bg-gray-50">
                          {executeResult.columns.map((col) => (
                            <td key={col} className="p-2 text-gray-600">
                              {String(row[col] ?? '')}
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                  {executeResult.totalRows > 20 && (
                    <p className="mt-2 text-sm text-gray-500 text-center">
                      Showing 20 of {executeResult.totalRows} rows
                    </p>
                  )}
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* History Sidebar */}
      {showHistory && (
        <div className="bg-white rounded-xl border border-gray-200 p-4">
          <h3 className="font-semibold text-gray-900 mb-4">Query History</h3>
          {historyQuery.isLoading ? (
            <div className="flex items-center justify-center py-8">
              <Loader2 className="w-6 h-6 animate-spin text-gray-400" />
            </div>
          ) : historyQuery.data?.length ? (
            <div className="space-y-2">
              {historyQuery.data.map((item) => (
                <div
                  key={item.id}
                  className="p-3 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer"
                  onClick={() => {
                    setQuery(item.naturalLanguage)
                    textToSqlMutation.mutate(item.naturalLanguage)
                  }}
                >
                  <p className="text-sm text-gray-700">{item.naturalLanguage}</p>
                  <p className="text-xs text-gray-400 mt-1">
                    {new Date(item.createdAt).toLocaleString()}
                  </p>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-gray-500 text-center py-8">No query history</p>
          )}
        </div>
      )}
    </div>
  )
}
