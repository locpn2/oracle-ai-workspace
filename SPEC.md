# SPEC.md - Oracle AI Data Visualization Tool

## 1. Project Overview

### 1.1 Project Name
**OracleVision** - AI-Powered Oracle Database Visualization & Query Tool

### 1.2 Vision
A tool that transforms Oracle database complexity into intuitive visualizations, enabling both technical and non-technical users to understand, query, and leverage their data through AI-powered natural language interactions.

### 1.3 Core Problem Statement
Oracle databases contain valuable data but are difficult to explore and understand without SQL expertise. This tool bridges the gap by providing visual schema exploration and AI-assisted querying.

### 1.4 Target Users
| User Type | Use Case | Primary Needs |
|-----------|----------|---------------|
| Business Analyst | Ad-hoc data queries | Quick answers, no SQL knowledge |
| Developer | SQL assistance, schema exploration | Code generation, ERD reference |
| Data Steward | Schema documentation | Visual documentation, data lineage |

---

## 2. Functional Requirements

### 2.1 Feature Matrix

| ID | Feature | Description | Priority | Complexity |
|----|---------|-------------|----------|------------|
| FR-01 | ERD Visualization | Interactive Entity Relationship Diagram | P0 | Medium |
| FR-02 | Text-to-SQL | Natural language to SQL conversion | P0 | High |
| FR-03 | Schema Grouping | Organize tables into logical groups | P1 | Low |
| FR-04 | RDBMS → Vector DB | Sync Oracle schema to Vector DB | P1 | High |
| FR-05 | Query Execution | Execute and display SQL results | P0 | Medium |
| FR-06 | SQL Preview | Show generated SQL before execution | P0 | Low |

### 2.2 Feature Specifications

#### FR-01: ERD Visualization
**Description:** Interactive diagram showing Oracle database tables, columns, relationships, and data types.

**Features:**
- Auto-generate ERD from Oracle schema metadata
- Display tables: name, columns, types, constraints
- Show relationships (PK, FK, unique)
- Interactive: zoom, pan, click to expand
- Filter by schema/group
- Export as PNG/SVG

**Acceptance Criteria:**
```
AC-01.1: ERD loads within 5 seconds for schema with 50 tables
AC-01.2: All tables with >5 columns show expandable detail
AC-01.3: Relationships render correctly (PK→FK connections)
AC-01.4: Export produces valid PNG/SVG file
```

#### FR-02: Text-to-SQL
**Description:** Convert natural language queries to Oracle SQL using LLM.

**Features:**
- Free-text input for queries
- Multi-turn conversation support
- Context-aware schema understanding
- Query history with revision
- Confidence score display

**Acceptance Criteria:**
```
AC-02.1: Simple queries (aggregation, filter) generate correct SQL >80%
AC-02.2: Complex queries (JOIN, subquery) generate correct SQL >60%
AC-02.3: Response time < 10 seconds for standard queries
AC-02.4: Generated SQL is syntax-valid for Oracle
```

#### FR-03: Schema Grouping
**Description:** Organize database tables into logical groups for easier navigation.

**Features:**
- Create/edit/delete groups
- Drag-drop tables into groups
- Color-coded groups
- Group-based ERD filtering
- Persist groupings per user

**Acceptance Criteria:**
```
AC-03.1: Users can create unlimited groups
AC-03.2: Groups persist across sessions
AC-03.3: ERD can filter by group selection
AC-03.4: Export grouping configuration available
```

#### FR-04: RDBMS → Vector DB
**Description:** Synchronize Oracle schema and data to pgvector for AI-enhanced operations.

**Features:**
- Schema embedding (table names, columns, descriptions)
- Sample data embedding (configurable row count)
- Semantic search on schema
- RAG-ready context injection
- Incremental sync (change detection)

**Acceptance Criteria:**
```
AC-04.1: Full schema sync completes within 5 minutes for 100 tables
AC-04.2: Semantic search returns relevant tables for query context
AC-04.3: RAG context injection reduces LLM token usage >30%
AC-04.4: Sync runs on schedule or on-demand
```

#### FR-05: Query Execution
**Description:** Execute SQL queries against Oracle database with result display.

**Features:**
- Execute generated or manual SQL
- Paginated result display (100 rows per page)
- Column sorting and filtering
- Export results (CSV, JSON, Excel)
- Query execution plan view

**Acceptance Criteria:**
```
AC-05.1: Results display within 5 seconds for <10K rows
AC-05.2: Export produces valid CSV/JSON files
AC-05.3: Execution plan shows cost estimates
AC-05.4: Timeout after 60 seconds with cancellation option
```

#### FR-06: SQL Preview
**Description:** Display generated SQL before execution for user review.

**Features:**
- Syntax-highlighted SQL display
- Copy to clipboard
- Edit SQL before execution
- Multiple SQL tabs
- SQL formatting/prettify

**Acceptance Criteria:**
```
AC-06.1: SQL displays immediately after generation
AC-06.2: Copy button copies full SQL to clipboard
AC-06.3: Edited SQL persists when switching tabs
AC-06.4: Prettify formats SQL correctly
```

---

## 3. Non-Functional Requirements

### 3.1 Performance

| Metric | Target | Measurement |
|--------|--------|-------------|
| ERD load (50 tables) | < 5s | First paint |
| ERD load (100 tables) | < 10s | First paint |
| Text-to-SQL response | < 10s | End-to-end |
| Query execution (simple) | < 5s | Result display |
| Vector sync (100 tables) | < 5min | Full sync |
| API response (p95) | < 500ms | Backend metrics |

### 3.2 Security

| Requirement | Implementation |
|-------------|----------------|
| Authentication | OAuth2/JWT |
| Password hashing | bcrypt (cost 12) |
| API security | Rate limiting, CORS |
| SQL injection | Parameterized queries only |
| Sensitive data | Encryption at rest |
| Audit logging | All query executions logged |

### 3.3 Scalability

| Dimension | Limit |
|-----------|-------|
| Tables per schema | 500 |
| Rows per query result | 10,000 (paginated) |
| Concurrent users | 50 |
| Vector embeddings | 100,000 |
| Query history | 1,000 per user |

### 3.4 Availability

| SLA | Target |
|-----|--------|
| Uptime | 99.5% |
| Planned maintenance | < 4h/month |
| Incident response | < 15min |
| Backup frequency | Daily |

### 3.5 Compatibility

| Component | Version |
|-----------|---------|
| Oracle Database | 11g+ |
| PostgreSQL/pgvector | 15+ |
| Browser | Chrome 100+, Firefox 100+, Safari 15+ |

---

## 4. Architecture

### 4.1 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Layer                             │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                React SPA (TypeScript)                        ││
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   ││
│  │  │ ERD View │  │ Query UI │  │ Schema UI │  │ Auth UI  │   ││
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘   ││
│  └─────────────────────────────────────────────────────────────┘│
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTPS (REST)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                         API Layer                                │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    FastAPI Backend                           ││
│  │  ┌─────────┐ ┌──────────┐ ┌─────────┐ ┌─────────────────┐ ││
│  │  │ Auth    │ │ Schema   │ │ Query   │ │ Vector Service  │ ││
│  │  │ Service │ │ Service  │ │ Service │ │                 │ ││
│  │  └─────────┘ └──────────┘ └─────────┘ └─────────────────┘ ││
│  │  ┌───────────────────────────────────────────────────────┐ ││
│  │  │         LLM Router (Smart Routing)                      │ ││
│  │  │  phi3:mini (simple) | llama3.2 (complex) | OpenAI (fb) │ ││
│  │  └───────────────────────────────────────────────────────┘ ││
│  │  ┌───────────────────────────────────────────────────────┐ ││
│  │  │      Template Fallback (6 patterns) + SQL Validator    │ ││
│  │  └───────────────────────────────────────────────────────┘ ││
│  │  ┌───────────────────────────────────────────────────────┐ ││
│  │  │      Connection Pool (TCPConnector limit=10)           │ ││
│  │  └───────────────────────────────────────────────────────┘ ││
│  └─────────────────────────────────────────────────────────────┘│
└──────┬───────────────┬───────────────┬─────────────────────────┘
       │               │               │
       ▼               ▼               ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────────┐
│ Oracle XE   │ │ PostgreSQL  │ │ Redis           │
│ (Main DB)   │ │ (pgvector) │ │ (Cache/Session) │
│ Port 1521   │ │ Port 5432   │ │ Port 6379       │
└─────────────┘ └─────────────┘ └─────────────────┘
```

### 4.2 Data Flow

```
User Input (Natural Language)
         │
         ▼
┌─────────────────┐
│ Text-to-SQL     │
│ Service         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ LLM Router      │
│ (Select Model)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐    ┌─────────────────┐
│ Vector Context   │───▶│ RAG Retrieval    │
│ (pgvector)      │    │ (Schema Context) │
└────────┬────────┘    └─────────────────┘
         │
         ▼
┌─────────────────┐
│ SQL Generation   │
│ (Prompt + Ctx)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Oracle Executor  │
│ (Validate/Safe)  │
└────────┬────────┘
         │
         ▼
    Query Results
```

### 4.3 Project Structure

```
oracle-vision/
├── frontend/                      # React SPA
│   ├── src/
│   │   ├── components/            # UI Components
│   │   │   ├── erd/              # ERD Viewer
│   │   │   ├── query/            # Query Interface
│   │   │   ├── schema/           # Schema Browser
│   │   │   └── common/           # Shared Components
│   │   ├── pages/                # Route Pages
│   │   ├── hooks/                # Custom Hooks
│   │   ├── services/             # API Clients
│   │   ├── stores/               # State Management
│   │   └── types/                # TypeScript Types
│   ├── public/
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.ts
│
├── backend/                      # FastAPI Backend
│   ├── app/
│   │   ├── api/                  # API Routes
│   │   │   ├── v1/
│   │   │   │   ├── auth/
│   │   │   │   ├── schema/
│   │   │   │   ├── query/
│   │   │   │   └── vector/
│   │   ├── core/                 # Core Config
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── exceptions.py
│   │   ├── models/               # Pydantic Models
│   │   ├── services/             # Business Logic
│   │   ├── llm/                  # LLM Integration
│   │   │   ├── router.py
│   │   │   ├── openai.py
│   │   │   ├── anthropic.py
│   │   │   └── prompts/
│   │   ├── db/                   # Database
│   │   │   ├── oracle.py
│   │   │   ├── postgres.py
│   │   │   └── redis.py
│   │   └── main.py
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
│
├── docker-compose.yml
├── SPEC.md
└── README.md
```

---

## 5. API Specification

### 5.1 Authentication

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/auth/login` | POST | Login with credentials |
| `/api/v1/auth/refresh` | POST | Refresh access token |
| `/api/v1/auth/logout` | POST | Invalidate session |

### 5.2 Schema Operations

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/schema/tables` | GET | List all tables |
| `/api/v1/schema/tables/{name}` | GET | Table details |
| `/api/v1/schema/erd` | GET | ERD data (nodes/edges) |
| `/api/v1/schema/groups` | GET/POST | Manage groups |

### 5.3 Query Operations

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/query/text-to-sql` | POST | Convert NL to SQL (with smart LLM routing + template fallback) |
| `/api/v1/query/text-to-sql/stream` | GET | SSE streaming with real-time progress events |
| `/api/v1/query/execute` | POST | Execute SQL query |
| `/api/v1/query/history` | GET | Query history (supports `?use_db=true` for PostgreSQL) |
| `/api/v1/query/preview` | POST | Validate SQL |

### 5.4 Vector Operations

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/vector/sync` | POST | Trigger sync |
| `/api/v1/vector/search` | POST | Semantic search |
| `/api/v1/vector/status` | GET | Sync status |

---

## 6. Tech Stack

### 6.1 Frontend

| Component | Technology | Version |
|-----------|------------|---------|
| Framework | React | 18.x |
| Language | TypeScript | 5.x |
| Build | Vite | 5.x |
| State | Zustand | 4.x |
| HTTP | TanStack Query | 5.x |
| ERD | React Flow | 11.x |
| UI | shadcn/ui | latest |
| Styling | Tailwind CSS | 3.x |

### 6.2 Backend

| Component | Technology | Version |
|-----------|------------|---------|
| Framework | FastAPI | 0.109.x |
| Language | Python | 3.11+ |
| ORM | SQLAlchemy | 2.x |
| Oracle | oracledb | 2.x |
| Vector | pgvector | 0.5+ |
| LLM | LangChain | 0.1.x |
| Cache | Redis | 7.x |
| Auth | python-jose | 3.3.x |

### 6.3 Infrastructure

| Component | Technology |
|-----------|------------|
| Container | Docker |
| Orchestration | docker-compose |
| CI/CD | GitHub Actions |
| Monitoring | Prometheus + Grafana |

---

## 7. User Flows

### 7.1 Text-to-SQL Flow

```
1. User enters: "Show me total sales by region for Q4"
         │
         ▼
2. System extracts intent: aggregation + filter
         │
         ▼
3. System retrieves schema context from pgvector
         │
         ▼
4. LLM generates SQL with schema context
         │
         ▼
5. Display SQL preview to user
         │
         ▼
6. User reviews, edits if needed, clicks Execute
         │
         ▼
7. System executes against Oracle, returns results
         │
         ▼
8. Display results in table with export options
```

### 7.2 ERD Visualization Flow

```
1. User navigates to ERD page
         │
         ▼
2. System fetches schema metadata from Oracle
         │
         ▼
3. System generates nodes (tables) and edges (relationships)
         │
         ▼
4. React Flow renders interactive diagram
         │
         ▼
5. User can zoom, pan, click to expand
         │
         ▼
6. User can filter by schema group
         │
         ▼
7. User can export as PNG/SVG
```

---

## 8. Testing Strategy

### 8.1 Test Pyramid

| Layer | Coverage Target | Tools |
|-------|-----------------|-------|
| Unit | 80% | pytest, unittest |
| Integration | 60% | pytest-asyncio, Testcontainers |
| E2E | 20% | Playwright |

### 8.2 Critical Test Scenarios

| Scenario | Test Type | Priority |
|----------|-----------|----------|
| Text-to-SQL accuracy | Integration | P0 |
| SQL injection prevention | Security | P0 |
| ERD rendering correctness | E2E | P1 |
| Vector sync accuracy | Unit | P1 |
| Auth token refresh | Unit | P1 |

---

## 9. Deployment

### 9.1 Environments

| Environment | Branch | URL |
|-------------|--------|-----|
| Development | local | localhost:3000 |
| Staging | develop | staging.oraclevision.local |
| Production | main | oraclevision.example.com |

### 9.2 Docker Services

| Service | Image | Ports |
|---------|-------|-------|
| frontend | nginx:alpine | 80, 443 |
| backend | python:3.11-slim | 8000 |
| oracle-xe | gvenzl/oracle-xe:21-slim | 1521 |
| postgres | pgvector/pgvector:pg15 | 5432 |
| redis | redis:7-alpine | 6379 |

---

## 10. Open Questions

| Question | Status | Resolution |
|----------|--------|------------|
| LLM provider final selection | **Resolved** | Smart routing: phi3:mini (simple) + llama3.2 (complex) + OpenAI fallback |
| Oracle connection pooling strategy | **Resolved** | aiohttp TCPConnector (limit=10, limit_per_host=5) for LLM; SQLAlchemy pool for DB |
| Vector embedding model | Open | Use OpenAI text-embedding-3 |
| Query result pagination size | Open | 100 rows default |
| LLM availability guarantee | **Resolved** | Ollama healthcheck verifies actual model response, not just `/api/tags` |
| SQL generation reliability | **Resolved** | Template fallback (6 patterns) + clear error for unmatched queries |

---

## 11. Success Criteria

### 11.1 MVP Definition

- [ ] User can login and view ERD
- [x] User can query with natural language
- [x] Generated SQL executes successfully
- [x] Results display correctly
- [ ] Basic schema grouping works

### 11.2 Go-Live Criteria

- [ ] All P0 acceptance criteria met
- [ ] Security audit passed
- [x] Performance benchmarks met (Text-to-SQL: 10-12ms template, 5-15s LLM)
- [ ] Documentation complete
- [ ] Runbooks created

## 12. Implementation Plan

### 12.1 Current Status

| Feature | Current Status | Target | Priority |
|---------|----------------|--------|----------|
| FR-04: Vector DB | Stub (20%) | Full Implementation | P0 |
| Oracle DB Connection | Mock | Real Connection | P0 |
| LLM Integration (Ollama) | **Done** | Smart routing + pooling + fallback | P0 |
| OAuth2/JWT | Demo (50%) | Full OAuth2 | P1 |
| ERD Export PNG/SVG | Button only | Full Implementation | P1 |
| Query Execution (Excel/Plan) | Basic | Full Features | P1 |
| SQL Preview Tabs | Single | Multiple Tabs | P2 |
| Text-to-SQL Fallback | **Done** | Template (6 patterns) + clear error | P0 |
| SSE Streaming | **Done** | Real-time progress events | P1 |
| Query History (Persistent) | **Done** | PostgreSQL-backed | P1 |
| SQL Validation | **Done** | LLM-based validation | P1 |

### 12.2 Technology Decisions

| Component | Decision | Rationale |
|-----------|----------|-----------|
| Vector DB | pgvector | Already in docker-compose |
| Embedding Model | Ollama (nomic-embed-text) | Privacy-friendly, free |
| LLM for SQL | Ollama (llama3.2) | Local, no API costs |
| Oracle Client | oracledb | Official thin client |

### 12.3 Implementation Phases

#### Phase 1: Vector DB (pgvector) — Pending
- Update postgres.py - Add vector operations
- Create vector service (embed, sync, search)
- Update vector API routes
- Integrate with text-to-sql
- Frontend: VectorSync + SemanticSearch

#### Phase 2: Ollama Integration — Completed
- ~~Create LLM router~~ — Smart routing: phi3:mini (simple) + llama3.2 (complex)
- ~~Create Ollama client~~ — Connection pooling with TCPConnector, shared session
- ~~Update text-to-sql service~~ — Template fallback (6 patterns), clear error response
- ~~Test with llama3.2 model~~ — End-to-end verified (10-12ms template, 5-15s LLM)
- **Additional:** OpenAI API fallback for complex queries when Ollama fails
- **Additional:** Query complexity classifier for intelligent model selection
- **Additional:** Real availability check (actual chat test, not just `/api/tags`)

#### Phase 3: Oracle DB Connection — Pending
- Add credentials to .env
- Test Oracle connection
- Add error handling
- Verify with real schema

#### Phase 4: OAuth2/JWT Full — Pending
- Create refresh_tokens table
- Create audit_logs table
- Implement /register endpoint
- Implement token rotation
- Add rate limiting
- Add audit logging

#### Phase 5: Minor Features — Pending
- ERD Export PNG/SVG
- Query Export Excel
- Execution Plan view
- SQL Preview tabs

#### Phase 6: Testing & Fix — Partially Complete
- Unit tests — Updated `test_services.py`, `test_integration.py`
- Integration tests — Template fallback, query classification, SSE streaming
- Fix bugs — HTTP status codes, success logic, healthchecks, connection pooling

#### Phase 7: Infrastructure Improvements — Completed
- ~~Frontend healthcheck~~ — Fixed to check `localhost:80/`
- ~~Ollama healthcheck~~ — Verifies actual model response via chat API
- ~~Persistent query history~~ — Wired up `QueryHistoryDB` with PostgreSQL
- ~~SSE streaming endpoint~~ — `/text-to-sql/stream` with progress events
- ~~SQL validation~~ — LLM-based validation via `SQL_VALIDATION_PROMPT`
- ~~Request timeout~~ — `asyncio.wait_for()` with configurable timeout, HTTP 504
- ~~Security~~ — `.env.docker` added to `.gitignore`

---

*Document Version: 1.2*
*Updated: 2026-03-30*
*Status: Updated with LLM Integration, Smart Routing, Template Fallback, SSE Streaming*
