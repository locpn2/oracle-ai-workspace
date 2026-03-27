import { useCallback } from 'react'
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
  addEdge,
} from '@xyflow/react'
import type { Connection, Node, Edge } from '@xyflow/react'
import '@xyflow/react/dist/style.css'
import { useQuery } from '@tanstack/react-query'
import { Loader2, RefreshCw, Download } from 'lucide-react'
import { schemaService } from '@/services/schemaService'
import { TableNode } from '@/components/erd/TableNode'

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const nodeTypes: any = {
  table: TableNode,
}

export function ERDPage() {
  const [nodes, setNodes, onNodesChange] = useNodesState<Node>([])
  const [edges, setEdges, onEdgesChange] = useEdgesState<Edge>([])

  const { data, isLoading, error, refetch, isFetching } = useQuery({
    queryKey: ['erd'],
    queryFn: schemaService.getERD,
    staleTime: 5 * 60 * 1000,
  })

  const onConnect = useCallback(
    (connection: Connection) => setEdges((eds) => addEdge(connection, eds)),
    [setEdges]
  )

  if (data && nodes.length === 0) {
    setNodes(data.nodes)
    setEdges(data.edges)
  }

  return (
    <div className="h-[calc(100vh-8rem)] bg-white rounded-xl border border-gray-200 overflow-hidden">
      <div className="flex items-center justify-between px-4 py-3 border-b border-gray-200">
        <div>
          <h1 className="text-lg font-semibold text-gray-900">ERD Viewer</h1>
          <p className="text-sm text-gray-500">
            {nodes.length} tables, {edges.length} relationships
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => refetch()}
            disabled={isFetching}
            className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition"
            title="Refresh"
          >
            <RefreshCw className={`w-5 h-5 ${isFetching ? 'animate-spin' : ''}`} />
          </button>
          <button
            className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition"
            title="Export PNG"
          >
            <Download className="w-5 h-5" />
          </button>
        </div>
      </div>

      <div className="h-[calc(100%-60px)]">
        {isLoading ? (
          <div className="flex items-center justify-center h-full">
            <Loader2 className="w-8 h-8 text-blue-600 animate-spin" />
            <span className="ml-3 text-gray-600">Loading schema...</span>
          </div>
        ) : error ? (
          <div className="flex items-center justify-center h-full text-red-600">
            Failed to load schema. Please try again.
          </div>
        ) : (
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            nodeTypes={nodeTypes}
            fitView
            attributionPosition="bottom-left"
          >
            <Background />
            <Controls />
            <MiniMap
              nodeColor={(node) => {
                switch (node.type) {
                  case 'table':
                    return '#3b82f6'
                  default:
                    return '#94a3b8'
                }
              }}
            />
          </ReactFlow>
        )}
      </div>
    </div>
  )
}
