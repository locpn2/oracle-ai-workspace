# Oracle AI Data Vision - Specification Document

## 1. Project Overview

### Project Name
**OracleVision** - AI-Powered Oracle Database Visualization & Vectorization Platform

### Project Type
Full-stack web application with AI capabilities

### Core Functionality Summary
Một công cụ trực quan hóa dữ liệu Oracle DB với khả năng AI query (Text-to-SQL), mô hình hóa dữ liệu theo nhóm, và đặc biệt là chuyển đổi RDBMS sang Vector DB để tăng cường xử lý AI.

### Target Users
- Database administrators (DBAs)
- Data analysts
- Developers working with Oracle databases
- Business users who need to understand database structure
- AI/ML engineers needing vector representations of relational data

---

## 2. System Architecture

### High-Level Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (React + TypeScript)             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐ │
│  │   ERD    │  │  AI Chat │  │  Data    │  │  Vector Search   │ │
│  │  Viewer  │  │  Query   │  │  Model   │  │     Console      │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Backend API (FastAPI + Python)               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐ │
│  │ Oracle   │  │  AI/LLM  │  │ Embedding│  │    Vector DB    │ │
│  │  Driver  │  │  Router  │  │ Service  │  │    Manager      │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│ Oracle DB     │    │ Vector Store  │    │ LLM API       │
│ (Source)      │    │ (Chroma/PG)   │    │ (OpenAI/etc)  │
└───────────────┘    └───────────────┘    └───────────────┘
```

### Technology Stack
- **Frontend**: React 18 + TypeScript + TailwindCSS + D3.js (for ERD)
- **Backend**: FastAPI + Python 3.11+
- **Database Driver**: oracledb (python-oracledb)
- **Vector Store**: ChromaDB / pgvector (configurable)
- **LLM Integration**: OpenAI API, Anthropic Claude, or local LLM (Ollama)
- **Embedding**: OpenAI embeddings, sentence-transformers
- **ORM**: SQLAlchemy (for better DX)
- **Containerization**: Docker + Docker Compose

---

## 3. Functionality Specification

### 3.1 Module 1: Oracle DB Connection & Schema Explorer

#### Features
- **Connection Management**
  - Support multiple Oracle DB connections
  - Secure credential storage (encrypted)
  - Connection pooling for performance
  - Health check and reconnection logic

- **Schema Discovery**
  - Auto-discover all tables, views, sequences
  - Extract column definitions (types, constraints, defaults)
  - Identify primary keys, foreign keys, unique constraints
  - Extract indexes and their types
  - Parse PL/SQL package/procedure signatures

#### User Interactions
1. Add new Oracle connection via UI form
2. Test connection before saving
3. View list of schemas/owners
4. Select schema to explore
5. Browse tables list with search/filter

#### Data Handling
- Cache schema metadata in memory (refresh on demand)
- Support incremental schema updates
- Handle large schemas (1000+ tables)

#### Edge Cases
- Connection timeout handling
- Invalid credentials error
- Network interruption recovery
- Handle tables without primary keys
- Handle circular foreign key references

---

### 3.2 Module 2: ERD Visualization (Accessibility-First)

#### Features
- **Interactive ERD Diagram**
  - Auto-layout using force-directed graph (D3.js)
  - Zoom, pan, and fit-to-screen controls
  - Click table to expand column details
  - Highlight relationships on hover

- **Accessibility Features (for "blind" users)**
  - Full keyboard navigation (Tab, Enter, Arrow keys)
  - Screen reader compatible (ARIA labels)
  - High contrast mode toggle
  - Text-based alternative view (table list with relationships)
  - Audio descriptions for diagram elements (TTS)
  - Export to accessible HTML/SVG formats

- **Visual Elements**
  - Color-coded relationship types (1:1, 1:N, N:N)
  - Table icons based on type (table, view, materialized view)
  - Badge showing row count
  - Search highlighting

#### User Interactions
1. Click table node to show details panel
2. Drag to reposition tables
3. Double-click relationship line to see join conditions
4. Right-click context menu (hide table, focus, export)
5. Toggle accessibility modes

#### Data Handling
- Calculate optimal layout positions
- Lazy load relationships for performance
- Support partial schema visualization

#### Edge Cases
- Handle orphan tables (no relationships)
- Visualize self-referencing tables
- Handle very wide tables (many columns)
- Performance with 100+ tables

---

### 3.3 Module 3: AI Text-to-SQL Query

#### Features
- **Natural Language to SQL**
  - Convert Vietnamese/English questions to Oracle SQL
  - Support complex queries with JOINs, aggregations
  - Auto-detect required tables from schema
  - Generate optimized SQL with hints

- **AI Chat Interface**
  - Conversational query refinement
  - Query history with replay
  - Share query results
  - Save favorite queries

- **SQL Editor**
  - Syntax highlighting (Oracle SQL)
  - Auto-completion for table/column names
  - Query execution with results display
  - Explain plan visualization

#### User Interactions
1. Type question in natural language
2. Review generated SQL (editable)
3. Execute or modify SQL
4. View results in table/chart format
5. Ask follow-up questions

#### Data Handling
- Context window with schema context
- Rate limiting for API calls
- Query result caching
- Pagination for large results

#### Edge Cases
- Ambiguous queries (ask for clarification)
- Queries requiring table creation
- SQL injection prevention
- Timeout handling for long queries
- Empty result set handling

---

### 3.4 Module 4: Data Modeling by Groups

#### Features
- **Domain/Business Entity Grouping**
  - Create custom groups (e.g., "Sales", "HR", "Finance")
  - Drag-drop tables into groups
  - Define group relationships
  - Color-code groups for visual distinction

- **Domain Model Visualization**
  - Show only selected groups in ERD
  - Cross-group relationship highlighting
  - Group-level statistics (table count, row estimates)

- **Data Dictionary Generation**
  - Auto-generate documentation per group
  - Business description fields
  - Data quality metrics

#### User Interactions
1. Create new group with name/description
2. Select tables and assign to groups
3. Set group hierarchy (parent-child)
4. Toggle group visibility in ERD

#### Data Handling
- Persist grouping configuration
- Import/export grouping definitions
- Sync with version control

#### Edge Cases
- Table belonging to multiple groups
- Deleting groups with assigned tables
- Circular group hierarchy prevention

---

### 3.5 Module 5: RDBMS to Vector DB Conversion (Core Feature)

#### Features
- **Vectorization Engine**
  - Extract structured data from Oracle tables
  - Generate text embeddings for each record
  - Preserve relationships as metadata
  - Batch processing for large tables

- **Embedding Strategies**
  - Row-level embedding (each row = one vector)
  - Column-based embedding (for search)
  - Semantic summarization of related records
  - Custom embedding templates per table

- **Vector Storage**
  - ChromaDB (local, open-source)
  - pgvector (PostgreSQL extension)
  - Pinecone (cloud, optional)
  - Milvus (cloud, optional)

- **Sync Mechanism**
  - Incremental sync (only changed records)
  - Full re-sync option
  - Scheduled sync (cron job)
  - Real-time CDC (Change Data Capture) via Oracle triggers

#### User Interactions
1. Select tables to vectorize
2. Configure embedding strategy per table
3. Set primary key and text columns
4. Trigger initial vectorization
5. Monitor sync progress

#### Data Handling
- Chunking strategy for large text fields
- Embedding model selection (OpenAI, local)
- Vector dimension management
- Deduplication logic

#### Edge Cases
- Tables with BLOBs (skip or extract text)
- Tables with JSON/XML columns
- Unicode text handling
- Null value handling
- Vector store connection failures

---

## 4. API Specification

### Core Endpoints

#### Connection Management
```
POST   /api/v1/connections              - Create new connection
GET    /api/v1/connections              - List all connections
GET    /api/v1/connections/{id}         - Get connection details
PUT    /api/v1/connections/{id}         - Update connection
DELETE /api/v1/connections/{id}         - Delete connection
POST   /api/v1/connections/{id}/test    - Test connection
```

#### Schema Discovery
```
GET    /api/v1/connections/{id}/schemas           - List schemas
GET    /api/v1/connections/{id}/schemas/{name}/tables    - List tables
GET    /api/v1/connections/{id}/tables/{schema}/{table}   - Get table details
GET    /api/v1/connections/{id}/relationships             - Get all relationships
GET    /api/v1/connections/{id}/erd                      - Get ERD data (JSON)
```

#### AI Query
```
POST   /api/v1/ai/query                    - Text-to-SQL conversion
POST   /api/v1/ai/query/execute            - Execute generated SQL
GET    /api/v1/ai/query/history            - Query history
POST   /api/v1/ai/query/explain            - Explain SQL query
```

#### Data Groups
```
GET    /api/v1/groups                      - List all groups
POST   /api/v1/groups                      - Create group
PUT    /api/v1/groups/{id}                 - Update group
DELETE /api/v1/groups/{id}                - Delete group
POST   /api/v1/groups/{id}/tables         - Add tables to group
DELETE /api/v1/groups/{id}/tables/{table_id} - Remove table from group
```

#### Vectorization
```
GET    /api/v1/vector/collections         - List vector collections
POST   /api/v1/vector/collections         - Create collection
POST   /api/v1/vector/sync                - Trigger sync
GET    /api/v1/vector/sync/status         - Get sync status
POST   /api/v1/vector/search               - Semantic search
POST   /api/v1/vector/query               - Query with filters
```

---

## 5. Database Schema (Internal Storage)

### Connections Table
```sql
CREATE TABLE connections (
    id UUID PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    host VARCHAR(255) NOT NULL,
    port INTEGER DEFAULT 1521,
    service_name VARCHAR(100),
    sid VARCHAR(100),
    username VARCHAR(100) NOT NULL,
    password_encrypted TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Groups Table
```sql
CREATE TABLE data_groups (
    id UUID PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    color VARCHAR(7) DEFAULT '#3B82F6',
    parent_id UUID REFERENCES data_groups(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Group Tables Junction
```sql
CREATE TABLE group_tables (
    group_id UUID REFERENCES data_groups(id) ON DELETE CASCADE,
    connection_id UUID REFERENCES connections(id) ON DELETE CASCADE,
    schema_name VARCHAR(100) NOT NULL,
    table_name VARCHAR(100) NOT NULL,
    PRIMARY KEY (group_id, connection_id, schema_name, table_name)
);
```

### Vector Collections Table
```sql
CREATE TABLE vector_collections (
    id UUID PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    connection_id UUID REFERENCES connections(id) ON DELETE CASCADE,
    source_table VARCHAR(100) NOT NULL,
    source_schema VARCHAR(100) NOT NULL,
    embedding_model VARCHAR(100) DEFAULT 'text-embedding-3-small',
    vector_dimension INTEGER,
    status VARCHAR(50) DEFAULT 'idle',
    last_sync_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 6. Security Considerations

- Encrypted storage for database credentials (Fernet encryption)
- API authentication via JWT tokens
- Role-based access control (RBAC)
- SQL injection prevention in query execution
- Rate limiting on AI endpoints
- Audit logging for all operations
- Secure WebSocket connections for real-time updates

---

## 7. Acceptance Criteria

### Connection Management
- [ ] Can add Oracle connection with all supported auth methods
- [ ] Connection test provides clear success/failure feedback
- [ ] Connections persist across sessions

### ERD Visualization
- [ ] ERD renders within 3 seconds for schemas with 50+ tables
- [ ] All accessibility features work with screen readers
- [ ] Zoom/pan is smooth and responsive
- [ ] Table details panel shows all column information

### AI Query
- [ ] Can generate SQL from natural language questions
- [ ] Generated SQL executes correctly against Oracle DB
- [ ] Query history is maintained and searchable

### Data Grouping
- [ ] Can create, edit, delete groups
- [ ] Tables can be assigned to multiple groups
- [ ] Group filtering works in ERD view

### Vector Conversion
- [ ] Can configure and trigger vectorization
- [ ] Incremental sync detects changes correctly
- [ ] Semantic search returns relevant results
- [ ] Vector store can be queried with filters

---

## 8. Project Structure

```
oracle-ai-workspace/
├── SPEC.md
├── README.md
├── docs/
│   ├── requirement.md
│   └── api-spec.md
├── src/
│   ├── backend/
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py                 # FastAPI app entry
│   │   │   ├── config.py               # Configuration
│   │   │   ├── api/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── v1/
│   │   │   │   │   ├── connections.py
│   │   │   │   │   ├── schemas.py
│   │   │   │   │   ├── ai_query.py
│   │   │   │   │   ├── groups.py
│   │   │   │   │   └── vector.py
│   │   │   ├── core/
│   │   │   │   ├── security.py
│   │   │   │   └── exceptions.py
│   │   │   ├── models/
│   │   │   │   ├── database.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── orm.py
│   │   │   └── services/
│   │   │       ├── oracle_client.py
│   │   │       ├── ai_service.py
│   │   │       ├── embedding_service.py
│   │   │       └── vector_service.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   └── frontend/
│       ├── src/
│       │   ├── App.tsx
│       │   ├── main.tsx
│       │   ├── components/
│       │   │   ├── ERDViewer/
│       │   │   ├── AIQuery/
│       │   │   ├── DataGroups/
│       │   │   └── VectorSearch/
│       │   ├── pages/
│       │   └── services/
│       ├── package.json
│       └── Dockerfile
├── docker-compose.yml
└── .env.example
```

---

## 9. Implementation Phases

### Phase 1: Foundation
- Project setup with Docker
- Oracle DB connection layer
- Basic schema discovery API
- Internal database setup

### Phase 2: Core Visualization
- ERD backend API
- React frontend with ERD viewer
- Accessibility features implementation

### Phase 3: AI Integration
- LLM integration for Text-to-SQL
- AI chat interface
- SQL execution and results display

### Phase 4: Data Grouping
- Group management CRUD
- Group assignment UI
- Group filtering in ERD

### Phase 5: Vector Conversion
- Embedding service implementation
- Vector store integration
- Sync mechanism
- Semantic search API

### Phase 6: Polish & Deploy
- Performance optimization
- Security hardening
- Documentation
- Deployment automation
