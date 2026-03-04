# Event Storming - Phase 2: Strategic Design

## 1. Actors (Người tham gia)

| Actor | Mô tả | Quyền |
|-------|--------|--------|
| User | Người dùng cuối sử dụng hệ thống | Xem ERD, Chat, Search |
| Admin | Quản trị viản lý users, cên | Quấu hình hệ thống |
| System | Hệ thống tự động | Batch jobs, embedding tasks |

---

## 2. Domain Events (Sự kiện nghiệp vụ - Cam)

### 2.1 Schema Context Events

| Event | Mô tả | Trigger |
|-------|--------|---------|
| `SchemaExtracted` | Metadata (tables, columns, constraints) đã được trích xuất từ Oracle | User yêu cầu xem schema |
| `TablesListed` | Danh sách tables đã được trả về | Query ALL_TABLES thành công |
| `ColumnsRetrieved` | Thông tin columns của table đã được lấy | User xem chi tiết table |
| `RelationshipsMapped` | FK relationships đã được xác định | Query ALL_CONSTRAINTS thành công |
| `ERDGenerated` | ERD JSON đã sẵn sàng cho D3.js | Tất cả metadata đã load |

### 2.2 Chat Context Events

| Event | Mô tả | Trigger |
|-------|--------|---------|
| `QueryReceived` | Câu hỏi tiếng Việt/Anh đã nhận được | User gửi câu hỏi |
| `SchemaContextAttached` | Schema context đã được gắn vào prompt | AI cần context |
| `SQLGenerated` | SQL query đã được tạo từ AI | LLM trả về SQL |
| `SQLValidated` | SQL đã được kiểm tra (whitelist) | Validation thành công |
| `SQLExecuted` | SQL đã chạy trên Oracle | Query thành công |
| `ResultReturned` | Kết quả trả về cho user | Response gửi đi |
| `FallbackTriggered` | AI primary fail, chuyển sang fallback | Primary AI error |
| `HistorySaved` | Chat history đã được lưu | Session kết thúc |

### 2.3 Vector Context Events

| Event | Mô tả | Trigger |
|-------|--------|---------|
| `EmbeddingRequested` | Yêu cầu embed table/rows đã nhận | User chọn embed |
| `RowsFlattened` | Rows đã chuyển thành documents | Flattening xong |
| `BatchQueued` | Batch embedding đã được queue | Chia batch xong |
| `EmbeddingsGenerated` | Vectors đã được tạo | AI embedding xong |
| `EmbeddingsStored` | Vectors đã lưu vào pgvector | Insert thành công |
| `SearchQueryReceived` | Query tìm kiếm đã nhận | User search |
| `SimilarityCalculated` | Tính toán cosine similarity | Vector search xong |
| `SearchResultsReturned` | Kết quả search trả về | Response gửi đi |

### 2.4 Auth Context Events

| Event | Mô tả | Trigger |
|-------|--------|---------|
| `UserRegistered` | User mới đã đăng ký | POST /register |
| `UserAuthenticated` | User đã login thành công | POST /login |
| `TokenIssued` | JWT token đã được phát hành | Auth thành công |
| `TokenValidated` | Token đã được xác thực | Request có token |
| `ConnectionEstablished` | Oracle connection đã được tạo per-user | User authenticated |

---

## 3. Commands (Lệnh - Xanh)

### 3.1 Schema Context Commands

| Command | Mô tả | Handler |
|---------|--------|---------|
| `ExtractSchema` | Trích xuất toàn bộ schema | SchemaExtractor |
| `ListTables` | Lấy danh sách tables | TableRepository |
| `GetTableDetails` | Lấy chi tiết một table | TableService |
| `GetRelationships` | Lấy FK relationships | RelationshipService |
| `GenerateERD` | Tạo JSON cho D3.js | ERDGenerator |

### 3.2 Chat Context Commands

| Command | Mô tả | Handler |
|---------|--------|---------|
| `ProcessQuery` | Xử lý câu hỏi tự nhiên | QueryProcessor |
| `GenerateSQL` | Tạo SQL từ LLM | TextToSQLService |
| `ValidateSQL` | Kiểm tra SQL (SELECT only) | SQLValidator |
| `ExecuteQuery` | Chạy SQL trên Oracle | QueryExecutor |
| `FallbackToOllama` | Chuyển sang Ollama | OllamaClient |
| `FallbackToGemini` | Chuyển sang Gemini | GeminiClient |
| `SaveHistory` | Lưu chat history | ChatHistoryService |

### 3.3 Vector Context Commands

| Command | Mô tả | Handler |
|---------|--------|---------|
| `EmbedTable` | Embed toàn bộ table | EmbeddingService |
| `FlattenRows` | Chuyển rows thành text | FlatteningService |
| `GenerateEmbeddings` | Tạo vectors (BGE-base) | EmbeddingGenerator |
| `StoreEmbeddings` | Lưu vào pgvector | VectorRepository |
| `SemanticSearch` | Tìm kiếm vector | VectorSearchService |

### 3.4 Auth Context Commands

| Command | Mô tả | Handler |
|---------|--------|---------|
| `RegisterUser` | Đăng ký user mới | AuthService |
| `AuthenticateUser` | Xác thực user | AuthService |
| `IssueToken` | Phát hành JWT | JwtProvider |
| `ValidateToken` | Xác thực token | JwtFilter |
| `CreateUserConnection` | Tạo Oracle connection per-user | ConnectionPool |

---

## 4. Aggregates & Entities

### 4.1 Schema Aggregate

```
SchemaAggregate
├── Table (Entity)
│   ├── name: String
│   ├── columns: List<Column>
│   ├── primaryKey: List<String>
│   └── foreignKeys: List<ForeignKey>
├── Column (Value Object)
│   ├── name: String
│   ├── dataType: String
│   ├── nullable: Boolean
│   └── position: Integer
└── ForeignKey (Value Object)
    ├── sourceColumn: String
    ├── targetTable: String
    └── targetColumn: String
```

### 4.2 Chat Aggregate

```
ChatSession (Aggregate Root)
├── sessionId: UUID
├── userId: String
├── messages: List<ChatMessage>
│   ├── role: Enum (USER, ASSISTANT)
│   ├── content: String
│   ├── sql: String (optional)
│   └── timestamp: DateTime
└── createdAt: DateTime
```

### 4.3 Embedding Aggregate

```
EmbeddingJob (Aggregate Root)
├── jobId: UUID
├── tableName: String
├── status: Enum (PENDING, PROCESSING, COMPLETED, FAILED)
├── totalRows: Long
├── processedRows: Long
├── batches: List<EmbeddingBatch>
└── createdAt: DateTime
```

---

## 5. Process Flows

### 5.1 Text-to-SQL Flow

```
User: "Tìm nhân viên có lương > 5000"
    │
    ▼
[QueryReceived]
    │
    ▼
[SchemaContextAttached] ──► Schema Context: Get schema metadata
    │
    ▼
[SQLGenerated] ──► Groq API (llama-3.1-8b-instant)
    │
    ▼
[SQLValidated] ──► Whitelist: SELECT only
    │
    ├─── Success ──► [SQLExecuted] ──► Oracle DB
    │                      │
    │                      ▼
    │               [ResultReturned]
    │                      │
    ▼                      │
[FallbackTriggered] ◄──────┘
    │
    ▼
Ollama (SQLCoder-7B)
    │
    ▼
Fallback to Gemini
```

### 5.2 Embedding Flow

```
User: Select table "EMPLOYEES" to embed
    │
    ▼
[EmbeddingRequested]
    │
    ▼
[RowsFlattened] ──► Row: (101, 'John', 5000)
                    Doc: "Employee ID: 101, Name: John, Salary: 5000"
    │
    ▼
[BatchQueued] ──► 1000 rows per batch
    │
    ▼
[EmbeddingsGenerated] ──► Ollama (BGE-base)
    │
    ▼
[EmbeddingsStored] ──► PostgreSQL + pgvector
```

---

## 6. Ghi chú thảo luận

### Câu hỏi mở (Open Questions)

1. **Caching Strategy**: Schema metadata có nên cache không? TTL là bao lâu?
2. **Embedding Sync**: Khi Oracle DB thay đổi, vectors có tự động update không?
3. **Rate Limiting**: Giới hạn bao nhiêu queries/user cho AI endpoints?
4. **Session Management**: Chat sessions có expire không? Sau bao lâu?

### Giả định (Assumptions)

1. Oracle DB là read-only cho schema extraction
2. User connection sử dụng connection pooling per-user
3. Embedding là batch async, không blocking user request
4. SQL validation chỉ cho phép SELECT queries (whitelist)
