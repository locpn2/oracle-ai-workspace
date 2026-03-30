# Changelog

All notable changes to the OracleVision project will be documented in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

## [2.0.0] - 2026-03-30

### Fixed

#### Phase 1: Quick Wins
- **Docker healthchecks**: Frontend healthcheck now correctly checks `localhost:80/` instead of backend URL
- **Ollama healthcheck**: Changed from `exit 0` to `curl -sf http://localhost:11434/api/tags` to verify actual availability
- **Docker memory**: Increased Ollama mem_limit from 4GB to 6GB, start_period to 300s
- **Success logic**: Fixed `success` field — now uses `has_sql and not has_error` instead of `not result.get("error")`
- **HTTP status codes**: Error responses now return proper HTTP status codes (400/500/504) instead of returning 200 with error content
- **Security**: Added `.env.docker` to `.gitignore`, removed OPENAI_API_KEY exposure risk

### Added

#### Phase 2: Core Improvements
- **Smart LLM routing** (`backend/app/llm/router.py`):
  - Query complexity classifier (`classify_query_complexity()`)
  - Simple queries use `phi3:mini` (small model, faster)
  - Complex queries use `llama3.2` (full model, better reasoning)
  - Both fall back to OpenAI API when local LLM unavailable
- **Real availability check** (`backend/app/llm/ollama.py`):
  - `is_available()` now sends actual test chat request (`num_predict=1`)
  - Detects model loading delays, not just API availability
- **Template fallback** (`backend/app/services/text_to_sql.py`):
  - 6 patterns: `show_table`, `count_table`, `top_n`, `max`, `min`, `avg`
  - Helper functions: `_find_table()`, `_find_column()`
  - Response time: 10-12ms (vs old 75s timeout)
  - Clear error message for unmatched queries (no more wrong SQL)
- **Request timeout**:
  - `asyncio.wait_for()` with configurable `LLM_REQUEST_TIMEOUT=30s`
  - Returns HTTP 504 Gateway Timeout on timeout
  - Prevents infinite hangs

#### Phase 3: Architecture Improvements
- **Connection pooling** (`backend/app/llm/ollama.py`):
  - Shared `aiohttp.ClientSession` with `TCPConnector(limit=10, limit_per_host=5)`
  - Connection reuse across requests
  - `close()` method for graceful shutdown
- **SQL validation**:
  - `validate_sql()` function using `SQL_VALIDATION_PROMPT`
  - LLM-based syntax and semantic validation
- **Persistent query history**:
  - Wired up existing `QueryHistoryDB` class from `postgres.py`
  - `query_history_db.add_query()` called alongside in-memory list
  - History endpoint supports `?use_db=true` for PostgreSQL queries
- **SSE streaming endpoint**:
  - New endpoint: `/api/v1/query/text-to-sql/stream` (GET)
  - Real-time progress events: `status`, `generating`, `validation`, `result`
  - Enables progress indicators in frontend

### Configuration

- **Environment variables** (`.env`):
  - Added `OLLAMA_SMALL_MODEL=phi3:mini`
  - Added `LLM_REQUEST_TIMEOUT=30`
  - Added `LLM_OLLAMA_TIMEOUT=30`

- **Docker services** (`docker-compose.yml`):
  - Ollama mem_limit increased to 6GB
  - Ollama healthcheck uses chat API verification
  - Frontend healthcheck corrected

### Testing

- **Updated test files**:
  - `backend/tests/test_services.py` — Template fallback, query classification, fail clearly
  - `backend/tests/test_integration.py` — SSE streaming test
  - All Python syntax verified in container
  - All imports verified working

---

## [1.1.0] - 2026-03-27

### Added
- Implementation Plan (Section 12) to SPEC.md
- Technology Decisions section
- Implementation Phases (6 phases)

### Changed
- Updated document status to "Updated with Implementation Plan"

---

## [1.0.0] - 2026-03-25

### Added
- Initial SPEC.md with full project specification
- Docker Compose configuration
- Frontend (React SPA) with ERD Viewer, Query UI
- Backend (FastAPI) with Text-to-SQL, Schema, Auth services
- Ollama LLM integration (llama3.2)
- PostgreSQL with pgvector
- Oracle XE database
- Redis cache/session

---

## Performance Metrics

### Before vs After (Text-to-SQL)

| Scenario | Before | After | Improvement |
|----------|--------|-------|-------------|
| LLM unavailable (cold) | 75s timeout | 10-12ms template | 99.98% faster |
| LLM unavailable (unmatched) | 75s → wrong SQL | 10ms → clear error | Correct + fast |
| LLM warm | 15-20s | 5-15s | 25-50% faster |
| Simple query (phi3:mini) | 15-20s | 3-8s | 60-80% faster |

### Architecture Diagram (Current)

```
User Input (Natural Language)
         │
         ▼
┌─────────────────┐
│ Query Complexity │
│ Classifier       │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
 Simple    Complex
    │         │
    ▼         ▼
┌────────┐ ┌────────┐
│phi3:mini│ │llama3.2│
└────┬────┘ └────┬────┘
     │           │
     └─────┬─────┘
           │ fail?
           ▼
     ┌──────────┐
     │ OpenAI   │
     │ API      │
     └────┬─────┘
          │ fail?
          ▼
    ┌──────────────┐
    │ Template     │
    │ Fallback     │
    │ (6 patterns) │
    └──────┬───────┘
           │ no match
           ▼
    ┌──────────────┐
    │ Clear Error  │
    │ (HTTP 400)   │
    └──────────────┘
```

---

*Document Version: 1.0*
*Created: 2026-03-30*
*Last Updated: 2026-03-30*
