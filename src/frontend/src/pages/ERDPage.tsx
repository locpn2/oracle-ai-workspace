import { useState, useEffect, useRef } from 'react'
import { useQuery } from '@tanstack/react-query'
import * as d3 from 'd3'
import { connectionApi, schemaApi } from '../services/api'

interface ERDNode extends d3.SimulationNodeDatum {
  id: string
  label: string
  schema: string
  columns: number
  rowCount?: number
}

interface ERDLink extends d3.SimulationLinkDatum<ERDNode> {
  source: string | ERDNode
  target: string | ERDNode
  label: string
}

function ERDPage() {
  const svgRef = useRef<SVGSVGElement>(null)
  const [selectedConnection, setSelectedConnection] = useState<string>('')
  const [selectedSchema, setSelectedSchema] = useState<string>('')
  const [accessibilityMode, setAccessibilityMode] = useState(false)
  const [tableDetails, setTableDetails] = useState<any>(null)

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

  const { data: erdData, isLoading } = useQuery({
    queryKey: ['erd', selectedConnection, selectedSchema],
    queryFn: async () => {
      const response = await schemaApi.getERD(selectedConnection, selectedSchema)
      return response.data
    },
    enabled: !!selectedConnection,
  })

  useEffect(() => {
    if (!svgRef.current || !erdData) return

    const svg = d3.select(svgRef.current)
    svg.selectAll('*').remove()

    const width = svgRef.current.clientWidth
    const height = svgRef.current.clientHeight

    const nodes: ERDNode[] = erdData.tables.map((table: any) => ({
      id: `${table.schema_name}.${table.table_name}`,
      label: table.table_name,
      schema: table.schema_name,
      columns: table.columns.length,
      rowCount: table.row_count,
    }))

    const links: ERDLink[] = erdData.relationships.map((rel: any) => ({
      source: `${rel.from_schema}.${rel.from_table}`,
      target: `${rel.to_schema}.${rel.to_table}`,
      label: `${rel.from_columns?.join(', ')} → ${rel.to_columns?.join(', ')}`,
    }))

    const simulation = d3.forceSimulation(nodes)
      .force('link', d3.forceLink<ERDNode, ERDLink>(links).id((d) => d.id).distance(150))
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collision', d3.forceCollide().radius(80))

    const g = svg.append('g')

    svg.call(
      d3.zoom<SVGSVGElement, unknown>()
        .scaleExtent([0.1, 4])
        .on('zoom', (event) => g.attr('transform', event.transform))
    )

    const link = g.append('g')
      .selectAll('line')
      .data(links)
      .join('line')
      .attr('stroke', '#94a3b8')
      .attr('stroke-width', 2)
      .attr('marker-end', 'url(#arrowhead)')

    svg.append('defs')
      .append('marker')
      .attr('id', 'arrowhead')
      .attr('viewBox', '-0 -5 10 10')
      .attr('refX', 25)
      .attr('refY', 0)
      .attr('orient', 'auto')
      .attr('markerWidth', 6)
      .attr('markerHeight', 6)
      .append('path')
      .attr('d', 'M 0,-5 L 10,0 L 0,5')
      .attr('fill', '#94a3b8')

    const node = g.append('g')
      .selectAll<SVGGElement, ERDNode>('g')
      .data(nodes)
      .join('g')
      .attr('class', 'cursor-pointer')
      .call(d3.drag<SVGGElement, ERDNode>()
        .on('start', (event, d) => {
          if (!event.active) simulation.alphaTarget(0.3).restart()
          d.fx = d.x
          d.fy = d.y
        })
        .on('drag', (event, d) => {
          d.fx = event.x
          d.fy = event.y
        })
        .on('end', (event, d) => {
          if (!event.active) simulation.alphaTarget(0)
          d.fx = null
          d.fy = null
        })
      )
      .on('click', (_, d) => {
        const table = erdData.tables.find((t: any) => `${t.schema_name}.${t.table_name}` === d.id)
        setTableDetails(table)
      })

    node.append('rect')
      .attr('width', 160)
      .attr('height', (d) => 40 + d.columns * 20)
      .attr('x', -80)
      .attr('y', -20)
      .attr('rx', 8)
      .attr('fill', '#eff6ff')
      .attr('stroke', '#3b82f6')
      .attr('stroke-width', 2)

    node.append('text')
      .attr('text-anchor', 'middle')
      .attr('y', 0)
      .attr('font-weight', 'bold')
      .attr('font-size', '12px')
      .text((d) => d.label)

    node.append('text')
      .attr('text-anchor', 'middle')
      .attr('y', 12)
      .attr('font-size', '10px')
      .attr('fill', '#64748b')
      .text((d) => `${d.columns} columns`)

    simulation.on('tick', () => {
      link
        .attr('x1', (d: any) => d.source.x)
        .attr('y1', (d: any) => d.source.y)
        .attr('x2', (d: any) => d.target.x)
        .attr('y2', (d: any) => d.target.y)

      node.attr('transform', (d: any) => `translate(${d.x},${d.y})`)
    })

    return () => {
      simulation.stop()
    }
  }, [erdData])

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">ERD Visualization</h2>
          <p className="text-gray-500 mt-1">Trực quan hóa sơ đồ quan hệ dữ liệu (Accessible for all)</p>
        </div>
        <div className="flex items-center gap-4">
          <label className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={accessibilityMode}
              onChange={(e) => setAccessibilityMode(e.target.checked)}
              className="rounded"
            />
            <span className="text-sm">Chế độ hỗ trợ tiếp cận</span>
          </label>
        </div>
      </div>

      <div className="grid grid-cols-4 gap-6">
        <div className="col-span-1 space-y-4">
          <div className="bg-white rounded-lg shadow p-4">
            <h3 className="font-semibold mb-3">Chọn kết nối</h3>
            <select
              value={selectedConnection}
              onChange={(e) => {
                setSelectedConnection(e.target.value)
                setSelectedSchema('')
              }}
              className="w-full rounded-md border border-gray-300 p-2"
            >
              <option value="">-- Chọn kết nối --</option>
              {connections.map((c: any) => (
                <option key={c.id} value={c.id}>{c.name}</option>
              ))}
            </select>
          </div>

          {schemas.length > 0 && (
            <div className="bg-white rounded-lg shadow p-4">
              <h3 className="font-semibold mb-3">Chọn Schema</h3>
              <select
                value={selectedSchema}
                onChange={(e) => setSelectedSchema(e.target.value)}
                className="w-full rounded-md border border-gray-300 p-2"
              >
                <option value="">-- Tất cả schemas --</option>
                {schemas.map((s: string) => (
                  <option key={s} value={s}>{s}</option>
                ))}
              </select>
            </div>
          )}

          {accessibilityMode && erdData && (
            <div className="bg-white rounded-lg shadow p-4">
              <h3 className="font-semibold mb-3">Danh sách bảng (Accessibility)</h3>
              <div className="space-y-2 max-h-96 overflow-y-auto" role="list" aria-label="Danh sách bảng">
                {erdData.tables.map((table: any) => (
                  <button
                    key={`${table.schema_name}.${table.table_name}`}
                    onClick={() => setTableDetails(table)}
                    className="w-full text-left p-2 rounded hover:bg-gray-100 focus:outline-2 focus:outline-primary-500"
                    aria-label={`Bảng ${table.table_name} trong schema ${table.schema_name}`}
                  >
                    <div className="font-medium">{table.table_name}</div>
                    <div className="text-xs text-gray-500">{table.schema_name}</div>
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>

        <div className="col-span-3">
          <div className="bg-white rounded-lg shadow" style={{ height: '600px' }}>
            {isLoading ? (
              <div className="flex items-center justify-center h-full">
                <div className="text-gray-500">Đang tải ERD...</div>
              </div>
            ) : !selectedConnection ? (
              <div className="flex items-center justify-center h-full">
                <div className="text-center text-gray-500">
                  <p className="text-4xl mb-2">📊</p>
                  <p>Vui lòng chọn kết nối Oracle để xem ERD</p>
                </div>
              </div>
            ) : (
              <>
                <svg
                  ref={svgRef}
                  width="100%"
                  height="100%"
                  className="focus:outline-2 focus:outline-primary-500"
                  role="img"
                  aria-label="Sơ đồ ERD tương tác. Sử dụng Ctrl+Scroll để zoom, kéo để di chuyển."
                />
                <div className="absolute top-4 right-4 flex gap-2">
                  <button
                    onClick={() => {
                      const svg = d3.select(svgRef.current)
                      svg.transition().call(
                        (d3.zoom as any).transform,
                        d3.zoomIdentity
                      )
                    }}
                    className="px-3 py-1 bg-white rounded shadow text-sm"
                  >
                    Reset View
                  </button>
                </div>
              </>
            )}
          </div>
        </div>
      </div>

      {tableDetails && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[80vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-xl font-bold">{tableDetails.table_name}</h3>
                  <p className="text-gray-500 text-sm">{tableDetails.schema_name}</p>
                </div>
                <button
                  onClick={() => setTableDetails(null)}
                  className="text-gray-500 hover:text-gray-700"
                  aria-label="Đóng"
                >
                  ✕
                </button>
              </div>

              <div className="space-y-4">
                <div>
                  <h4 className="font-semibold mb-2">Cột dữ liệu</h4>
                  <table className="w-full text-sm" role="table" aria-label="Chi tiết cột">
                    <thead>
                      <tr className="bg-gray-50">
                        <th className="text-left p-2">Tên</th>
                        <th className="text-left p-2">Kiểu dữ liệu</th>
                        <th className="text-left p-2">Nullable</th>
                        <th className="text-left p-2">Default</th>
                      </tr>
                    </thead>
                    <tbody>
                      {tableDetails.columns.map((col: any, idx: number) => (
                        <tr key={idx} className="border-t">
                          <td className="p-2 font-medium">{col.name}</td>
                          <td className="p-2">{col.data_type}</td>
                          <td className="p-2">{col.nullable ? 'Yes' : 'No'}</td>
                          <td className="p-2 text-gray-500">{col.default_value || '-'}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                {tableDetails.primary_key && (
                  <div>
                    <h4 className="font-semibold mb-2">Primary Key</h4>
                    <p>{tableDetails.primary_key.columns.join(', ')}</p>
                  </div>
                )}

                {tableDetails.foreign_keys.length > 0 && (
                  <div>
                    <h4 className="font-semibold mb-2">Foreign Keys</h4>
                    <ul className="list-disc list-inside">
                      {tableDetails.foreign_keys.map((fk: any, idx: number) => (
                        <li key={idx}>
                          {fk.columns.join(', ')} → {fk.referenced_schema}.{fk.referenced_table}({fk.referenced_columns.join(', ')})
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default ERDPage
