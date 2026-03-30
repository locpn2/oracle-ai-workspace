import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Plus, Search, Loader2, Table2, ChevronRight } from 'lucide-react'
import { schemaService } from '@/services/schemaService'
import { VectorSync } from '@/components/vector/VectorSync'

const GROUP_COLORS = [
  '#ef4444', '#f97316', '#eab308', '#22c55e', '#06b6d4', '#3b82f6', '#8b5cf6', '#ec4899'
]

export function SchemaPage() {
  const queryClient = useQueryClient()
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedGroup, setSelectedGroup] = useState<string | null>(null)
  const [expandedTable, setExpandedTable] = useState<string | null>(null)
  const [showNewGroup, setShowNewGroup] = useState(false)
  const [newGroupName, setNewGroupName] = useState('')

  const tablesQuery = useQuery({
    queryKey: ['tables'],
    queryFn: schemaService.getTables,
  })

  const groupsQuery = useQuery({
    queryKey: ['groups'],
    queryFn: schemaService.getGroups,
  })

  const createGroupMutation = useMutation({
    mutationFn: (name: string) =>
      schemaService.createGroup({
        name,
        color: GROUP_COLORS[Math.floor(Math.random() * GROUP_COLORS.length)],
        tableNames: [],
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['groups'] })
      setShowNewGroup(false)
      setNewGroupName('')
    },
  })

  const filteredTables = tablesQuery.data?.filter((table) => {
    const matchesSearch = table.name.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesGroup = !selectedGroup || 
      groupsQuery.data?.find(g => g.id === selectedGroup)?.tableNames.includes(table.name)
    return matchesSearch && matchesGroup
  })

  const handleCreateGroup = () => {
    if (newGroupName.trim()) {
      createGroupMutation.mutate(newGroupName.trim())
    }
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
      {/* Sidebar - Groups */}
      <div className="bg-white rounded-xl border border-gray-200 p-4">
        <div className="flex items-center justify-between mb-4">
          <h2 className="font-semibold text-gray-900">Schema Groups</h2>
          <button
            onClick={() => setShowNewGroup(true)}
            className="p-1.5 text-blue-600 hover:bg-blue-50 rounded-lg"
            title="New Group"
          >
            <Plus className="w-5 h-5" />
          </button>
        </div>

        {showNewGroup && (
          <div className="mb-4 p-3 bg-gray-50 rounded-lg">
            <input
              type="text"
              value={newGroupName}
              onChange={(e) => setNewGroupName(e.target.value)}
              placeholder="Group name..."
              className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm mb-2"
              onKeyDown={(e) => e.key === 'Enter' && handleCreateGroup()}
            />
            <div className="flex gap-2">
              <button
                onClick={handleCreateGroup}
                className="flex-1 py-1.5 bg-blue-600 text-white text-sm rounded-lg"
              >
                Create
              </button>
              <button
                onClick={() => setShowNewGroup(false)}
                className="flex-1 py-1.5 bg-gray-200 text-gray-700 text-sm rounded-lg"
              >
                Cancel
              </button>
            </div>
          </div>
        )}

        <div className="space-y-2">
          <button
            onClick={() => setSelectedGroup(null)}
            className={`w-full flex items-center justify-between p-2 rounded-lg text-left ${
              !selectedGroup ? 'bg-blue-50 text-blue-700' : 'hover:bg-gray-50'
            }`}
          >
            <span className="text-sm font-medium">All Tables</span>
            <span className="text-xs bg-gray-200 px-2 py-0.5 rounded-full">
              {tablesQuery.data?.length || 0}
            </span>
          </button>

          {groupsQuery.data?.map((group) => (
            <div
              key={group.id}
              className={`flex items-center justify-between p-2 rounded-lg cursor-pointer ${
                selectedGroup === group.id ? 'bg-blue-50' : 'hover:bg-gray-50'
              }`}
              onClick={() => setSelectedGroup(selectedGroup === group.id ? null : group.id)}
            >
              <div className="flex items-center gap-2">
                <div
                  className="w-3 h-3 rounded-full"
                  style={{ backgroundColor: group.color }}
                />
                <span className="text-sm font-medium">{group.name}</span>
              </div>
              <span className="text-xs text-gray-500">{group.tableNames.length}</span>
            </div>
          ))}
        </div>

        {/* Vector Sync Component */}
        <div className="mt-4 pt-4 border-t">
          <VectorSync />
        </div>
      </div>

      {/* Main Content - Tables */}
      <div className="lg:col-span-3 bg-white rounded-xl border border-gray-200">
        {/* Search */}
        <div className="p-4 border-b border-gray-200">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search tables..."
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            />
          </div>
        </div>

        {/* Table List */}
        <div className="p-4">
          {tablesQuery.isLoading ? (
            <div className="flex items-center justify-center py-12">
              <Loader2 className="w-8 h-8 animate-spin text-gray-400" />
            </div>
          ) : filteredTables?.length ? (
            <div className="space-y-2">
              {filteredTables.map((table) => (
                <div key={table.name} className="border border-gray-200 rounded-lg">
                  <div
                    className="flex items-center justify-between p-3 cursor-pointer hover:bg-gray-50"
                    onClick={() => setExpandedTable(expandedTable === table.name ? null : table.name)}
                  >
                    <div className="flex items-center gap-3">
                      <Table2 className="w-5 h-5 text-gray-400" />
                      <div>
                        <p className="font-medium text-gray-900">{table.name}</p>
                        <p className="text-xs text-gray-500">{table.columns.length} columns</p>
                      </div>
                    </div>
                    <ChevronRight className={`w-5 h-5 text-gray-400 transition-transform ${
                      expandedTable === table.name ? 'rotate-90' : ''
                    }`} />
                  </div>

                  {expandedTable === table.name && (
                    <div className="border-t border-gray-200 p-3 bg-gray-50">
                      <table className="w-full text-sm">
                        <thead>
                          <tr className="text-left text-gray-500">
                            <th className="pb-2 font-medium">Column</th>
                            <th className="pb-2 font-medium">Type</th>
                            <th className="pb-2 font-medium">Nullable</th>
                            <th className="pb-2 font-medium">Key</th>
                          </tr>
                        </thead>
                        <tbody>
                          {table.columns.map((col) => (
                            <tr key={col.name} className="border-t border-gray-200">
                              <td className="py-2 font-mono text-sm">{col.name}</td>
                              <td className="py-2 text-gray-600">{col.type}</td>
                              <td className="py-2">{col.nullable ? 'Yes' : 'No'}</td>
                              <td className="py-2">
                                {col.isPrimaryKey && (
                                  <span className="px-2 py-0.5 bg-yellow-100 text-yellow-700 text-xs rounded">
                                    PK
                                  </span>
                                )}
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-12 text-gray-500">
              No tables found
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
