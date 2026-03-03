# AGENTS.md

## Project Overview

**Oracle DB Visualization & RDBMS-to-Vector Converter** - Công cụ trích xuất schema Oracle DB để trực quan hóa (D3.js ERD) và chuyển đổi dữ liệu sang Vector DB với AI Text-to-SQL.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Spring Boot 3.x + Spring AI |
| Frontend | React 18 + Vite + Tailwind CSS + D3.js |
| Source DB | Oracle DB |
| Vector DB | PostgreSQL 15 + pgvector |
| AI (Primary) | Groq API (llama-3.1-8b-instant) |
| AI (Local) | Ollama (SQLCoder-7B, BGE-base) |
| AI (Fallback) | Google Gemini 2.0 |

## Project Structure

```
oracle-ai-workspace/
├── backend/                 # Spring Boot application
│   ├── src/main/java/...
│   └── pom.xml
├── frontend/               # React application
│   ├── src/...
│   └── package.json
├── docs/
│   └── spec/
│       └── requirement.md  # Full requirement specification
├── docker-compose.yml      # Infrastructure
└── AGENTS.md              # This file
```

## Getting Started

### Prerequisites

- Java 17+
- Node.js 18+
- Docker & Docker Compose
- Ollama (for local AI)

### Environment Variables

Xem `.env.example` trong requirement.md

### Commands

```bash
# Start infrastructure
docker-compose up -d

# Start backend
cd backend && ./mvnw spring-boot:run

# Start frontend
cd frontend && npm install && npm run dev
```

## Coding Conventions

### Backend (Java/Spring)

- Use Spring Data JPA for Oracle
- Use Spring AI for LLM integration
- Follow Spring Boot conventions
- Place AI logic in `service/ai/` package

### Frontend (React)

- Use functional components with hooks
- Use Tailwind CSS for styling
- Use D3.js for ERD visualization
- API calls via Axios

### Database

- Oracle: Source database (read-only access)
- PostgreSQL: Vector storage with pgvector

## Key Modules

| Module | Description |
|--------|-------------|
| `SchemaExtractor` | Extract table/column/FK metadata from Oracle |
| `TextToSQLService` | Convert natural language to SQL using AI |
| `EmbeddingService` | Convert rows to vectors using BGE-base |
| `VectorSearchService` | Semantic search with cosine similarity |

## Testing

```bash
# Backend tests
./mvnw test

# Frontend tests
npm test
```

## Important Notes

- AI uses hybrid fallback: Groq → Ollama → Gemini
- Vector embedding uses BGE-base via Ollama
- Schema extraction queries: ALL_TABLES, ALL_TAB_COLUMNS, ALL_CONSTRAINTS
- Flattening logic converts DB rows to text documents for embedding
