import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { vectorApi, connectionApi, schemaApi } from '../services/api'

function VectorPage() {
  const queryClient = useQueryClient()
  const [showForm, setShowForm] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState<any[]>([])
  const [searchingCollection, setSearchingCollection] = useState('')
  const [form, setForm] = useState({
    name: '',
    connection_id: '',
    source_schema: '',
    source_table: '',
    embedding_model: 'text-embedding-3-small',
    text_columns: [] as string[],
  })

  const { data: collections = [] } = useQuery({
    queryKey: ['vector-collections'],
    queryFn: async () => {
      const response = await vectorApi.listCollections()
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

  const { data: schemas = [] } = useQuery({
    queryKey: ['schemas', form.connection_id],
    queryFn: async () => {
      const response = await schemaApi.getSchemas(form.connection_id)
      return response.data
    },
    enabled: !!form.connection_id,
  })

  const { data: tables = [] } = useQuery({
    queryKey: ['tables', form.connection_id, form.source_schema],
    queryFn: async () => {
      const response = await schemaApi.getTables(form.connection_id, form.source_schema)
      return response.data
    },
    enabled: !!form.connection_id && !!form.source_schema,
  })

  const createMutation = useMutation({
    mutationFn: (data: typeof form) => vectorApi.createCollection({
      ...data,
      text_columns: data.text_columns,
    }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['vector-collections'] })
      setShowForm(false)
    },
  })

  const syncMutation = useMutation({
    mutationFn: (id: string) => vectorApi.triggerSync(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['vector-collections'] })
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (id: string) => vectorApi.deleteCollection(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['vector-collections'] })
    },
  })

  const handleSearch = async (collectionId: string) => {
    if (!searchQuery) return
    setSearchingCollection(collectionId)
    try {
      const response = await vectorApi.search({
        collection_id: collectionId,
        query: searchQuery,
        top_k: 5,
      })
      setSearchResults(response.data.results)
    } catch (error) {
      console.error('Search error:', error)
      setSearchResults([])
    }
    setSearchingCollection('')
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Vector Database</h2>
          <p className="text-gray-500 mt-1">Chuyển đổi RDBMS sang Vector DB để tăng cường xử lý AI</p>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
        >
          {showForm ? 'Hủy' : '+ Tạo Vector Collection'}
        </button>
      </div>

      {showForm && (
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h3 className="text-lg font-semibold mb-4">Tạo Vector Collection mới</h3>
          <form
            onSubmit={(e) => {
              e.preventDefault()
              createMutation.mutate(form)
            }}
            className="space-y-4"
          >
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Tên collection</label>
                <input
                  type="text"
                  required
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm border p-2"
                  placeholder="customer_vectors"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Embedding Model</label>
                <select
                  value={form.embedding_model}
                  onChange={(e) => setForm({ ...form, embedding_model: e.target.value })}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm border p-2"
                >
                  <option value="text-embedding-3-small">OpenAI text-embedding-3-small</option>
                  <option value="text-embedding-3-large">OpenAI text-embedding-3-large</option>
                  <option value="sentence-transformers">Sentence Transformers (Local)</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Kết nối Oracle</label>
                <select
                  value={form.connection_id}
                  onChange={(e) => setForm({ ...form, connection_id: e.target.value, source_schema: '', source_table: '' })}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm border p-2"
                  required
                >
                  <option value="">-- Chọn kết nối --</option>
                  {connections.map((c: any) => (
                    <option key={c.id} value={c.id}>{c.name}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Schema</label>
                <select
                  value={form.source_schema}
                  onChange={(e) => setForm({ ...form, source_schema: e.target.value, source_table: '' })}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm border p-2"
                  disabled={!form.connection_id}
                  required
                >
                  <option value="">-- Chọn schema --</option>
                  {schemas.map((s: string) => (
                    <option key={s} value={s}>{s}</option>
                  ))}
                </select>
              </div>
              <div className="col-span-2">
                <label className="block text-sm font-medium text-gray-700">Bảng nguồn</label>
                <select
                  value={form.source_table}
                  onChange={(e) => setForm({ ...form, source_table: e.target.value })}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm border p-2"
                  disabled={!form.source_schema}
                  required
                >
                  <option value="">-- Chọn bảng --</option>
                  {tables.map((t: any) => (
                    <option key={t.name} value={t.name}>{t.name}</option>
                  ))}
                </select>
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
                {createMutation.isPending ? 'Đang tạo...' : 'Tạo Collection'}
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="grid grid-cols-3 gap-6">
        <div className="col-span-2">
          <div className="bg-white rounded-lg shadow">
            <div className="p-4 border-b">
              <h3 className="font-semibold">Danh sách Vector Collections</h3>
            </div>
            {collections.length === 0 ? (
              <div className="p-8 text-center text-gray-500">
                Chưa có collection nào. Tạo mới để bắt đầu vectorization.
              </div>
            ) : (
              <div className="divide-y">
                {collections.map((col: any) => (
                  <div key={col.id} className="p-4">
                    <div className="flex justify-between items-start mb-3">
                      <div>
                        <h4 className="font-medium">{col.name}</h4>
                        <p className="text-sm text-gray-500">
                          {col.source_schema}.{col.source_table} | {col.record_count} records
                        </p>
                        <p className="text-xs text-gray-400">
                          Model: {col.embedding_model} | Status: {col.status}
                        </p>
                      </div>
                      <div className="flex gap-2">
                        <button
                          onClick={() => syncMutation.mutate(col.id)}
                          disabled={syncMutation.isPending}
                          className="px-3 py-1 text-sm bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200"
                        >
                          Sync
                        </button>
                        <button
                          onClick={() => {
                            if (confirm('Xóa collection này?')) deleteMutation.mutate(col.id)
                          }}
                          className="px-3 py-1 text-sm bg-red-100 text-red-700 rounded-lg hover:bg-red-200"
                        >
                          Xóa
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        <div className="col-span-1">
          <div className="bg-white rounded-lg shadow p-4">
            <h3 className="font-semibold mb-4">Semantic Search</h3>
            <p className="text-sm text-gray-500 mb-4">
              Tìm kiếm dữ liệu bằng ngôn ngữ tự nhiên thay vì SQL
            </p>
            
            <div className="space-y-3">
              <select
                value={searchingCollection || (collections[0]?.id || '')}
                onChange={(e) => setSearchingCollection(e.target.value)}
                className="w-full rounded-md border border-gray-300 p-2 text-sm"
              >
                {collections.map((c: any) => (
                  <option key={c.id} value={c.id}>{c.name}</option>
                ))}
              </select>
              <textarea
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="VD: Tìm khách hàng ở Hà Nội"
                className="w-full p-2 border border-gray-300 rounded-lg text-sm h-20 resize-none"
              />
              <button
                onClick={() => handleSearch(searchingCollection || collections[0]?.id)}
                disabled={!searchQuery || !collections.length}
                className="w-full px-4 py-2 bg-primary-600 text-white rounded-lg text-sm disabled:opacity-50"
              >
                Tìm kiếm
              </button>
            </div>

            {searchResults.length > 0 && (
              <div className="mt-4 space-y-2">
                <h4 className="font-medium text-sm">Kết quả:</h4>
                {searchResults.map((result, idx) => (
                  <div key={idx} className="p-3 bg-gray-50 rounded-lg text-sm">
                    <div className="flex justify-between items-start mb-1">
                      <span className="font-medium">#{idx + 1}</span>
                      <span className="text-primary-600">{(result.score * 100).toFixed(1)}%</span>
                    </div>
                    <p className="text-gray-600 truncate">
                      {result.document?.text || JSON.stringify(result.document)}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default VectorPage
