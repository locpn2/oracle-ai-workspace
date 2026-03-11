import axios from 'axios';
import type {
  ApiResponse,
  TableDTO,
  ERDResponse,
  QueryRequest,
  QueryResponse,
  SearchRequest,
  SearchResult,
  AuthResponse,
  LoginRequest,
  RegisterRequest,
  EmbedTableRequest,
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const schemaApi = {
  getTables: () => api.get<ApiResponse<TableDTO[]>>('/api/schema/tables'),
  getTable: (name: string) => api.get<ApiResponse<TableDTO>>(`/api/schema/tables/${name}`),
  getERD: () => api.get<ApiResponse<ERDResponse>>('/api/schema/erd'),
};

export const chatApi = {
  query: (data: QueryRequest) => api.post<ApiResponse<QueryResponse>>('/api/chat/query', data),
};

export const vectorApi = {
  embedTable: (data: EmbedTableRequest) => api.post<ApiResponse<{ jobId: string }>>('/api/vector/embed-table', data),
  search: (data: SearchRequest) => api.post<ApiResponse<SearchResult[]>>('/api/vector/search', data),
};

export const authApi = {
  login: (data: LoginRequest) => api.post<ApiResponse<AuthResponse>>('/api/auth/login', data),
  register: (data: RegisterRequest) => api.post<ApiResponse<AuthResponse>>('/api/auth/register', data),
};

export default api;
