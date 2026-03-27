import { apiClient } from '@/lib/api'

export interface VectorSyncStatus {
  last_sync: string | null
  status: 'idle' | 'syncing' | 'completed' | 'error'
  tables_synced: number
  total_tables: number
  embedding_count: number
  unique_tables: number
  error: string | null
}

export interface SemanticSearchResult {
  table_name: string
  column_name: string | null
  description: string
  similarity: number
}

export interface SyncResult {
  message: string
  tables_synced?: number
  total_tables?: number
  last_sync?: string
}

export interface ModelInfo {
  available: boolean
  models: string[]
  current_model: string
  current_embed_model: string
  error?: string
}

export const vectorService = {
  triggerSync: async (tableName?: string): Promise<SyncResult> => {
    const response = await apiClient.post<SyncResult>('/vector/sync', { table_name: tableName })
    return response.data
  },

  getStatus: async (): Promise<VectorSyncStatus> => {
    const response = await apiClient.get<VectorSyncStatus>('/vector/status')
    return response.data
  },

  semanticSearch: async (query: string, topK: number = 5): Promise<SemanticSearchResult[]> => {
    const response = await apiClient.post<{ query: string; results: SemanticSearchResult[] }>(
      '/vector/search',
      { query, top_k: topK }
    )
    return response.data.results
  },

  clearEmbeddings: async (): Promise<{ message: string }> => {
    const response = await apiClient.delete<{ message: string }>('/vector/clear')
    return response.data
  },

  listModels: async (): Promise<ModelInfo> => {
    const response = await apiClient.get<ModelInfo>('/vector/models')
    return response.data
  },
}