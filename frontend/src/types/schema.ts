export interface Table {
  name: string
  db_schema: string
  columns: Column[]
  primaryKeys: string[]
  foreignKeys: ForeignKey[]
  rowCount?: number
}

export interface Column {
  name: string
  type: string
  nullable: boolean
  defaultValue?: string
  isPrimaryKey: boolean
}

export interface ForeignKey {
  column: string
  referencedTable: string
  referencedColumn: string
}

export interface ERDNode {
  id: string
  type: 'table'
  position: { x: number; y: number }
  data: {
    table: Table
  }
}

export interface ERDEdge {
  id: string
  source: string
  target: string
  label?: string
  type: 'primary' | 'foreign'
}

export interface SchemaGroup {
  id: string
  name: string
  color: string
  tableNames: string[]
}
