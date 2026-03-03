# Oracle DB Visualization & RDBMS-to-Vector Converter

## 1. Project Overview

### 1.1 Mục tiêu cốt lõi

Xây dựng công cụ hỗ trợ người dùng:
- **Trích xuất Schema** từ Oracle DB để trực quan hóa (biểu đồ ERD)
- **Chuyển đổi dữ liệu** (Rows) sang Vector DB (PostgreSQL + pgvector)
- **Text-To-SQL**: Truy vấn dữ liệu bằng ngôn ngữ tự nhiên với AI

### 1.2 Phạm vi

| STT | Tính năng | Ưu tiên |
|-----|------------|---------|
| 1 | Schema Extraction (Table, Column, FK) | P0 |
| 2 | ERD Visualization (D3.js) | P0 |
| 3 | Text-to-SQL (AI Chat) | P0 |
| 4 | RDBMS-to-Vector (Flattening + Embedding) | P0 |
| 5 | Semantic Search | P1 |
| 6 | Authentication/Authorization | P1 |

---

## 2. Architecture Overview

### 2.1 System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              PRESENTATION LAYER                              │
│  ┌─────────────────────┐              ┌─────────────────────────────────┐ │
│  │   React + Vite      │              │         D3.js ERD              │ │
│  │   (Dashboard)       │              │      (Visualization)           │ │
│  └──────────┬──────────┘              └─────────────────────────────────┘ │
│             │                                                                   │
│             │ HTTP/WebSocket                                                   │
└─────────────┼───────────────────────────────────────────────────────────────┘
              │
┌─────────────┼───────────────────────────────────────────────────────────────┐
│             │                     API GATEWAY LAYER                           │
│             ▼                                                                 │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    Spring Boot 3.x + Spring AI                       │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │   Auth      │  │   Schema    │  │    Chat     │  │   Vector    │ │   │
│  │  │   Module    │  │   Module    │  │   Module    │  │   Module    │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────┬───────────────────────────────────────────────────────────────┘
              │
┌─────────────┼───────────────────────────────────────────────────────────────┐
│             │                       DATA LAYER                               │
│             ▼                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────────┐ │
│  │   Oracle DB     │  │  PostgreSQL +   │  │      Ollama (Local)        │ │
│  │   (Source)      │  │   pgvector      │  │  ┌─────────────────────┐  │ │
│  │                 │  │  (Vector Store) │  │  │  SQLCoder-7B        │  │ │
│  │                 │  │                 │  │  │  BGE-base           │  │ │
│  │                 │  │                 │  │  └─────────────────────┘  │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────────────────┘ │
└───────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Data Flow

```
┌──────────────┐     ┌─────────────────┐     ┌──────────────┐
│  Oracle DB   │────▶│   Metadata      │────▶│   Frontend   │
│   (Source)   │     │   Extractor     │     │   (D3.js)    │
└──────────────┘     └────────┬────────┘     └──────────────┘
                             │
                             ▼
                      ┌─────────────────┐
                      │   AI Engine     │
                      │   (Hybrid)      │
                      └────────┬────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        ▼                      ▼                      ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Text-to-SQL  │    │  Embedding   │    │   SQL       │
│   (Chat)     │    │  (Vectorize) │    │  Executor    │
└──────────────┘    └──────┬───────┘    └──────────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ PostgreSQL +   │
                 │   pgvector     │
                 └─────────────────┘
```

---

## 3. Tech Stack Chi Tiết

### 3.1 Backend

| Component | Technology | Version |
|-----------|------------|---------|
| Framework | Spring Boot | 3.3.x |
| AI Integration | Spring AI | 1.0.x |
| ORM | Spring Data JPA + MyBatis | - |
| Oracle Driver | ojdbc11 | 23.x |
| Security | Spring Security + JWT | - |
| Build Tool | Maven | 3.9.x |

### 3.2 Frontend

| Component | Technology | Version |
|-----------|------------|---------|
| Framework | React | 18.x |
| Build Tool | Vite | 5.x |
| Styling | Tailwind CSS | 3.x |
| Visualization | D3.js | 7.x |
| HTTP Client | Axios | - |
| State Management | React Query / Zustand | - |

### 3.3 Database

| Database | Purpose | Extension |
|----------|---------|-----------|
| Oracle DB | Source (RDBMS) | - |
| PostgreSQL 15 | Vector Store | pgvector |
| Redis | Session/Cache | - |

### 3.4 AI Engine (Hybrid)

| Provider | Model | Use Case | Free Limits |
|----------|-------|----------|-------------|
| **Groq** | llama-3.1-8b-instant | Primary LLM | 30 RPM, 500K TPD |
| **Ollama** | SQLCoder-7B | Local Text-to-SQL | Unlimited (local) |
| **Ollama** | BGE-base | Embedding | Unlimited (local) |
| **Google** | Gemini 2.0 | Fallback | Pay-as-you-go |

---

## 4. AI Engine Specification

### 4.1 Text-to-SQL Pipeline

```
User Question → Schema Context → Groq LLM → SQL Validation → Execute → Result
      │              │              │            │           │
      │              │              │            │           ▼
      │              │              │            │      Format Output
      │              │              │            │
      └──────────────┴──────────────┴────────────┘
                    Fallback Chain:
                    Groq → Ollama/SQLCoder → Gemini
```

### 4.2 Prompt Template

```sql
You are an expert SQL developer. Convert the question to Oracle SQL.

Database Schema:
{schema}

Tables:
{tables}

Question: {question}

Rules:
1. Use Oracle SQL syntax
2. Only SELECT queries (no INSERT/UPDATE/DELETE)
3. Use proper JOINs for multi-table queries
4. Include appropriate WHERE clauses
5. Use aggregate functions with GROUP BY when needed

Generate only the SQL query, no explanation.
```

### 4.3 Embedding Pipeline

```
Oracle Rows → Flattening Logic → Batch (1000 rows) → BGE-base (Ollama)
                                              │
                                              ▼
                                     pgvector Storage
                           Table: document_embeddings
                           Columns: id, table_name, row_data, embedding_vector
```

### 4.4 Flattening Logic

```text
Input: Table EMPLOYEES with columns (employee_id, name, salary, department_id)
Row: (101, 'John Doe', 5000, 10)

Output Document:
"Employee ID: 101, Name: John Doe, Salary: 5000, Department ID: 10"
```

### 4.5 Distance Metric

- **pgvector**: `cosine_distance` (L2-normalized vectors)
- **SQL Query**: `ORDER BY embedding_vector <=> embedding`

---

## 5. API Endpoints

### 5.1 Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login and get JWT |
| GET | `/api/auth/me` | Get current user info |

### 5.2 Schema

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/schema/tables` | List all tables |
| GET | `/api/schema/tables/{name}` | Get table details |
| GET | `/api/schema/columns/{table}` | Get columns of table |
| GET | `/api/schema/relationships` | Get FK relationships |
| GET | `/api/schema/erd` | Full ERD JSON for D3.js |

### 5.3 Chat (Text-to-SQL)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat/query` | Natural language to SQL |
| GET | `/api/chat/history` | Get chat history |
| GET | `/api/chat/history/{sessionId}` | Get session history |

### 5.4 Vector Store

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/vector/embed-table` | Embed entire table |
| POST | `/api/vector/embed-rows` | Embed specific rows |
| GET | `/api/vector/search` | Semantic search |
| GET | `/api/vector/status` | Embedding status |

---

## 6. Database Schema

### 6.1 Vector Store (PostgreSQL)

```sql
-- Document embeddings table
CREATE TABLE document_embeddings (
    id BIGSERIAL PRIMARY KEY,
    table_name VARCHAR(255) NOT NULL,
    row_id VARCHAR(255),
    document_text TEXT NOT NULL,
    embedding_vector VECTOR(768),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for cosine similarity
CREATE INDEX ON document_embeddings 
    USING ivfflat (embedding_vector cosine_ops)
    WITH (lists = 100);

-- Table metadata cache
CREATE TABLE table_metadata (
    id BIGSERIAL PRIMARY KEY,
    table_name VARCHAR(255) UNIQUE NOT NULL,
    schema_json JSONB,
    row_count BIGINT,
    last_synced TIMESTAMP
);
```

---

## 7. Environment Variables

### 7.1 Required Variables (.env)

```bash
# ===================
# APPLICATION
# ===================
APP_NAME=oracle-ai-workspace
APP_PORT=8080
SPRING_PROFILES_ACTIVE=dev

# ===================
# ORACLE DATABASE
# ===================
ORACLE_HOST=localhost
ORACLE_PORT=1521
ORACLE_SID=xe
ORACLE_USERNAME=system
ORACLE_PASSWORD=your_password

# ===================
# POSTGRESQL + VECTOR
# ===================
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=vector_store
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password

# ===================
# AI PROVIDERS
# ===================
# Groq (Primary LLM)
GROQ_API_KEY=your_groq_api_key

# Google Gemini (Fallback)
GEMINI_API_KEY=your_gemini_api_key

# Ollama (Local)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=sqlcoder:7b
OLLAMA_EMBEDDING_MODEL=bge-base

# ===================
# JWT SECURITY
# ===================
JWT_SECRET=your_256_bit_secret_key
JWT_EXPIRATION=86400000

# ===================
# OPTIONAL
# ===================
LOG_LEVEL=INFO
BATCH_SIZE=1000
```

---

## 8. Todo List

### Phase 1: Infrastructure & Setup

- [ ] Khởi tạo GitHub Repository
- [ ] Tạo docker-compose.yml với Oracle XE, PostgreSQL 15 + pgvector, Redis
- [ ] Thiết lập Spring Boot project với dependencies:
  - spring-ai-bom
  - spring-boot-starter-data-jpa
  - spring-boot-starter-security
  - ojdbc11
  - pgvector jdbc
- [ ] Cấu hình application.yml cho multi-datasource
- [ ] Tạo .env.example template
- [ ] Verify docker-compose up thành công

### Phase 2: Schema Extraction & Visualization

- [ ] Module trích xuất Metadata:
  - Query `ALL_TABLES`
  - Query `ALL_TAB_COLUMNS`
  - Query `ALL_CONSTRAINTS` (FK)
  - Query `ALL_INDEXES`
- [ ] API: GET `/api/schema/erd` trả về JSON cho D3.js
- [ ] Frontend: Tích hợp D3.js vẽ ERD
  - Force-directed graph
  - Zoom/Pan
  - Click to drill-down
  - Table node hiển thị columns
- [ ] Frontend: Dashboard layout với Tailwind CSS

### Phase 3: AI Integration (Text-to-SQL)

- [ ] Tích hợp Groq API với Spring AI
- [ ] Xây dựng Prompt Template cho Text-to-SQL
- [ ] Implement SQL Validation (chỉ SELECT, whitelist)
- [ ] Fallback chain: Groq → Ollama → Gemini
- [ ] API: POST `/api/chat/query`
- [ ] Frontend: Chat UI với message bubbles

### Phase 4: RDBMS to Vector

- [ ] Module Flattening: Chuyển row thành document
- [ ] Tích hợp BGE-base embedding qua Ollama
- [ ] Batch processing (1000 rows/batch)
- [ ] Lưu vector vào pgvector
- [ ] API: POST `/api/vector/embed-table`
- [ ] API: GET `/api/vector/search` với cosine similarity

### Phase 5: Security & Auth

- [ ] JWT Authentication
- [ ] User registration/login
- [ ] Password BCrypt hashing
- [ ] Role-based access control (Admin/User)
- [ ] Rate limiting trên AI endpoints

### Phase 6: Deployment

- [ ] Dockerfile cho Backend (multi-stage build)
- [ ] Dockerfile cho Frontend (nginx)
- [ ] docker-compose.yml production
- [ ] GitHub Actions CI/CD
  - Build & Test
  - Docker build & push
  - Deploy to server

---

## 9. Manual Verification

### 9.1 Infrastructure

```bash
# Start all services
docker-compose up -d

# Verify PostgreSQL
psql -h localhost -p 5432 -U postgres -c "SELECT 1;"

# Verify Oracle
docker exec -it oracle-db sqlplus system/password@//localhost:1521/XE

# Verify Ollama
curl http://localhost:11434/api/tags
```

### 9.2 Schema Extract API

```bash
# Start backend
./mvnw spring-boot:run

# Test schema API
curl -X GET http://localhost:8080/api/schema/tables \
  -H "Authorization: Bearer <token>"
```

Expected response:
```json
{
  "tables": [
    {
      "name": "EMPLOYEES",
      "columns": [...],
      "primaryKey": "EMPLOYEE_ID",
      "foreignKeys": [...]
    }
  ]
}
```

### 9.3 Frontend Dashboard

```bash
# Install dependencies
npm install

# Start development
npm run dev

# Access http://localhost:5173
# Verify D3.js renders ERD diagram
```

### 9.4 End-to-End Chat

```bash
# Test Text-to-SQL
curl -X POST http://localhost:8080/api/chat/query \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tìm tất cả nhân viên có lương cao hơn 5000"
  }'
```

Expected:
- SQL generated: `SELECT * FROM employees WHERE salary > 5000`
- Result displayed in frontend

### 9.5 Vector Embedding

```bash
# Embed a table
curl -X POST http://localhost:8080/api/vector/embed-table \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "tableName": "EMPLOYEES"
  }'

# Search
curl -X GET "http://localhost:8080/api/vector/search?query=employee+salary" \
  -H "Authorization: Bearer <token>"
```

---

## 10. Checklists

### 10.1 Security Checklist

- [ ] Thông tin kết nối DB lưu trong biến môi trường (.env)
- [ ] .env không được commit to git (thêm vào .gitignore)
- [ ] JWT token có expiration và refresh mechanism
- [ ] SQL injection prevention (whitelist keywords, validation)
- [ ] Rate limiting trên AI endpoints (Groq free tier protection)
- [ ] Password được hash với BCrypt
- [ ] CORS configuration cho frontend
- [ ] HTTPS in production

### 10.2 Performance Checklist

- [ ] Pagination khi trích xuất dữ liệu lớn (>100K rows)
- [ ] Batch processing (1000 rows/batch) cho embedding
- [ ] Connection pooling (HikariCP) cho Oracle và PostgreSQL
- [ ] Index trên vector columns (ivfflat)
- [ ] Cache schema metadata
- [ ] Async processing cho embedding jobs
- [ ] Streaming response cho large queries

### 10.3 Data Quality Checklist

- [ ] Handle NULL values trong flattening
- [ ] Handle special characters (escape/sanitize)
- [ ] Handle BLOB/CLOB columns (skip or convert to text)
- [ ] Handle composite keys
- [ ] Handle Oracle data types mapping
- [ ] Validation trước khi insert vector

### 10.4 Testing Checklist

- [ ] Unit tests cho Flattening logic
- [ ] Unit tests cho SQL generation
- [ ] Integration tests cho API endpoints
- [ ] E2E tests với Cypress/Playwright
- [ ] Load tests cho AI endpoints

---

## 11. Commit & Test Rule

### 11.1 Git Commit Convention

```
<type>(<scope>): <description>

Types:
- feat: New feature
- fix: Bug fix
- refactor: Code refactoring
- docs: Documentation
- chore: Build process, dependencies

Examples:
feat(schema): Add metadata extraction from Oracle
feat(ai): Integrate Groq API for Text-to-SQL
fix(vector): Handle NULL values in flattening
docs(api): Add API documentation
```

### 11.2 Test Before Commit

- [ ] Chạy unit tests: `./mvnw test`
- [ ] Chạy integration tests: `./mvnw verify`
- [ ] Không có compile errors
- [ ] Pass all linting (nếu có)
- [ ] Review code trước khi commit

### 11.3 Branching Strategy

```
main (production)
  └── develop (development)
        ├── feature/schema-extraction
        ├── feature/text-to-sql
        ├── feature/vector-embedding
        └── bugfix/fix-issues
```

---

## 12. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Groq rate limit | High | Fallback to Ollama/Gemini |
| Oracle connection timeout | Medium | Connection pooling, retry |
| Large data embedding | High | Batch processing, async |
| SQL injection | Critical | Whitelist validation |
| Out of memory | High | Pagination, streaming |

---

## 13. References

- [Spring AI Documentation](https://docs.spring.io/spring-ai/)
- [Ollama Documentation](https://github.com/ollama/ollama)
- [pgvector Documentation](https://github.com/pgvector/pgvector)
- [Groq API Documentation](https://console.groq.com/docs)
- [D3.js Documentation](https://d3js.org/)
- [Defog SQLCoder](https://github.com/defog-ai/sqlcoder)

---

**Version**: 1.0  
**Last Updated**: 2026-03-03  
**Author**: Solution Architect
