# SPEC.md - Oracle AI Data Visualizer

## 1. Project Overview
- **Project Name**: Oracle AI Data Visualizer
- **Version**: 1.0.0
- **Description**: Công cụ trực quan hóa Oracle Database với AI-powered query và RDBMS-to-Vector sync
- **Target Users**: Business users, Data Analysts, Developers, DBAs

---

## 2. Functional Requirements

### 2.1 Database Connection
| ID | Requirement | Priority | Use Case |
|----|-------------|----------|----------|
| FR01 | Kết nối Oracle DB qua JDBC với connection string | P0 | UC01 |
| FR02 | Quản lý connection pool (HikariCP) | P0 | UC01 |
| FR03 | Lưu trữ connection config an toàn (encrypted) | P0 | UC01 |
| FR04 | Kiểm tra kết nối trước khi thao tác | P0 | UC01 |

### 2.2 Schema Extraction & ERD Visualization
| ID | Requirement | Priority | Use Case |
|----|-------------|----------|----------|
| FR05 | Extract tất cả tables từ schema | P0 | UC01 |
| FR06 | Extract columns, data types, constraints | P0 | UC01 |
| FR07 | Extract primary keys và foreign keys | P0 | UC01 |
| FR08 | Extract indexes | P1 | UC01 |
| FR09 | Render interactive ERD diagram | P0 | UC01 |
| FR10 | Zoom, pan, fit-to-screen cho diagram | P0 | UC01 |
| FR11 | Tìm kiếm tables trong diagram | P0 | UC01 |
| FR12 | Click table hiển thị chi tiết columns | P0 | UC01 |
| FR13 | Export ERD as PNG/SVG | P2 | UC07 |

### 2.3 AI-Powered Query (Text-to-SQL)
| ID | Requirement | Priority | Use Case |
|----|-------------|----------|----------|
| FR14 | Gửi natural language query tới Ollama | P0 | UC02 |
| FR15 | Inject schema context vào prompt | P0 | UC02 |
| FR16 | Validate generated SQL trước execute | P0 | UC02 |
| FR17 | Execute SQL query và return results | P0 | UC02 |
| FR18 | Format results as JSON/Table | P0 | UC02 |
| FR19 | Hiển thị generated SQL cho user review | P0 | UC02 |
| FR20 | Handle query timeout và errors | P0 | UC02 |

### 2.4 Data Grouping/Modeling
| ID | Requirement | Priority | Use Case |
|----|-------------|----------|----------|
| FR21 | Tạo/sửa/xóa data groups | P1 | UC03 |
| FR22 | Assign tables vào groups | P1 | UC03 |
| FR23 | Auto-suggest groups từ table naming patterns | P2 | UC03 |
| FR24 | Hiển thị groups trong navigation sidebar | P1 | UC03 |
| FR25 | Lưu group metadata vào local database | P1 | UC03 |

### 2.5 RDBMS to Vector DB Sync
| ID | Requirement | Priority | Use Case |
|----|-------------|----------|----------|
| FR26 | Select tables để sync | P0 | UC04 |
| FR27 | Configure columns cho text representation | P0 | UC04 |
| FR28 | Full sync: extract all data và embed | P0 | UC04 |
| FR29 | Incremental sync: detect changes và update | P0 | UC04 |
| FR30 | Generate embeddings với Ollama | P0 | UC04 |
| FR31 | Store vectors vào ChromaDB | P0 | UC04 |
| FR32 | Track sync progress và status | P0 | UC04 |
| FR33 | Semantic search API | P1 | UC05 |
| FR34 | Delete/regenerate vectors | P1 | UC04 |

### 2.6 User Management
| ID | Requirement | Priority | Use Case |
|----|-------------|----------|----------|
| FR35 | Đăng ký/đăng nhập local users | P0 | UC06 |
| FR36 | Role-based access (Admin/User/Viewer) | P1 | UC06 |
| FR37 | Session management với JWT | P0 | UC06 |

---

## 3. Non-Functional Requirements

### 3.1 Performance
| Category | Requirement | Target |
|----------|-------------|--------|
| Performance | ERD render với 200 tables | < 3 seconds |
| Performance | Text-to-SQL response time | < 10 seconds |
| Performance | Vector sync 1000 records | < 30 seconds |
| Performance | Initial page load | < 2 seconds |
| Performance | Database metadata extraction | < 5 seconds |

### 3.2 Security
| Category | Requirement | Target |
|----------|-------------|--------|
| Security | Encrypted database password storage | AES-256 |
| Security | HTTPS/TLS for all connections | Required |
| Security | JWT token authentication | HS256 |
| Security | Role-based authorization | 3 roles |
| Security | SQL injection prevention | Parameterized queries |

### 3.3 Scalability
| Category | Requirement | Target |
|----------|-------------|--------|
| Scalability | Concurrent users | 10+ |
| Scalability | Support database up to | 500 tables |

### 3.4 Reliability
| Category | Requirement | Target |
|----------|-------------|--------|
| Availability | Uptime | 99.5% |
| Error Handling | Graceful degradation | Yes |
| Logging | Full request logging | Yes |

---

## 4. Use Cases

### UC01: View Database Schema
**Actor**: Business User, Data Analyst
**Pre-condition**: User đã đăng nhập, đã có valid DB connection
**Flow**:
1. User clicks "Connect to Database"
2. User nhập connection details (host, port, service, username, password)
3. System validates connection
4. System extracts metadata (tables, columns, relationships)
5. System renders ERD diagram
6. User có thể zoom, pan, search, click để xem chi tiết
**Post-condition**: ERD diagram hiển thị, user có thể tương tác

### UC02: Query Data with Natural Language
**Actor**: Business User, Data Analyst
**Pre-condition**: User đã đăng nhập, đã connect to DB
**Flow**:
1. User nhập câu hỏi bằng ngôn ngữ tự nhiên
2. System gửi câu hỏi + schema context tới Ollama
3. Ollama generates SQL query
4. System validates SQL (syntax check)
5. System displays generated SQL cho user review
6. User confirms hoặc edits SQL
7. System executes SQL và returns results
8. Results displayed as table
**Post-condition**: User nhận được data results

### UC03: Organize Data into Groups
**Actor**: Data Analyst, DBA
**Pre-condition**: User đã đăng nhập, đã extract schema
**Flow**:
1. User clicks "Data Groups" tab
2. User creates new group (e.g., "Sales", "HR", "Finance")
3. User assigns tables vào group
4. System saves group metadata
5. Groups displayed in sidebar navigation
**Post-condition**: Tables organized into groups

### UC04: Sync to Vector Database
**Actor**: Developer, DBA
**Pre-condition**: User đã đăng nhập, đã connect to DB
**Flow**:
1. User clicks "Vector Sync" tab
2. User selects tables để sync
3. User configures which columns dùng để generate text
4. User clicks "Start Full Sync" hoặc "Start Incremental Sync"
5. System extracts data, generates embeddings
6. System stores vectors vào ChromaDB
7. Progress displayed in real-time
8. Completion notification
**Post-condition**: Data available in ChromaDB for semantic search

### UC05: Semantic Search
**Actor**: Developer
**Pre-condition**: Data đã sync vào ChromaDB
**Flow**:
1. Developer gửi search query via API
2. System generates embedding từ query
3. System searches ChromaDB for similar vectors
4. Results returned với similarity scores
**Post-condition**: Developer nhận kết quả tìm kiếm

### UC06: User Authentication
**Actor**: All users
**Flow**:
1. User registers với username/password
2. User đăng nhập
3. System returns JWT token
4. Token stored in localStorage
5. Subsequent requests include token
**Post-condition**: User authenticated, authorized

---

## 5. Acceptance Criteria

### AC01: Database Connection
- [ ] User có thể nhập và lưu Oracle connection details
- [ ] System validates connection trước khi save
- [ ] Connection thành công hiển thị success message
- [ ] Connection thất bại hiển thị error message rõ ràng

### AC02: ERD Visualization
- [ ] Tất cả tables hiển thị trong diagram
- [ ] Foreign key relationships shown as lines
- [ ] User có thể zoom in/out với mouse wheel
- [ ] User có thể pan bằng drag
- [ ] Click on table hiển thị popup với columns
- [ ] Search box lọc tables theo tên

### AC03: AI Query
- [ ] User nhập "Show me all users created this month"
- [ ] System generates valid SQL
- [ ] SQL displayed cho user review
- [ ] User click execute và nhận results
- [ ] Invalid SQL hiển thị error message

### AC04: Data Grouping
- [ ] User tạo group mới với tên
- [ ] User thêm tables vào group
- [ ] Groups hiển thị trong sidebar
- [ ] Click group lọc ERD chỉ hiển thị tables trong group

### AC05: Vector Sync
- [ ] User select tables từ checkbox list
- [ ] User click Start Sync
- [ ] Progress bar hiển thị sync progress
- [ ] Completion hiển thị success message
- [ ] Incremental sync chỉ sync changed records

### AC06: Semantic Search
- [ ] API endpoint /api/vector/search hoạt động
- [ ] Query returns relevant results với scores

### AC07: Authentication
- [ ] User đăng ký với username/password
- [ ] User đăng nhập và nhận JWT
- [ ] Unauthorized requests return 401

---

## 6. Technical Architecture

### 6.1 Tech Stack
| Component | Technology | Version |
|-----------|------------|---------|
| Backend | Spring Boot | 3.4.x |
| Language | Java | 21 |
| Oracle Driver | ojdbc11 | 23.x |
| Connection Pool | HikariCP | Included |
| AI Framework | LangChain4j | 0.31.x |
| LLM | Ollama (Llama 3.1) | Latest |
| Embeddings | mxbai-embed-large | Latest |
| Vector DB | ChromaDB | Latest |
| Local DB | H2 Database | 2.x |
| Auth | Spring Security + JWT | Included |
| Frontend | React + TypeScript | 18.x |
| UI Library | Material UI | 5.x |
| Diagram | ReactFlow | 11.x |
| Build | Maven | 3.9.x |
| Container | Docker | Latest |

### 6.2 Project Structure (DDD)
```
oracle-ai-visualizer/
├── src/main/java/com/oracleai/
│   ├── domain/
│   │   ├── entity/          # Table, Column, Relationship, User, Group
│   │   ├── valueobject/     # ConnectionConfig, EmbeddingConfig
│   │   ├── repository/     # Repository interfaces
│   │   └── service/        # Domain services
│   ├── application/
│   │   ├── dto/            # Request/Response DTOs
│   │   ├── usecase/        # Use case implementations
│   │   └── service/        # Application services
│   ├── infrastructure/
│   │   ├── oracle/         # JDBC connections, schema extraction
│   │   ├── ollama/         # LLM client, embeddings
│   │   ├── chroma/         # Vector store client
│   │   ├── security/       # JWT, authentication
│   │   └── persistence/    # H2 repositories
│   └── api/
│       └── controller/     # REST controllers
├── src/main/resources/
│   ├── application.yml
│   └── static/             # React build
├── src/frontend/           # React application
├── docker-compose.yml
└── pom.xml
```

### 6.3 API Endpoints

#### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/register | Register new user |
| POST | /api/auth/login | Login, returns JWT |

#### Schema
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/connections | Save connection |
| GET | /api/connections | List connections |
| GET | /api/schema/tables | Get all tables |
| GET | /api/schema/tables/{name} | Get table details |
| GET | /api/schema/relationships | Get FK relationships |
| GET | /api/schema/export | Export as PlantUML |

#### AI Query
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/ai/query | Generate SQL from natural language |
| POST | /api/ai/execute | Execute SQL query |

#### Groups
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/groups | List all groups |
| POST | /api/groups | Create group |
| PUT | /api/groups/{id} | Update group |
| DELETE | /api/groups/{id} | Delete group |
| POST | /api/groups/{id}/tables | Add tables to group |

#### Vector Sync
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/vector/sync | Start sync (full/incremental) |
| GET | /api/vector/status | Get sync status |
| GET | /api/vector/search | Semantic search |
| DELETE | /api/vector/collections/{table} | Delete collection |

---

## 7. Configuration

### 7.1 Environment Variables
```env
# Oracle Database
ORACLE_HOST=localhost
ORACLE_PORT=1521
ORACLE_SERVICE=ORCL
ORACLE_USERNAME=your_user
ORACLE_PASSWORD=your_password

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1
OLLAMA_EMBED_MODEL=mxbai-embed-large

# ChromaDB
CHROMA_HOST=localhost
CHROMA_PORT=8000

# App
JWT_SECRET=your-256-bit-secret-key
JWT_EXPIRATION=86400000
SERVER_PORT=8080
```

### 7.2 Docker Compose Services
- **oracle-db**: Oracle Database 23c Free
- **chroma**: ChromaDB vector database
- **ollama**: Ollama LLM service
- **app**: Spring Boot application
- **frontend**: React application (nginx)
