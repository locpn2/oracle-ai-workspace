import { apiClient } from '@/lib/api'
import type { Table, ERDNode, ERDEdge, SchemaGroup } from '@/types/schema'

export interface ERDData {
  nodes: ERDNode[]
  edges: ERDEdge[]
}

export const schemaService = {
  getTables: async (): Promise<Table[]> => {
    const response = await apiClient.get<Table[]>('/schema/tables')
    return response.data
  },
  
  getTableDetails: async (tableName: string): Promise<Table> => {
    const response = await apiClient.get<Table>(`/schema/tables/${tableName}`)
    return response.data
  },
  
  getERD: async (): Promise<ERDData> => {
    const response = await apiClient.get<ERDData>('/schema/erd')
    return response.data
  },
  
  getGroups: async (): Promise<SchemaGroup[]> => {
    const response = await apiClient.get<SchemaGroup[]>('/schema/groups')
    return response.data
  },
  
  createGroup: async (group: Omit<SchemaGroup, 'id'>): Promise<SchemaGroup> => {
    const response = await apiClient.post<SchemaGroup>('/schema/groups', group)
    return response.data
  },
  
  updateGroup: async (id: string, group: Partial<SchemaGroup>): Promise<SchemaGroup> => {
    const response = await apiClient.patch<SchemaGroup>(`/schema/groups/${id}`, group)
    return response.data
  },
  
  deleteGroup: async (id: string): Promise<void> => {
    await apiClient.delete(`/schema/groups/${id}`)
  },
}
