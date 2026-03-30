import { apiClient } from '@/lib/api'
import type { QueryRequest, QueryResponse, ExecuteRequest, ExecuteResponse, QueryHistory } from '@/types/query'

export const queryService = {
  textToSQL: async (data: QueryRequest): Promise<QueryResponse> => {
    const response = await apiClient.post<QueryResponse>('/query/text-to-sql', data)
    return response.data
  },
  
  execute: async (data: ExecuteRequest): Promise<ExecuteResponse> => {
    const response = await apiClient.post<ExecuteResponse>('/query/execute', data)
    return response.data
  },
  
  getHistory: async (limit = 50): Promise<QueryHistory[]> => {
    const response = await apiClient.get<QueryHistory[]>('/query/history', {
      params: { limit },
    })
    return response.data
  },
  
  preview: async (sql: string): Promise<{ valid: boolean; error?: string }> => {
    const response = await apiClient.post<{ valid: boolean; error?: string }>('/query/preview', { sql })
    return response.data
  },
  
  export: async (sql: string, format: 'csv' | 'json' | 'xlsx' = 'csv'): Promise<Blob> => {
    const response = await apiClient.post('/query/export', {
      sql,
      page: 1,
      page_size: 10000,
      format,
    }, {
      responseType: 'blob',
    })
    return response.data
  },
}
