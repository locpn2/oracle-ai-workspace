import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { connectionApi } from '../services/api'

interface ConnectionForm {
  name: string
  host: string
  port: string
  service_name: string
  sid: string
  username: string
  password: string
  connection_type: 'service_name' | 'sid'
}

function ConnectionsPage() {
  const queryClient = useQueryClient()
  const [showForm, setShowForm] = useState(false)
  const [testingId, setTestingId] = useState<string | null>(null)
  const [form, setForm] = useState<ConnectionForm>({
    name: '',
    host: '',
    port: '1521',
    service_name: '',
    sid: '',
    username: '',
    password: '',
    connection_type: 'service_name',
  })

  const { data: connections = [], isLoading } = useQuery({
    queryKey: ['connections'],
    queryFn: async () => {
      const response = await connectionApi.list()
      return response.data
    },
  })

  const createMutation = useMutation({
    mutationFn: (data: ConnectionForm) => connectionApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['connections'] })
      setShowForm(false)
      setForm({
        name: '', host: '', port: '1521', service_name: '', sid: '',
        username: '', password: '', connection_type: 'service_name',
      })
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (id: string) => connectionApi.delete(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['connections'] }),
  })

  const testMutation = useMutation({
    mutationFn: (id: string) => connectionApi.test(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['connections'] })
      setTestingId(null)
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    createMutation.mutate(form)
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Quản lý kết nối Oracle</h2>
          <p className="text-gray-500 mt-1">Thêm và quản lý các kết nối đến CSDL Oracle</p>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
        >
          {showForm ? 'Hủy' : '+ Thêm kết nối'}
        </button>
      </div>

      {showForm && (
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h3 className="text-lg font-semibold mb-4">Thêm kết nối Oracle mới</h3>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Tên kết nối</label>
                <input
                  type="text"
                  required
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm border p-2"
                  placeholder="My Oracle DB"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Host</label>
                <input
                  type="text"
                  required
                  value={form.host}
                  onChange={(e) => setForm({ ...form, host: e.target.value })}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm border p-2"
                  placeholder="localhost"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Port</label>
                <input
                  type="number"
                  required
                  value={form.port}
                  onChange={(e) => setForm({ ...form, port: e.target.value })}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm border p-2"
                  placeholder="1521"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Loại kết nối</label>
                <select
                  value={form.connection_type}
                  onChange={(e) => setForm({ ...form, connection_type: e.target.value as any })}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm border p-2"
                >
                  <option value="service_name">Service Name</option>
                  <option value="sid">SID</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  {form.connection_type === 'service_name' ? 'Service Name' : 'SID'}
                </label>
                <input
                  type="text"
                  required
                  value={form.connection_type === 'service_name' ? form.service_name : form.sid}
                  onChange={(e) => setForm({
                    ...form,
                    service_name: form.connection_type === 'service_name' ? e.target.value : form.service_name,
                    sid: form.connection_type === 'sid' ? e.target.value : form.sid,
                  })}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm border p-2"
                  placeholder={form.connection_type === 'service_name' ? 'ORCL' : 'ORCL'}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Username</label>
                <input
                  type="text"
                  required
                  value={form.username}
                  onChange={(e) => setForm({ ...form, username: e.target.value })}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm border p-2"
                  placeholder="SYSTEM"
                />
              </div>
              <div className="col-span-2">
                <label className="block text-sm font-medium text-gray-700">Password</label>
                <input
                  type="password"
                  required
                  value={form.password}
                  onChange={(e) => setForm({ ...form, password: e.target.value })}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm border p-2"
                />
              </div>
            </div>
            <div className="flex justify-end gap-2">
              <button
                type="button"
                onClick={() => setShowForm(false)}
                className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200"
              >
                Hủy
              </button>
              <button
                type="submit"
                disabled={createMutation.isPending}
                className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50"
              >
                {createMutation.isPending ? 'Đang lưu...' : 'Lưu kết nối'}
              </button>
            </div>
          </form>
        </div>
      )}

      {isLoading ? (
        <div className="text-center py-8">Đang tải...</div>
      ) : connections.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          Chưa có kết nối nào. Hãy thêm kết nối Oracle đầu tiên.
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200" role="table" aria-label="Danh sách kết nối">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tên</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Host</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Trạng thái</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Thao tác</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {connections.map((conn: any) => (
                <tr key={conn.id}>
                  <td className="px-6 py-4 whitespace-nowrap font-medium">{conn.name}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-gray-500">
                    {conn.host}:{conn.port}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 py-1 text-xs rounded-full ${
                      conn.status === 'active' ? 'bg-green-100 text-green-800' :
                      conn.status === 'error' ? 'bg-red-100 text-red-800' :
                      'bg-gray-100 text-gray-800'
                    }`}>
                      {conn.status === 'active' ? 'Kết nối' : conn.status === 'error' ? 'Lỗi' : 'Chưa kết nối'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right">
                    <button
                      onClick={() => {
                        setTestingId(conn.id)
                        testMutation.mutate(conn.id)
                      }}
                      disabled={testMutation.isPending && testingId === conn.id}
                      className="text-primary-600 hover:text-primary-800 mr-3"
                    >
                      Kiểm tra
                    </button>
                    <button
                      onClick={() => deleteMutation.mutate(conn.id)}
                      disabled={deleteMutation.isPending}
                      className="text-red-600 hover:text-red-800"
                    >
                      Xóa
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

export default ConnectionsPage
