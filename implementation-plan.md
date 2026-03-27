# Implementation Plan - OracleVision

**Created**: 2026-03-27  
**Version**: 1.0  
**Status**: Active

---

## Overview

This document details the implementation plan for OracleVision based on SPEC.md requirements. The project is currently at ~60-65% completion with several key features requiring full implementation.

---

## Phase 1: Vector DB (pgvector) - Est: 2-3 days

### Objectives
- Implement full pgvector integration for schema embedding
- Enable semantic search for schema context retrieval
- Integrate with text-to-sql for RAG-based query generation

### Backend Tasks

#### 1.1 Update postgres.py
**File**: `backend/app/db/postgres.py`

```python
# Add vector operations:
- init_vector_extension()
- create_embedding_table()
- insert_schema_embedding()
- semantic_search()
- get_all_embeddings()
- delete_embeddings()
```

#### 1.2 Create Vector Service
**New File**: `backend/app/services/vector.py`

```python
class VectorService:
    - embed_text(text: str) -> List[float]           # Generate embedding
    - embed_table_info(table: Table) -> dict         # Embed table metadata
    - embed_column_info(column: Column) -> dict     # Embed column metadata
    - sync_full_schema() -> SyncResult               # Full schema sync
    - sync_table(table_name: str) -> bool            # Single table sync
    - semantic_search(query: str, top_k: int) -> List[SearchResult]
    - get_sync_status() -> SyncStatus
    - delete_all_embeddings() -> bool
```

#### 1.3 Update Vector API Routes
**File**: `backend/app/api/v1/vector/__init__.py`

```python
# Current: Stub endpoints
# Target: Full implementation

@router.post("/sync")
async def trigger_sync():
    """Trigger full schema sync to pgvector"""
    # Implementation needed

@router.get("/status")
async def get_sync_status():
    """Get current sync status"""
    # Implementation needed

@router.post("/search")
async def search_schemas(query: str, top_k: int = 5):
    """Semantic search on schema"""
    # Implementation needed

@router.delete("/clear")
async def clear_embeddings():
    """Clear all embeddings"""
    # Implementation needed
```

### Frontend Tasks

#### 1.4 VectorSync Component
**New File**: `frontend/src/components/vector/VectorSync.tsx`

```typescript
// Features:
// - Display sync status (last sync, tables synced, errors)
// - Manual sync trigger button
// - Auto-sync toggle
// - Progress indicator during sync
```

#### 1.5 Semantic Search Component
**New File**: `frontend/src/components/vector/SemanticSearch.tsx`

```typescript
// Features:
// - Search input
// - Results display with relevance scores
// - Click to navigate to table
```

### Database (Already Created)
**File**: `init.sql`

```sql
-- Already exists:
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE schema_embeddings (...)
CREATE INDEX idx_schema_embeddings ...
```

---

## Phase 2: Ollama LLM Integration - Est: 2-3 days

### Objectives
- Implement Ollama client for local LLM inference
- Replace mock text-to-sql with real LLM generation
- Use Ollama for embeddings (nomic-embed-text)

### Backend Tasks

#### 2.1 Create LLM Router
**New File**: `backend/app/llm/router.py`

```python
class LLMProvider:
    """Route between different LLM providers"""
    
    def __init__(self, provider: str = "ollama"):
        self.provider = provider
    
    async def generate(self, prompt: str) -> str:
        """Generate text from prompt"""
        if self.provider == "ollama":
            return await ollama_client.generate(prompt)
        elif self.provider == "openai":
            return await openai_client.generate(prompt)
        # etc.
    
    async def embed(self, text: str) -> List[float]:
        """Generate embeddings"""
        if self.provider == "ollama":
            return await ollama_client.embed(text)
        # etc.

# Configuration in config.py:
# - default_llm_provider: "ollama"
# - ollama_base_url: "http://localhost:11434"
# - ollama_model: "llama3.2"
# - ollama_embed_model: "nomic-embed-text"
```

#### 2.2 Create Ollama Client
**New File**: `backend/app/llm/ollama.py`

```python
class OllamaClient:
    """Ollama API client"""
    
    def __init__(self, base_url: str, model: str, embed_model: str):
        self.base_url = base_url
        self.model = model
        self.embed_model = embed_model
    
    async def generate(self, prompt: str, **options) -> str:
        """Call /api/generate endpoint"""
        # Implementation with aiohttp
        
    async def embed(self, text: str) -> List[float]:
        """Call /api/embeddings endpoint"""
        # Implementation with aiohttp
        
    async def chat(self, messages: List[ChatMessage]) -> ChatResponse:
        """Call /api/chat endpoint"""
        # Implementation with aiohttp
        
    async def list_models() -> List[str]:
        """List available models"""
        # Call /api/tags
```

#### 2.3 Update text_to_sql Service
**File**: `backend/app/services/text_to_sql.py`

```python
# Current: Mock template-based generation
# Target: Real LLM generation with schema context

async def convert_text_to_sql(natural_language: str, context: str = None):
    # 1. Get schema context from vector DB (semantic search)
    # 2. Build prompt with schema context
    # 3. Call LLM (Ollama)
    # 4. Parse and validate SQL
    # 5. Return with confidence score
```

#### 2.4 Create SQL Generation Prompts
**File**: `backend/app/llm/prompts/text_to_sql.py`

```python
SYSTEM_PROMPT = """You are an expert Oracle SQL developer.
Given a natural language query and database schema, generate accurate Oracle SQL.
Rules:
- Use Oracle syntax (ROWNUM for pagination, not LIMIT)
- Use SYSDATE for current date
- Use proper JOIN syntax
- Always use table aliases when needed
- Return only the SQL query, no explanation
"""

USER_PROMPT = """Schema:
{schema_context}

Query: {natural_language}

Generate Oracle SQL:"""
```

### Frontend Tasks

#### 2.5 Update Query Page
- Add loading indicator during LLM generation
- Show model being used
- Handle streaming responses (optional)

---

## Phase 3: Oracle DB Connection - Est: 1-2 days

### Objectives
- Enable real Oracle database connection
- Add proper error handling and retry logic
- Verify with actual schema data

### Backend Tasks

#### 3.1 Update .env with Oracle Credentials
**File**: `.env` (create if not exists)

```env
# Oracle Connection
ORACLE_HOST=oracle-xe
ORACLE_PORT=1521
ORACLE_SERVICE=XEPDB1
ORACLE_USER=oraclevision
ORACLE_PASSWORD=vision123
```

#### 3.2 Update Oracle Connection
**File**: `backend/app/db/oracle.py`

```python
# Already has real implementation
# Add:
- Connection timeout handling
- Retry logic with exponential backoff
- Better error messages
- Connection pool health check
```

#### 3.3 Add Docker Compose for Ollama
**File**: `docker-compose.yml`

```yaml
# Add ollama service:
ollama:
  image: ollama/ollama:latest
  ports:
    - "11434:11434"
  volumes:
    - ollama-data:/root/.ollama
  networks:
    - oracle-vision
```

### Testing

#### 3.4 Test with Docker
```bash
# Start all services
docker-compose up -d

# Check Ollama
curl http://localhost:11434/api/tags

# Pull models
docker exec -it oracle-vision-ollama-1 ollama pull llama3.2
docker exec -it oracle-vision-ollama-1 ollama pull nomic-embed-text

# Test Oracle
docker exec -it oracle-vision-oracle-xe-1 sqlplus system/oracle123@//localhost:1521/XEPDB1
```

---

## Phase 4: OAuth2/JWT Full Implementation - Est: 2-3 days

### Objectives
- Complete OAuth2/JWT flow with proper security
- Implement token rotation and blacklisting
- Add rate limiting and audit logging

### Database Tasks

#### 4.1 Create Additional Tables
**File**: `init.sql`

```sql
-- Refresh tokens table
CREATE TABLE refresh_tokens (
    id SERIAL PRIMARY KEY,
    token_hash VARCHAR(255) NOT NULL UNIQUE,
    user_id VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    revoked BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    user_agent TEXT
);

-- Audit logs table
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255),
    action VARCHAR(100) NOT NULL,
    details JSONB,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Password reset tokens table
CREATE TABLE password_reset_tokens (
    id SERIAL PRIMARY KEY,
    token_hash VARCHAR(255) NOT NULL UNIQUE,
    user_id VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Backend Tasks

#### 4.2 Update User Models
**File**: `backend/app/models/user.py`

```python
# Add:
class RefreshToken(BaseModel):
    id: int
    token_hash: str
    user_id: str
    expires_at: datetime
    revoked: bool

class AuditLog(BaseModel):
    id: int
    user_id: Optional[str]
    action: str
    details: Optional[dict]
    ip_address: Optional[str]
    created_at: datetime

class PasswordReset(BaseModel):
    email: str

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str
```

#### 4.3 Update Auth Endpoints
**File**: `backend/app/api/v1/auth/__init__.py`

```python
# Current:
# - POST /login (simple JWT)
# - POST /logout (stub)
# - POST /refresh (stub)

# Add:
@router.post("/register")
async def register(user: UserCreate):
    """User registration with password hashing"""
    # Create user, return token

@router.post("/password-reset")
async def request_password_reset(request: PasswordReset):
    """Request password reset"""
    # Generate reset token, send email (stub)

@router.post("/password-reset/confirm")
async def confirm_password_reset(request: PasswordResetConfirm):
    """Confirm password reset"""
    # Validate token, update password

# Update existing:
@router.post("/login")
async def login(request: LoginRequest):
    """Return access + refresh token"""
    # Generate both tokens, store refresh token

@router.post("/refresh")
async def refresh_token(refresh_token: str):
    """Exchange refresh token for new access token"""
    # Validate, rotate (invalidate old, create new)

@router.post("/logout")
async def logout(refresh_token: str):
    """Revoke refresh token"""
    # Add to blacklist
```

#### 4.4 Create Security Middleware
**New File**: `backend/app/middleware/rate_limit.py`

```python
# Rate limiting:
# - Login: 5 attempts per minute per IP
# - API: 100 requests per minute per user

class RateLimitMiddleware:
    # Implementation with Redis for distributed rate limiting
```

#### 4.5 Update Security Module
**File**: `backend/app/core/security.py`

```python
# Add:
- verify_refresh_token()     # Verify refresh token
- hash_token()               # Hash tokens for storage
- is_token_revoked()         # Check token blacklist
- revoke_token()             # Add to blacklist
```

### Frontend Tasks

#### 4.6 Create Register Page
**New File**: `frontend/src/pages/RegisterPage.tsx`

```typescript
// Features:
// - Email input
// - Password input (with strength indicator)
// - Confirm password
// - Submit to /register
// - Redirect to login on success
```

#### 4.7 Update Auth Store
**File**: `frontend/src/stores/authStore.ts`

```typescript
// Add:
// - refreshToken storage
// - auto-refresh before expiration
// - logout revokes refresh token
```

---

## Phase 5: Minor Features - Est: 1-2 days

### 5.1 ERD Export PNG/SVG

**File**: `frontend/src/pages/ERDPage.tsx`

```typescript
// Add export functionality:
// - Use html-to-image or react-flow's built-in export
// - Export to PNG
// - Export to SVG

const exportToPNG = () => {
  // Get React Flow instance
  // Use toPng() or similar
}

const exportToSVG = () => {
  // Use toSvg() or similar
}
```

### 5.2 Query Export Excel

**File**: `backend/app/api/v1/query/__init__.py`

```python
@router.post("/export")
async def export_results(request: ExecuteRequest, format: str = "csv"):
    """Export query results"""
    # Support: csv, json, xlsx
    # Use xlsxwriter or openpyxl for Excel
```

**Frontend**: Add export buttons to query results

### 5.3 Execution Plan View

**File**: `backend/app/api/v1/query/__init__.py`

```python
@router.post("/explain")
async def explain_query(sql: str):
    """Get execution plan"""
    # Run EXPLAIN PLAN FOR
    # Return plan details
```

**Frontend**: Add "Show Plan" button, display plan in modal

### 5.4 SQL Preview Tabs

**Frontend**: Convert single SQL preview to tabbed interface

```typescript
// Multiple SQL tabs:
// - Add tab state management
// - Tab close/add buttons
// - Tab switching preserves SQL
```

---

## Phase 6: Testing & Bug Fixing - Est: 1-2 days

### 6.1 Unit Tests
- Test vector service
- Test LLM router
- Test auth endpoints
- Test Oracle queries

### 6.2 Integration Tests
- Test full text-to-sql flow
- Test ERD generation
- Test query execution

### 6.3 E2E Tests
- Test login flow
- Test ERD viewing
- Test query generation and execution

### 6.4 Bug Fixes
- Fix all identified issues
- Fix performance issues
- Fix security issues

---

## File Structure Summary

```
oracle-ai-workspace-opencode/
├── SPEC.md                      # ✅ Updated with section 12
├── implementation-plan.md       # 📄 This file
├── .env                         # 🔲 Create
├── docker-compose.yml           # 🔲 Update (add Ollama)
├── init.sql                     # 🔲 Update (add tables)
│
├── backend/
│   ├── app/
│   │   ├── db/
│   │   │   ├── postgres.py      # 🔲 Update (vector ops)
│   │   │   └── oracle.py        # 🔲 Update (error handling)
│   │   ├── services/
│   │   │   ├── vector.py        # 📄 Create
│   │   │   └── text_to_sql.py   # 🔲 Update (LLM)
│   │   ├── llm/
│   │   │   ├── router.py        # 📄 Create
│   │   │   ├── ollama.py        # 📄 Create
│   │   │   └── prompts/
│   │   │       └── text_to_sql.py # 📄 Create
│   │   ├── api/v1/
│   │   │   ├── vector/__init__.py # 🔲 Update
│   │   │   ├── auth/__init__..py  # 🔲 Update
│   │   │   └── query/__init__.py  # 🔲 Update
│   │   ├── middleware/
│   │   │   └── rate_limit.py    # 📄 Create
│   │   ├── models/
│   │   │   └── user.py          # 🔲 Update
│   │   └── core/
│   │       └── security.py      # 🔲 Update
│   └── requirements.txt
│
└── frontend/
    └── src/
        ├── components/
        │   ├── vector/
        │   │   ├── VectorSync.tsx     # 📄 Create
        │   │   └── SemanticSearch.tsx # 📄 Create
        │   └── erd/
        │       └── ERDPage.tsx        # 🔲 Update
        ├── pages/
        │   └── RegisterPage.tsx       # 📄 Create
        ├── services/
        │   └── vectorService.ts       # 📄 Create
        └── stores/
            └── authStore.ts           # 🔲 Update
```

---

## Dependencies to Install

### Backend
```txt
# requirements.txt - add:
aiohttp>=3.9.0
xlsxwriter>=3.1.0
openpyxl>=3.1.0
```

### Frontend
```json
// package.json - add:
html-to-image@latest
```

---

## Success Criteria

- [ ] Phase 1: Vector DB fully operational with semantic search
- [ ] Phase 2: Ollama generating SQL with >80% accuracy on simple queries
- [ ] Phase 3: Oracle connection working with real schema
- [ ] Phase 4: Full OAuth2 flow with rate limiting and audit logging
- [ ] Phase 5: All minor features implemented
- [ ] Phase 6: All tests passing, no critical bugs

---

*Document Version: 1.0*
*Created: 2026-03-27*
*Status: Active*