import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { RefreshCw, Database, CheckCircle, AlertCircle, Loader2, Brain } from 'lucide-react'
import { vectorService } from '@/services/vectorService'

export function VectorSync() {
  const queryClient = useQueryClient()
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState<{ table_name: string; similarity: number }[]>([])

  const { data: status, isLoading: statusLoading } = useQuery({
    queryKey: ['vectorStatus'],
    queryFn: vectorService.getStatus,
    refetchInterval: 5000,
  })

  const { data: models } = useQuery({
    queryKey: ['ollamaModels'],
    queryFn: vectorService.listModels,
    refetchInterval: 30000,
  })

  const syncMutation = useMutation({
    mutationFn: () => vectorService.triggerSync(),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['vectorStatus'] })
    },
  })

  const searchMutation = useMutation({
    mutationFn: ({ query, topK }: { query: string; topK: number }) =>
      vectorService.semanticSearch(query, topK),
    onSuccess: (results) => {
      setSearchResults(results.map(r => ({ table_name: r.table_name, similarity: r.similarity })))
    },
  })

  const handleSearch = () => {
    if (searchQuery.trim()) {
      searchMutation.mutate({ query: searchQuery, topK: 5 })
    }
  }

  const getStatusIcon = () => {
    if (statusLoading) return <Loader2 className="w-5 h-5 animate-spin text-blue-500" />
    switch (status?.status) {
      case 'syncing':
        return <Loader2 className="w-5 h-5 animate-spin text-yellow-500" />
      case 'completed':
        return <CheckCircle className="w-5 h-5 text-green-500" />
      case 'error':
        return <AlertCircle className="w-5 h-5 text-red-500" />
      default:
        return <Database className="w-5 h-5 text-gray-400" />
    }
  }

  const getStatusColor = () => {
    switch (status?.status) {
      case 'syncing':
        return 'bg-yellow-50 border-yellow-200'
      case 'completed':
        return 'bg-green-50 border-green-200'
      case 'error':
        return 'bg-red-50 border-red-200'
      default:
        return 'bg-gray-50 border-gray-200'
    }
  }

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-4 space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="font-semibold text-gray-900 flex items-center gap-2">
          <Brain className="w-5 h-5 text-purple-600" />
          Vector Database
        </h3>
        
        <button
          onClick={() => syncMutation.mutate()}
          disabled={syncMutation.isPending || status?.status === 'syncing'}
          className="flex items-center gap-2 px-3 py-1.5 bg-purple-600 text-white rounded-lg text-sm font-medium hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <RefreshCw className={`w-4 h-4 ${syncMutation.isPending ? 'animate-spin' : ''}`} />
          {syncMutation.isPending ? 'Syncing...' : 'Sync Schema'}
        </button>
      </div>

      {/* Status Card */}
      <div className={`p-3 rounded-lg border ${getStatusColor()}`}>
        <div className="flex items-center gap-2 mb-2">
          {getStatusIcon()}
          <span className="font-medium text-gray-900 capitalize">{status?.status || 'Unknown'}</span>
        </div>
        <div className="grid grid-cols-2 gap-2 text-sm">
          <div>
            <span className="text-gray-500">Tables Synced:</span>
            <span className="ml-1 font-medium">{status?.tables_synced || 0} / {status?.total_tables || 0}</span>
          </div>
          <div>
            <span className="text-gray-500">Embeddings:</span>
            <span className="ml-1 font-medium">{status?.embedding_count || 0}</span>
          </div>
          {status?.last_sync && (
            <div className="col-span-2">
              <span className="text-gray-500">Last Sync:</span>
              <span className="ml-1 font-medium">{new Date(status.last_sync).toLocaleString()}</span>
            </div>
          )}
        </div>
        {status?.error && (
          <div className="mt-2 text-sm text-red-600">{status.error}</div>
        )}
      </div>

      {/* Ollama Status */}
      <div className="flex items-center gap-2 text-sm">
        <span className="text-gray-500">Ollama:</span>
        {models?.available ? (
          <span className="flex items-center gap-1 text-green-600">
            <CheckCircle className="w-4 h-4" />
            Connected
          </span>
        ) : (
          <span className="flex items-center gap-1 text-red-600">
            <AlertCircle className="w-4 h-4" />
            Not Connected
          </span>
        )}
        {models?.models && models.models.length > 0 && (
          <span className="ml-2 text-gray-400">({models.models.length} models)</span>
        )}
      </div>

      {/* Semantic Search */}
      <div className="border-t pt-4">
        <h4 className="text-sm font-medium text-gray-700 mb-2">Semantic Search</h4>
        <div className="flex gap-2">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
            placeholder="Search tables by meaning..."
            className="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
          />
          <button
            onClick={handleSearch}
            disabled={searchMutation.isPending || !searchQuery.trim()}
            className="px-3 py-2 bg-gray-900 text-white rounded-lg text-sm font-medium hover:bg-gray-800 disabled:opacity-50"
          >
            {searchMutation.isPending ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Search'}
          </button>
        </div>
        
        {searchResults.length > 0 && (
          <div className="mt-3 space-y-2">
            {searchResults.map((result, idx) => (
              <div key={idx} className="flex items-center justify-between px-3 py-2 bg-gray-50 rounded-lg text-sm">
                <span className="font-medium text-gray-900">{result.table_name}</span>
                <span className="text-gray-500">{(result.similarity * 100).toFixed(1)}%</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}