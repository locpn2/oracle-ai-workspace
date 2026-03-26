import axios from 'axios'

const API_BASE = '/api/v1'

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const connectionApi = {
  list: () => api.get('/connections'),
  get: (id: string) => api.get(`/connections/${id}`),
  create: (data: any) => api.post('/connections', data),
  update: (id: string, data: any) => api.put(`/connections/${id}`, data),
  delete: (id: string) => api.delete(`/connections/${id}`),
  test: (id: string) => api.post(`/connections/${id}/test`),
  testDirect: (data: any) => api.post('/connections/test-direct', data),
}

export const schemaApi = {
  getSchemas: (connectionId: string) => api.get(`/schemas/${connectionId}/schemas`),
  getTables: (connectionId: string, schema: string) => 
    api.get(`/schemas/${connectionId}/schemas/${schema}/tables`),
  getTableDetails: (connectionId: string, schema: string, table: string) =>
    api.get(`/schemas/${connectionId}/schemas/${schema}/tables/${table}`),
  getERD: (connectionId: string, schemaName?: string) =>
    api.get(`/schemas/${connectionId}/erd`, { params: { schema_name: schemaName } }),
  executeQuery: (connectionId: string, sql: string, fetchSize?: number) =>
    api.get(`/schemas/${connectionId}/query`, { params: { sql, fetch_size: fetchSize || 100 } }),
}

export const aiQueryApi = {
  textToSql: (data: { connection_id: string; natural_language: string; context_schema?: string }) =>
    api.post('/ai/query', data),
  executeQuery: (connectionId: string, sql: string, maxRows?: number) =>
    api.post(`/ai/query/execute?connection_id=${connectionId}&sql=${encodeURIComponent(sql)}&max_rows=${maxRows || 100}`),
  getHistory: (connectionId?: string, limit?: number) =>
    api.get('/ai/query/history', { params: { connection_id: connectionId, limit: limit || 50 } }),
  explain: (connectionId: string, sql: string) =>
    api.post(`/ai/query/explain?connection_id=${connectionId}&sql=${encodeURIComponent(sql)}`),
}

export const groupsApi = {
  list: (connectionId?: string) => api.get('/groups', { params: { connection_id: connectionId } }),
  get: (id: string) => api.get(`/groups/${id}`),
  create: (data: any) => api.post('/groups', data),
  update: (id: string, data: any) => api.put(`/groups/${id}`, data),
  delete: (id: string) => api.delete(`/groups/${id}`),
  addTable: (groupId: string, connectionId: string, schemaName: string, tableName: string) =>
    api.post(`/groups/${groupId}/tables`, null, {
      params: { connection_id: connectionId, schema_name: schemaName, table_name: tableName }
    }),
  removeTable: (groupId: string, tableId: string) =>
    api.delete(`/groups/${groupId}/tables/${tableId}`),
  getTables: (groupId: string) => api.get(`/groups/${groupId}/tables`),
}

export const vectorApi = {
  listCollections: () => api.get('/vector/collections'),
  createCollection: (data: any) => api.post('/vector/collections', data),
  deleteCollection: (id: string) => api.delete(`/vector/collections/${id}`),
  triggerSync: (id: string) => api.post(`/vector/sync/${id}`),
  getSyncStatus: (id: string) => api.get(`/vector/sync/status/${id}`),
  search: (data: { collection_id: string; query: string; top_k?: number; filter?: any }) =>
    api.post('/vector/search', data),
  getStats: (id: string) => api.get(`/vector/stats/${id}`),
}

export default api
