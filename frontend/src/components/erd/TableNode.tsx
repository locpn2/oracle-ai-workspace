import { memo } from 'react'
import { Handle, Position } from '@xyflow/react'
import type { NodeProps } from '@xyflow/react'
import { ChevronDown, ChevronRight, Key } from 'lucide-react'
import { useState } from 'react'
import type { Table } from '@/types/schema'

interface TableNodeData {
  table: Table
}

function TableNodeComponent({ data }: NodeProps) {
  const [expanded, setExpanded] = useState(true)
  const tableData = (data as unknown as TableNodeData).table

  return (
    <div className="bg-white border-2 border-gray-300 rounded-lg shadow-lg min-w-[200px]">
      <div
        className="flex items-center justify-between px-3 py-2 bg-gray-100 rounded-t-lg cursor-pointer"
        onClick={() => setExpanded(!expanded)}
      >
        <div className="flex items-center gap-2">
          {expanded ? (
            <ChevronDown className="w-4 h-4 text-gray-500" />
          ) : (
            <ChevronRight className="w-4 h-4 text-gray-500" />
          )}
          <span className="font-semibold text-gray-900">{tableData.name}</span>
        </div>
        {tableData.rowCount !== undefined && (
          <span className="text-xs text-gray-500">{tableData.rowCount.toLocaleString()}</span>
        )}
      </div>

      {expanded && (
        <div className="p-2 border-t border-gray-200">
          {tableData.columns.slice(0, 5).map((column) => (
            <div
              key={column.name}
              className="flex items-center justify-between py-1 px-1 text-sm hover:bg-gray-50 rounded"
            >
              <div className="flex items-center gap-2">
                {column.isPrimaryKey && (
                  <Key className="w-3 h-3 text-yellow-500" />
                )}
                <span className="text-gray-700">{column.name}</span>
              </div>
              <span className="text-xs text-gray-400">{column.type}</span>
            </div>
          ))}
          {tableData.columns.length > 5 && (
            <div className="text-xs text-gray-400 py-1 px-1">
              +{tableData.columns.length - 5} more columns
            </div>
          )}
        </div>
      )}

      <Handle
        type="target"
        position={Position.Left}
        className="w-3 h-3 bg-blue-500"
      />
      <Handle
        type="source"
        position={Position.Right}
        className="w-3 h-3 bg-blue-500"
      />
    </div>
  )
}

export const TableNode = memo(TableNodeComponent)
