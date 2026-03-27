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
│  │  │              LLM Router (LangChain)                    │ ││
│  │  │    OpenAI │ Claude │ Ollama │ Azure OpenAI           │ ││
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
| `/api/v1/query/text-to-sql` | POST | Convert NL to SQL |
| `/api/v1/query/execute` | POST | Execute SQL query |
| `/api/v1/query/history` | GET | Query history |
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
| LLM provider final selection | Open | Flexible router built-in |
| Oracle connection pooling strategy | Open | Default SQLAlchemy pool |
| Vector embedding model | Open | Use OpenAI text-embedding-3 |
| Query result pagination size | Open | 100 rows default |

---

## 11. Success Criteria

### 11.1 MVP Definition

- [ ] User can login and view ERD
- [ ] User can query with natural language
- [ ] Generated SQL executes successfully
- [ ] Results display correctly
- [ ] Basic schema grouping works

### 11.2 Go-Live Criteria

- [ ] All P0 acceptance criteria met
- [ ] Security audit passed
- [ ] Performance benchmarks met
- [ ] Documentation complete
- [ ] Runbooks created

---

*Document Version: 1.0*
*Created: 2026-03-26*
*Status: Draft*
