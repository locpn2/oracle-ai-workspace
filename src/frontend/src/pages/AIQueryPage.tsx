import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { connectionApi, aiQueryApi } from '../services/api'

function AIQueryPage() {
  const queryClient = useQueryClient()
  const [selectedConnection, setSelectedConnection] = useState('')
  const [question, setQuestion] = useState('')
  const [generatedSql, setGeneratedSql] = useState('')
  const [queryResults, setQueryResults] = useState<any>(null)

  const { data: connections = [] } = useQuery({
    queryKey: ['connections'],
    queryFn: async () => {
      const response = await connectionApi.list()
      return response.data
    },
  })

  const { data: history = [] } = useQuery({
    queryKey: ['ai-history', selectedConnection],
    queryFn: async () => {
      const response = await aiQueryApi.getHistory(selectedConnection)
      return response.data
    },
  })

  const textToSqlMutation = useMutation({
    mutationFn: () => aiQueryApi.textToSql({
      connection_id: selectedConnection,
      natural_language: question,
    }),
    onSuccess: (response) => {
      setGeneratedSql(response.data.generated_sql)
    },
  })

  const executeMutation = useMutation({
    mutationFn: (sql: string) => aiQueryApi.executeQuery(selectedConnection, sql),
    onSuccess: (response) => {
      setQueryResults(response.data)
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!selectedConnection || !question) return
    textToSqlMutation.mutate()
  }

  const handleExecute = () => {
    if (!generatedSql) return
    executeMutation.mutate(generatedSql)
  }

  return (
    <div>
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900">AI Truy vấn dữ liệu</h2>
        <p className="text-gray-500 mt-1">Sử dụng AI để truy vấn dữ liệu bằng ngôn ngữ tự nhiên</p>
      </div>

      <div className="grid grid-cols-4 gap-6">
        <div className="col-span-1">
          <div className="bg-white rounded-lg shadow p-4">
            <h3 className="font-semibold mb-3">Chọn kết nối</h3>
            <select
              value={selectedConnection}
              onChange={(e) => setSelectedConnection(e.target.value)}
              className="w-full rounded-md border border-gray-300 p-2"
            >
              <option value="">-- Chọn kết nối --</option>
              {connections.map((c: any) => (
                <option key={c.id} value={c.id}>{c.name}</option>
              ))}
            </select>
          </div>

          <div className="bg-white rounded-lg shadow p-4 mt-4">
            <h3 className="font-semibold mb-3">Lịch sử truy vấn</h3>
            <div className="space-y-2 max-h-96 overflow-y-auto">
              {history.map((h: any) => (
                <button
                  key={h.id}
                  onClick={() => {
                    setQuestion(h.natural_language)
                    setGeneratedSql(h.generated_sql)
                  }}
                  className="w-full text-left p-2 rounded hover:bg-gray-100 text-sm"
                >
                  <div className="truncate">{h.natural_language}</div>
                  <div className="text-xs text-gray-500 truncate">{h.generated_sql}</div>
                </button>
              ))}
              {history.length === 0 && (
                <p className="text-sm text-gray-500">Chưa có lịch sử</p>
              )}
            </div>
          </div>
        </div>

        <div className="col-span-3 space-y-4">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="font-semibold mb-4">Đặt câu hỏi bằng ngôn ngữ tự nhiên</h3>
            <form onSubmit={handleSubmit}>
              <textarea
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Ví dụ: Liệt kê tất cả các khách hàng có đơn hàng trong tháng này"
                className="w-full p-3 border border-gray-300 rounded-lg h-24 resize-none"
                disabled={!selectedConnection}
              />
              <div className="flex justify-end mt-3">
                <button
                  type="submit"
                  disabled={!selectedConnection || !question || textToSqlMutation.isPending}
                  className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50"
                >
                  {textToSqlMutation.isPending ? 'Đang xử lý...' : 'Tạo SQL'}
                </button>
              </div>
            </form>
          </div>

          {textToSqlMutation.data?.data && (
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex justify-between items-center mb-4">
                <h3 className="font-semibold">SQL được tạo</h3>
                {textToSqlMutation.data.data.explanation && (
                  <p className="text-sm text-gray-500">{textToSqlMutation.data.data.explanation}</p>
                )}
              </div>
              <pre className="bg-gray-50 p-4 rounded-lg overflow-x-auto text-sm font-mono">
                {generatedSql}
              </pre>
              <div className="flex justify-end gap-2 mt-4">
                <button
                  onClick={() => navigator.clipboard.writeText(generatedSql)}
                  className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200"
                >
                  Copy SQL
                </button>
                <button
                  onClick={handleExecute}
                  disabled={executeMutation.isPending}
                  className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50"
                >
                  {executeMutation.isPending ? 'Đang chạy...' : 'Thực thi SQL'}
                </button>
              </div>
            </div>
          )}

          {queryResults && (
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex justify-between items-center mb-4">
                <h3 className="font-semibold">Kết quả</h3>
                <div className="text-sm text-gray-500">
                  {queryResults.row_count} dòng | Thời gian: {queryResults.execution_time_ms}ms
                </div>
              </div>
              {queryResults.columns.length > 0 ? (
                <div className="overflow-x-auto">
                  <table className="min-w-full text-sm">
                    <thead>
                      <tr className="bg-gray-50">
                        {queryResults.columns.map((col: string, idx: number) => (
                          <th key={idx} className="px-4 py-2 text-left font-medium">{col}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {queryResults.rows.map((row: any[], idx: number) => (
                        <tr key={idx} className="border-t">
                          {row.map((cell, cidx) => (
                            <td key={cidx} className="px-4 py-2">{String(cell ?? '')}</td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <p className="text-gray-500">Không có kết quả</p>
              )}
            </div>
          )}

          {executeMutation.error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
              <strong>Lỗi:</strong> {String(executeMutation.error)}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default AIQueryPage
