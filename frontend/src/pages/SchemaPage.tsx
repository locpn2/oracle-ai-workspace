import { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { schemaApi } from '../services/api';
import type { ERDResponse, TableDTO } from '../types';

export default function SchemaPage() {
  const svgRef = useRef<SVGSVGElement>(null);
  const [erdData, setErdData] = useState<ERDResponse | null>(null);
  const [tables, setTables] = useState<TableDTO[]>([]);
  const [selectedTable, setSelectedTable] = useState<TableDTO | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [viewMode, setViewMode] = useState<'erd' | 'tables'>('erd');

  useEffect(() => {
    loadSchema();
  }, []);

  const loadSchema = async () => {
    try {
      setLoading(true);
      const response = await schemaApi.getERD();
      if (response.data?.success && response.data.data) {
        setErdData(response.data.data);
        setTables(response.data.data.tables);
      }
    } catch (err) {
      setError('Failed to load schema');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (viewMode === 'erd' && erdData && svgRef.current) {
      renderERD(erdData);
    }
  }, [viewMode, erdData]);

  const renderERD = (data: ERDResponse) => {
    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();

    const width = 1200;
    const height = 800;
    svg.attr('viewBox', `0 0 ${width} ${height}`);

    const nodeMap = new Map<string, { x: number; y: number }>();
    const nodeWidth = 180;
    const nodeHeight = 120;
    const cols = Math.ceil(Math.sqrt(data.tables.length));
    
    data.tables.forEach((table, i) => {
      nodeMap.set(table.name, {
        x: (i % cols) * (nodeWidth + 80) + 50,
        y: Math.floor(i / cols) * (nodeHeight + 100) + 50,
      });
    });

    const relationships = svg.append('g').attr('class', 'relationships');
    data.relationships.forEach((rel) => {
      const from = nodeMap.get(rel.fromTable);
      const to = nodeMap.get(rel.toTable);
      if (from && to) {
        relationships
          .append('line')
          .attr('x1', from.x + nodeWidth / 2)
          .attr('y1', from.y + nodeHeight)
          .attr('x2', to.x + nodeWidth / 2)
          .attr('y2', to.y)
          .attr('stroke', '#94a3b8')
          .attr('stroke-width', 2)
          .attr('marker-end', 'url(#arrow)');
      }
    });

    svg
      .append('defs')
      .append('marker')
      .attr('id', 'arrow')
      .attr('viewBox', '0 -5 10 10')
      .attr('refX', 8)
      .attr('refY', 0)
      .attr('markerWidth', 6)
      .attr('markerHeight', 6)
      .attr('orient', 'auto')
      .append('path')
      .attr('d', 'M0,-5L10,0L0,5')
      .attr('fill', '#94a3b8');

    const nodes = svg.append('g').attr('class', 'nodes');
    data.tables.forEach((table) => {
      const pos = nodeMap.get(table.name)!;
      const g = nodes
        .append('g')
        .attr('transform', `translate(${pos.x}, ${pos.y})`)
        .style('cursor', 'pointer')
        .on('click', () => setSelectedTable(table));

      g.append('rect')
        .attr('width', nodeWidth)
        .attr('height', nodeHeight)
        .attr('rx', 8)
        .attr('fill', 'white')
        .attr('stroke', '#6366f1')
        .attr('stroke-width', 2);

      g.append('rect')
        .attr('width', nodeWidth)
        .attr('height', 28)
        .attr('rx', 8)
        .attr('fill', '#6366f1');

      g.append('text')
        .attr('x', nodeWidth / 2)
        .attr('y', 18)
        .attr('text-anchor', 'middle')
        .attr('fill', 'white')
        .attr('font-weight', 'bold')
        .attr('font-size', 12)
        .text(table.name.substring(0, 20));

      const columns = table.columns.slice(0, 4);
      columns.forEach((col, i) => {
        const icon = col.primaryKey ? '🔑' : col.foreignKey ? '🔗' : '📄';
        g.append('text')
          .attr('x', 8)
          .attr('y', 48 + i * 18)
          .attr('font-size', 11)
          .attr('fill', '#374151')
          .text(`${icon} ${col.name}`);
      });

      if (table.columns.length > 4) {
        g.append('text')
          .attr('x', 8)
          .attr('y', 48 + 4 * 18)
          .attr('font-size', 10)
          .attr('fill', '#6b7280')
          .text(`+ ${table.columns.length - 4} more`);
      }
    });
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-red-600">{error}</p>
        <button onClick={loadSchema} className="mt-4 px-4 py-2 bg-indigo-600 text-white rounded-md">
          Retry
        </button>
      </div>
    );
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-800">Schema / ERD</h1>
        <div className="flex space-x-2">
          <button
            onClick={() => setViewMode('erd')}
            className={`px-4 py-2 rounded-md ${
              viewMode === 'erd' ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-700'
            }`}
          >
            ERD Diagram
          </button>
          <button
            onClick={() => setViewMode('tables')}
            className={`px-4 py-2 rounded-md ${
              viewMode === 'tables' ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-700'
            }`}
          >
            Table List
          </button>
        </div>
      </div>

      {viewMode === 'erd' ? (
        <div className="bg-white rounded-lg shadow p-4 overflow-auto">
          <svg ref={svgRef} className="w-full h-auto" style={{ minHeight: 600 }}></svg>
          <p className="text-sm text-gray-500 mt-2">Click on a table to view details</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {tables.map((table) => (
            <div
              key={table.name}
              className="bg-white rounded-lg shadow p-4 cursor-pointer hover:shadow-md transition-shadow"
              onClick={() => setSelectedTable(table)}
            >
              <h3 className="font-semibold text-indigo-600 mb-2">{table.name}</h3>
              <p className="text-sm text-gray-500">{table.type}</p>
              <p className="text-sm text-gray-500">{table.columns.length} columns</p>
            </div>
          ))}
        </div>
      )}

      {selectedTable && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[80vh] overflow-auto">
            <div className="p-6">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h2 className="text-xl font-bold text-gray-800">{selectedTable.name}</h2>
                  <p className="text-sm text-gray-500">{selectedTable.type}</p>
                </div>
                <button
                  onClick={() => setSelectedTable(null)}
                  className="text-gray-400 hover:text-gray-600 text-2xl"
                >
                  ×
                </button>
              </div>
              <table className="w-full">
                <thead>
                  <tr className="bg-gray-50">
                    <th className="px-4 py-2 text-left text-sm font-semibold">Column</th>
                    <th className="px-4 py-2 text-left text-sm font-semibold">Type</th>
                    <th className="px-4 py-2 text-left text-sm font-semibold">Key</th>
                    <th className="px-4 py-2 text-left text-sm font-semibold">Nullable</th>
                  </tr>
                </thead>
                <tbody>
                  {selectedTable.columns.map((col) => (
                    <tr key={col.name} className="border-t">
                      <td className="px-4 py-2 text-sm">{col.name}</td>
                      <td className="px-4 py-2 text-sm text-gray-500">{col.dataType}</td>
                      <td className="px-4 py-2 text-sm">
                        {col.primaryKey && <span className="text-yellow-600">PK</span>}
                        {col.foreignKey && <span className="text-blue-600 ml-1">FK</span>}
                      </td>
                      <td className="px-4 py-2 text-sm">{col.nullable ? 'Yes' : 'No'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
