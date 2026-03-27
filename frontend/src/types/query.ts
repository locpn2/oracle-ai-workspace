export interface QueryRequest {
  natural_language: string
  context?: string
}

export interface QueryResponse {
  sql: string
  confidence: number
  explanation?: string
  error?: string
}

export interface ExecuteRequest {
  sql: string
  page?: number
  pageSize?: number
}

export interface ExecuteResponse {
  columns: string[]
  rows: Record<string, unknown>[]
  totalRows: number
  page: number
  pageSize: number
  executionTime: number
  error?: string
}

export interface QueryHistory {
  id: string
  naturalLanguage: string
  sql: string
  createdAt: string
  success: boolean
}
