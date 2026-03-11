export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  message?: string;
}

export interface TableDTO {
  name: string;
  type: string;
  columns: ColumnDTO[];
}

export interface ColumnDTO {
  name: string;
  dataType: string;
  nullable: boolean;
  primaryKey: boolean;
  foreignKey?: {
    table: string;
    column: string;
  };
}

export interface ERDResponse {
  tables: TableDTO[];
  relationships: Relationship[];
}

export interface Relationship {
  fromTable: string;
  fromColumn: string;
  toTable: string;
  toColumn: string;
  type: 'one-to-one' | 'one-to-many' | 'many-to-many';
}

export interface QueryRequest {
  question: string;
  sessionId?: string;
}

export interface QueryResponse {
  sql: string;
  result?: unknown[];
  message?: string;
  sessionId: string;
}

export interface SearchRequest {
  query: string;
  tableName?: string;
  limit?: number;
}

export interface SearchResult {
  tableName: string;
  columnName: string;
  rowData: Record<string, unknown>;
  score: number;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface AuthResponse {
  token: string;
  user: {
    id: string;
    username: string;
    email: string;
  };
}

export interface EmbedTableRequest {
  tableName: string;
  batchSize?: number;
}
