import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { groupsApi, connectionApi, schemaApi } from '../services/api'

function GroupsPage() {
  const queryClient = useQueryClient()
  const [showForm, setShowForm] = useState(false)
  const [selectedGroup, setSelectedGroup] = useState<string | null>(null)
  const [showTableSelector, setShowTableSelector] = useState(false)
  const [form, setForm] = useState({
    name: '',
    description: '',
    color: '#3B82F6',
  })

  const { data: groups = [] } = useQuery({
    queryKey: ['groups'],
    queryFn: async () => {
      const response = await groupsApi.list()
      return response.data
    },
  })

  const { data: connections = [] } = useQuery({
    queryKey: ['connections'],
    queryFn: async () => {
      const response = await connectionApi.list()
      return response.data
    },
  })

  const { data: groupTables = [] } = useQuery({
    queryKey: ['group-tables', selectedGroup],
    queryFn: async () => {
      if (!selectedGroup) return []
      const response = await groupsApi.getTables(selectedGroup)
      return response.data
    },
    enabled: !!selectedGroup,
  })

  const createMutation = useMutation({
    mutationFn: (data: typeof form) => groupsApi.create({
      ...data,
      connection_id: null,
    }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['groups'] })
      setShowForm(false)
      setForm({ name: '', description: '', color: '#3B82F6' })
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (id: string) => groupsApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['groups'] })
      setSelectedGroup(null)
    },
  })

  const removeTableMutation = useMutation({
    mutationFn: ({ groupId, tableId }: { groupId: string; tableId: string }) =>
      groupsApi.removeTable(groupId, tableId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['group-tables'] })
    },
  })

  const selectedGroupData = groups.find((g: any) => g.id === selectedGroup)

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Quản lý nhóm dữ liệu</h2>
          <p className="text-gray-500 mt-1">Tổ chức và phân nhóm các bảng dữ liệu theo domain</p>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
        >
          {showForm ? 'Hủy' : '+ Tạo nhóm mới'}
        </button>
      </div>

      {showForm && (
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h3 className="text-lg font-semibold mb-4">Tạo nhóm dữ liệu mới</h3>
          <form
            onSubmit={(e) => {
              e.preventDefault()
              createMutation.mutate(form)
            }}
            className="space-y-4"
          >
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Tên nhóm</label>
                <input
                  type="text"
                  required
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm border p-2"
                  placeholder="VD: Sales, HR, Finance"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Màu sắc</label>
                <input
                  type="color"
                  value={form.color}
                  onChange={(e) => setForm({ ...form, color: e.target.value })}
                  className="mt-1 h-10 w-full rounded-md border-gray-300"
                />
              </div>
              <div className="col-span-2">
                <label className="block text-sm font-medium text-gray-700">Mô tả</label>
                <textarea
                  value={form.description}
                  onChange={(e) => setForm({ ...form, description: e.target.value })}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm border p-2"
                  rows={2}
                />
              </div>
            </div>
            <div className="flex justify-end gap-2">
              <button
                type="button"
                onClick={() => setShowForm(false)}
                className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg"
              >
                Hủy
              </button>
              <button
                type="submit"
                disabled={createMutation.isPending}
                className="px-4 py-2 bg-primary-600 text-white rounded-lg disabled:opacity-50"
              >
                {createMutation.isPending ? 'Đang tạo...' : 'Tạo nhóm'}
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="grid grid-cols-3 gap-6">
        <div className="col-span-1">
          <div className="bg-white rounded-lg shadow">
            <div className="p-4 border-b">
              <h3 className="font-semibold">Danh sách nhóm</h3>
            </div>
            <div className="p-2">
              {groups.length === 0 ? (
                <p className="text-sm text-gray-500 p-2">Chưa có nhóm nào</p>
              ) : (
                groups.map((group: any) => (
                  <button
                    key={group.id}
                    onClick={() => setSelectedGroup(group.id)}
                    className={`w-full text-left p-3 rounded-lg mb-1 transition-colors ${
                      selectedGroup === group.id
                        ? 'bg-primary-50 border-2 border-primary-500'
                        : 'hover:bg-gray-50'
                    }`}
                    style={{ borderLeftColor: group.color, borderLeftWidth: '4px' }}
                  >
                    <div className="font-medium">{group.name}</div>
                    <div className="text-xs text-gray-500">{group.description || 'Không có mô tả'}</div>
                  </button>
                ))
              )}
            </div>
          </div>
        </div>

        <div className="col-span-2">
          {selectedGroupData ? (
            <div className="bg-white rounded-lg shadow">
              <div className="p-4 border-b flex justify-between items-center">
                <div>
                  <h3 className="text-lg font-semibold" style={{ color: selectedGroupData.color }}>
                    {selectedGroupData.name}
                  </h3>
                  <p className="text-sm text-gray-500">{selectedGroupData.description}</p>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => setShowTableSelector(true)}
                    className="px-3 py-1 text-sm bg-primary-100 text-primary-700 rounded-lg hover:bg-primary-200"
                  >
                    + Thêm bảng
                  </button>
                  <button
                    onClick={() => {
                      if (confirm('Xóa nhóm này?')) deleteMutation.mutate(selectedGroupData.id)
                    }}
                    className="px-3 py-1 text-sm bg-red-100 text-red-700 rounded-lg hover:bg-red-200"
                  >
                    Xóa nhóm
                  </button>
                </div>
              </div>

              <div className="p-4">
                {groupTables.length === 0 ? (
                  <p className="text-gray-500 text-center py-8">
                    Nhóm này chưa có bảng nào. Nhấn "Thêm bảng" để bắt đầu.
                  </p>
                ) : (
                  <div className="space-y-2">
                    {groupTables.map((table: any) => (
                      <div
                        key={table.id}
                        className="flex justify-between items-center p-3 bg-gray-50 rounded-lg"
                      >
                        <div>
                          <span className="font-medium">{table.table_name}</span>
                          <span className="text-gray-500 text-sm ml-2">({table.schema_name})</span>
                        </div>
                        <button
                          onClick={() => removeTableMutation.mutate({
                            groupId: selectedGroupData.id,
                            tableId: table.id,
                          })}
                          className="text-red-600 hover:text-red-800"
                        >
                          ✕
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="bg-white rounded-lg shadow p-8 text-center text-gray-500">
              Chọn một nhóm để xem chi tiết
            </div>
          )}
        </div>
      </div>

      {showTableSelector && (
        <TableSelector
          groupId={selectedGroup!}
          onClose={() => setShowTableSelector(false)}
          onSuccess={() => {
            setShowTableSelector(false)
            queryClient.invalidateQueries({ queryKey: ['group-tables'] })
          }}
        />
      )}
    </div>
  )
}

function TableSelector({ groupId, onClose, onSuccess }: {
  groupId: string
  onClose: () => void
  onSuccess: () => void
}) {
  const [selectedConnection, setSelectedConnection] = useState('')
  const [selectedSchema, setSelectedSchema] = useState('')
  const [selectedTable, setSelectedTable] = useState('')

  const { data: connections = [] } = useQuery({
    queryKey: ['connections'],
    queryFn: async () => {
      const response = await connectionApi.list()
      return response.data
    },
  })

  const { data: schemas = [] } = useQuery({
    queryKey: ['schemas', selectedConnection],
    queryFn: async () => {
      const response = await schemaApi.getSchemas(selectedConnection)
      return response.data
    },
    enabled: !!selectedConnection,
  })

  const { data: tables = [] } = useQuery({
    queryKey: ['tables', selectedConnection, selectedSchema],
    queryFn: async () => {
      const response = await schemaApi.getTables(selectedConnection, selectedSchema)
      return response.data
    },
    enabled: !!selectedConnection && !!selectedSchema,
  })

  const addTableMutation = useMutation({
    mutationFn: () => groupsApi.addTable(groupId, selectedConnection, selectedSchema, selectedTable),
    onSuccess,
  })

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full">
        <div className="p-4 border-b flex justify-between items-center">
          <h3 className="font-semibold">Thêm bảng vào nhóm</h3>
          <button onClick={onClose} className="text-gray-500">✕</button>
        </div>
        <div className="p-4 space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Kết nối</label>
            <select
              value={selectedConnection}
              onChange={(e) => {
                setSelectedConnection(e.target.value)
                setSelectedSchema('')
                setSelectedTable('')
              }}
              className="w-full rounded-md border border-gray-300 p-2"
            >
              <option value="">-- Chọn kết nối --</option>
              {connections.map((c: any) => (
                <option key={c.id} value={c.id}>{c.name}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Schema</label>
            <select
              value={selectedSchema}
              onChange={(e) => {
                setSelectedSchema(e.target.value)
                setSelectedTable('')
              }}
              className="w-full rounded-md border border-gray-300 p-2"
              disabled={!selectedConnection}
            >
              <option value="">-- Chọn schema --</option>
              {schemas.map((s: string) => (
                <option key={s} value={s}>{s}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Bảng</label>
            <select
              value={selectedTable}
              onChange={(e) => setSelectedTable(e.target.value)}
              className="w-full rounded-md border border-gray-300 p-2"
              disabled={!selectedSchema}
            >
              <option value="">-- Chọn bảng --</option>
              {tables.map((t: any) => (
                <option key={t.name} value={t.name}>{t.name}</option>
              ))}
            </select>
          </div>
        </div>
        <div className="p-4 border-t flex justify-end gap-2">
          <button onClick={onClose} className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg">
            Hủy
          </button>
          <button
            onClick={() => addTableMutation.mutate()}
            disabled={!selectedTable || addTableMutation.isPending}
            className="px-4 py-2 bg-primary-600 text-white rounded-lg disabled:opacity-50"
          >
            {addTableMutation.isPending ? 'Đang thêm...' : 'Thêm'}
          </button>
        </div>
      </div>
    </div>
  )
}

export default GroupsPage
