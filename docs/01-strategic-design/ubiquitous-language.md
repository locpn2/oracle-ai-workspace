# Ubiquitous Language - Phase 2: Strategic Design

## 1. Giới thiệu

Document này định nghĩa **Ubiquitous Language** (Ngôn ngữ chung) cho dự án Oracle AI Workspace. Mục tiêu là đảm bảo tất cả thành viên trong team (dev, BA, stakeholders) sử dụng cùng một ngôn ngữ khi nói về hệ thống.

> **Quan trọng:** Một số từ có ý nghĩa khác nhau tùy thuộc vào Bounded Context. Bảng dưới đây phân biệt rõ ràng.

---

## 2. Term Definitions by Context

### 2.1 Auth Context

| Term | Context | Definition |
|------|---------|------------|
| **User** | Auth | Người sử dụng hệ thống, có credentials để login |
| **Admin** | Auth | User có quyền quản trị, quản lý users khác |
| **Token** | Auth | JWT token được phát hành sau khi authenticate |
| **Credential** | Auth | Username/password dùng để xác thực |
| **Connection** | Auth | Oracle DB connection được tạo riêng cho mỗi user |
| **Session** | Auth | Khoảng thời gian user logged-in |

### 2.2 Schema Context

| Term | Context | Definition |
|------|---------|------------|
| **Schema** | Schema | Tập hợp tất cả metadata của Oracle DB (tables, columns, constraints) |
| **Table** | Schema | Bảng trong Oracle DB, có columns, primary key, foreign keys |
| **Column** | Schema | Cột của table, có name, data type, nullable |
| **Primary Key** | Schema | Cột(s) xác định duy nhất mỗi row trong table |
| **Foreign Key** | Schema | Ràng buộc tham chiếu từ table này đến table khác |
| **Constraint** | Schema | Ràng buộc (PK, FK, UNIQUE, CHECK, NOT NULL) |
| **Index** | Schema | Cấu trúc tăng tốc độc truy vấn |
| **ERD** | Schema | Entity-Relationship Diagram - biểu đồ trực quan hóa schema |
| **Metadata** | Schema | Thông tin cấu trúc (table names, column types, relationships) |

### 2.3 Chat Context

| Term | Context | Definition |
|------|---------|------------|
| **Query** | Chat | Câu hỏi bằng ngôn ngữ tự nhiên từ user |
| **SQL** | Chat | Structured Query Language - câu truy vấn được generate |
| **Text-to-SQL** | Chat | Process chuyển đổi câu hỏi → SQL |
| **Prompt** | Chat | Input được gửi cho AI LLM |
| **Schema Context** | Chat | Schema metadata được gắn vào prompt để AI hiểu DB structure |
| **Validation** | Chat | Kiểm tra SQL chỉ chứa SELECT (whitelist) |
| **Fallback** | Chat | Chain: Groq → Ollama → Gemini khi AI primary fail |
| **History** | Chat | Lịch sử chat trong một session |
| **Session** | Chat | Cuộc hội thoại liên tục, có unique ID |
| **Message** | Chat | Một câu hỏi hoặc câu trả lời trong chat |
| **Result** | Chat | Kết quả trả về sau khi execute SQL |

### 2.4 Vector Context

| Term | Context | Definition |
|------|---------|------------|
| **Embedding** | Vector | Vector số (768 dimensions) đại diện cho semantic content |
| **Vector** | Vector | Mảng số thực 768 chiều từ BGE-base model |
| **Document** | Vector | Text representation của một row (sau flattening) |
| **Flattening** | Vector | Process chuyển đổi row → text document |
| **Chunk** | Vector | Một phần của document (dùng cho long text) |
| **Batch** | Vector | Nhóm rows (1000 rows) được xử lý cùng lúc |
| **Index** | Vector | pgvector index (ivfflat) để tìm kiếm nhanh |
| **Similarity** | Vector | Độ tương đồng giữa vectors (cosine distance) |
| **Search** | Vector | Semantic search - tìm kiếm theo nghĩa, không phải keyword |
| **Vector Store** | Vector | PostgreSQL + pgvector nơi lưu trữ embeddings |
| **Job** | Vector | Embedding job - async task embed một table |

### 2.5 Infrastructure (Generic)

| Term | Context | Definition |
|------|---------|------------|
| **Oracle DB** | Infra | Source database - RDBMS chứa dữ liệu cần visualize/search |
| **PostgreSQL** | Infra | Vector store database - lưu embeddings |
| **pgvector** | Infra | PostgreSQL extension cho vector operations |
| **Ollama** | Infra | Local AI engine chạy trên máy (SQLCoder, BGE-base) |
| **Groq** | Infra | Cloud AI provider (llama-3.1-8b-instant) |
| **Gemini** | Infra | Google AI fallback provider |
| **D3.js** | Infra | JavaScript library vẽ ERD visualization |

---

## 3. Term Mapping - Same Word, Different Meaning

### 3.1 "Schema"

| Context | Ý nghĩa | Ví dụ |
|---------|---------|-------|
| **Schema Context** | Database structure (DDL) | "Extract schema từ Oracle" |
| **Vector Context** | Table metadata cache | "Schema JSON lưu trong vector store" |
| **Chat Context** | Phần của prompt chứa table/column names | "Gắn schema vào prompt" |

**Lý do tách:** Schema trong Schema Context là read-only metadata từ Oracle. Trong Vector Context, schema là cached metadata để quản lý embedding jobs. Trong Chat Context, schema là context text cho AI.

### 3.2 "Table"

| Context | Ý nghĩa | Ví dụ |
|---------|---------|-------|
| **Schema Context** | Oracle table với columns, PK, FK | "Danh sách tables trong DB" |
| **Chat Context** | Table được referenced trong SQL | "Query table EMPLOYEES" |
| **Vector Context** | Nguồn rows để embed | "Embed table EMPLOYEES" |

**Lý do tách:** Trong Schema Context, table là entity cần visualize. Trong Chat Context, table là target của SQL. Trong Vector Context, table là nguồn dữ liệu để flatten.

### 3.3 "Query"

| Context | Ý nghĩa | Ví dụ |
|---------|---------|-------|
| **Chat Context** | Câu hỏi tự nhiên từ user | "Tìm nhân viên có lương > 5000" |
| **Schema Context** | SQL metadata query | "Query ALL_TABLES" |
| **Vector Context** | Semantic search query | "Search: employee salary" |
| **Infra** | Database query execution | "Execute query trên Oracle" |

**Lý do tách:** Query trong Chat Context là natural language. Trong Schema Context, query là metadata extraction SQL. Trong Vector Context, query là semantic search input.

### 3.4 "Connection"

| Context | Ý nghĩa | Ví dụ |
|---------|---------|-------|
| **Auth Context** | Oracle connection per-user | "Tạo connection cho user A" |
| **Infra** | Database connection pool | "HikariCP connection pool" |

**Lý do tách:** Connection trong Auth Context là business concept (per-user isolation). Connection trong Infra là technical concept (pooling, timeout).

---

## 4. Domain-Specific Phrases

### 4.1 Schema Context Phrases

| Phrase | Meaning |
|--------|---------|
| "Extract schema" | Lấy metadata từ Oracle DB |
| "Get ERD" | Lấy JSON cho D3.js render |
| "List tables" | Lấy danh sách tất cả tables |
| "Get columns" | Lấy chi tiết columns của một table |
| "Map relationships" | Xác định FK giữa các tables |

### 4.2 Chat Context Phrases

| Phrase | Meaning |
|--------|---------|
| "Process query" | Xử lý câu hỏi tự nhiên |
| "Generate SQL" | Tạo SQL query từ AI |
| "Validate SQL" | Kiểm tra SQL (SELECT only, no injection) |
| "Execute query" | Chạy SQL trên Oracle |
| "Fallback chain" | Thứ tự AI fallback: Groq → Ollama → Gemini |

### 4.3 Vector Context Phrases

| Phrase | Meaning |
|--------|---------|
| "Embed table" | Tạo embeddings cho tất cả rows của table |
| "Flatten row" | Chuyển row thành text document |
| "Batch process" | Xử lý 1000 rows một lần |
| "Semantic search" | Tìm kiếm theo nghĩa (vector similarity) |
| "Cosine distance" | Measure of similarity giữa vectors |

---

## 5. Code Naming Conventions

### 5.1 Package Structure (Backend)

```
com.oracleai.workspace
├── schema/           # Schema Bounded Context
│   ├── domain/       # Entities, Value Objects
│   ├── repository/   # Data access
│   ├── service/      # Business logic
│   └── api/          # REST controllers
├── chat/             # Chat Bounded Context
├── vector/           # Vector Bounded Context
├── auth/             # Auth Bounded Context
└── shared/           # Shared kernel (exceptions, DTOs)
```

### 5.2 Naming Examples

| Concept | Class Name | Method Name |
|---------|-----------|-------------|
| Schema extraction | `SchemaExtractor` | `extractTables()` |
| ERD generation | `ERDGenerator` | `generateJSON()` |
| Text-to-SQL | `TextToSQLService` | `convertToSQL()` |
| SQL validation | `SQLValidator` | `validate()` |
| Flattening | `FlatteningService` | `flattenRow()` |
| Embedding | `EmbeddingService` | `generateEmbeddings()` |
| Vector search | `VectorSearchService` | `search()` |
| Authentication | `AuthService` | `authenticate()` |

---

## 6. API Endpoint Conventions

### 6.1 RESTful Patterns

| Pattern | URL | HTTP Method |
|---------|-----|-------------|
| List resources | `/api/schema/tables` | GET |
| Get single resource | `/api/schema/tables/{name}` | GET |
| Create resource | `/api/vector/embed-table` | POST |
| Search | `/api/vector/search` | GET |
| Authenticate | `/api/auth/login` | POST |

### 6.2 Response Format

```json
{
  "success": true,
  "data": { ... },
  "message": "Optional message"
}
```

---

## 7. Summary

**Nguyên tắc sử dụng:**

1. **Luôn chỉ định Context** khi sử dụng các term ambiguous (Schema, Table, Query, Connection)
2. **Sử dụng Domain-Specific Phrases** thay vì diễn đạt chung chung
3. **Tuân theo Naming Conventions** cho code và API
4. **Khi thắc mắc**, refer vào bảng này trước khi hỏi

**Mục đích:** Giảm hiểu nhầm giữa team members, đặc biệt khi discuss về cross-context features.
