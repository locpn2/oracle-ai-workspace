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
├── backend/                 # Spring Boot application (DDD structure)
│   ├── src/main/java/com/oracleai/workspace/
│   │   ├── schema/          # Schema Bounded Context
│   │   ├── chat/           # AI/Chat Bounded Context
│   │   ├── vector/         # Vector Store Bounded Context
│   │   ├── auth/           # Authentication Bounded Context
│   │   └── shared/         # Shared kernel (config, exceptions, DTOs)
│   └── pom.xml
├── frontend/               # React application
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services (Axios)
│   │   └── hooks/         # Custom React hooks
│   └── package.json
├── docs/
│   ├── requirement.md     # Full requirement specification
│   └── archived/ddd-analysis.md  # DDD Strategic Design
└── docker-compose.yml     # Infrastructure
```

## Build Commands

### Backend (Maven)

```bash
# Build the project
cd backend && ./mvnw clean package

# Run development server
cd backend && ./mvnw spring-boot:run

# Run all tests
cd backend && ./mvnw test

# Run a single test class
cd backend && ./mvnw test -Dtest=SchemaExtractorTest

# Run a single test method
cd backend && ./mvnw test -Dtest=FlatteningServiceTest#testFlattenRow

# Run tests with verbose output
cd backend && ./mvnw test -Dverbose=true

# Skip tests during build
cd backend && ./mvnw clean package -DskipTests

# Run integration tests
cd backend && ./mvnw verify

# Check code style (if Checkstyle configured)
cd backend && ./mvnw checkstyle:check
```

### Frontend (npm)

```bash
# Install dependencies
cd frontend && npm install

# Run development server
cd frontend && npm run dev

# Run tests
cd frontend && npm test

# Run tests in watch mode
cd frontend && npm test -- --watch

# Run a single test file
cd frontend && npm test -- src/services/TextToSQLService.test.ts

# Run tests with coverage
cd frontend && npm test -- --coverage

# Build for production
cd frontend && npm run build

# Run linter
cd frontend && npm run lint

# Fix lint errors automatically
cd frontend && npm run lint -- --fix
```

### Infrastructure

```bash
# Start all services (Oracle, PostgreSQL, Redis)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Reset volumes
docker-compose down -v
```

## Code Style Guidelines

### General Principles

- **SOLID** principles for object-oriented design
- **DRY** (Don't Repeat Yourself) - extract common logic
- **KISS** (Keep It Simple, Stupid) - prefer simple solutions
- Write **self-documenting code** with clear naming

### Backend (Java/Spring)

#### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Classes | PascalCase | `SchemaExtractor`, `TextToSQLService` |
| Methods | camelCase | `extractTables()`, `convertToSQL()` |
| Variables | camelCase | `tableName`, `embeddingVector` |
| Constants | UPPER_SNAKE_CASE | `MAX_BATCH_SIZE`, `DEFAULT_MODEL` |
| Packages | lowercase | `com.oracleai.workspace.schema` |
| DTOs | suffix with DTO | `TableDTO`, `ChatRequestDTO` |
| Entities | noun, no suffix | `User`, `Document` |
| Services | noun + Service | `UserService`, `EmbeddingService` |
| Controllers | suffix with Controller | `SchemaController`, `ChatController` |

#### Code Formatting

- Use **4 spaces** for indentation (no tabs)
- Line length: **120 characters** max
- Opening brace on same line: `if (condition) {`
- Blank lines between methods
- JavaDoc for public APIs

#### Imports

```java
// Order: static, java, javax, org, com
import static com.oracleai.workspace.util.Constants.*;
import java.util.List;
import java.util.Optional;
import javax.persistence.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import com.oracleai.workspace.schema.entity.Table;
```

#### Error Handling

- Use **custom exceptions** for business logic errors
- **Global exception handler** with `@ControllerAdvice`
- Return proper HTTP status codes:
  - `200 OK` - Success
  - `201 Created` - Resource created
  - `400 Bad Request` - Validation error
  - `401 Unauthorized` - Authentication failed
  - `404 Not Found` - Resource not found
  - `500 Internal Server Error` - Unexpected error
- Log exceptions with appropriate level (ERROR for failures, WARN for recoverable)

```java
@ExceptionHandler(ResourceNotFoundException.class)
public ResponseEntity<ErrorResponse> handleNotFound(ResourceNotFoundException ex) {
    return ResponseEntity.status(404)
        .body(new ErrorResponse("NOT_FOUND", ex.getMessage()));
}
```

#### DDD Structure

Follow the **4 Bounded Contexts**:

```
schema/     - Schema extraction and visualization
chat/       - AI chat and Text-to-SQL
vector/     - Vector embedding and semantic search
auth/       - Authentication and authorization
```

Each context follows:
```
context/
├── domain/
│   ├── entity/          # Aggregate roots and entities
│   ├── valueobject/     # Value objects
│   └── service/         # Domain services
├── repository/          # Data access
├── api/                 # REST controllers
└── dto/                 # Request/Response DTOs
```

### Frontend (React/TypeScript)

#### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Components | PascalCase | `ERDDiagram`, `ChatWindow` |
| Hooks | camelCase + use prefix | `useSchema`, `useChat` |
| Services | camelCase | `schemaApi.ts`, `chatApi.ts` |
| Types/Interfaces | PascalCase | `TableData`, `ChatMessage` |
| Constants | UPPER_SNAKE_CASE | `API_BASE_URL` |
| CSS Classes | kebab-case | `.erd-node`, `.chat-message` |

#### Code Formatting

- Use **ESLint** and **Prettier**
- Use **2 spaces** for indentation
- Prefer **arrow functions** for callbacks
- Use **functional components** with hooks
- Destructuring for props and state

#### Component Structure

```typescript
// Preferred: Functional component with hooks
interface Props {
  tables: Table[];
  onSelect: (table: Table) => void;
}

export const ERDDiagram: React.FC<Props> = ({ tables, onSelect }) => {
  const [zoom, setZoom] = useState(1);
  
  useEffect(() => {
    // effect logic
  }, [tables]);
  
  return (
    <div className="erd-diagram">
      {/* render */}
    </div>
  );
};
```

#### Error Handling

- Use **try-catch** for async operations
- Show user-friendly error messages
- Use **React Query** for server state management
- Handle loading and error states

```typescript
const { data, isLoading, error } = useQuery({
  queryKey: ['tables'],
  queryFn: fetchTables,
});
```

#### Imports (Order)

```typescript
// React/Next
import React, { useState, useEffect } from 'react';

// External libraries
import axios from 'axios';
import { useQuery } from '@tanstack/react-query';

// Internal - components
import { Button } from '@/components/ui/Button';

// Internal - hooks
import { useSchema } from '@/hooks/useSchema';

// Internal - services
import { schemaApi } from '@/services/schemaApi';

// Types
import type { Table } from '@/types/schema';
```

### Database

#### Oracle (Source)

- Read-only access for schema extraction
- Use **ALL_TABLES**, **ALL_TAB_COLUMNS**, **ALL_CONSTRAINTS** for metadata
- Connection pooling via HikariCP

#### PostgreSQL + pgvector (Vector Store)

- Use **vector(768)** for BGE-base embeddings
- Index: `USING ivfflat (embedding_vector cosine_ops)`
- Cosine distance for similarity search

### API Design

#### REST Endpoints

| Context | Endpoint | Method | Description |
|---------|----------|--------|-------------|
| Schema | `/api/schema/tables` | GET | List all tables |
| Schema | `/api/schema/erd` | GET | Get ERD JSON for D3.js |
| Chat | `/api/chat/query` | POST | Text-to-SQL |
| Vector | `/api/vector/embed-table` | POST | Embed table rows |
| Vector | `/api/vector/search` | GET | Semantic search |
| Auth | `/api/auth/login` | POST | User login |

#### Response Format

```json
{
  "success": true,
  "data": { ... },
  "message": "Optional message"
}
```

### Git Commit Convention

```
<type>(<scope>): <description>

Types:
- feat:    New feature
- fix:     Bug fix
- refactor: Code refactoring
- docs:    Documentation
- chore:   Build process, dependencies
- test:    Adding tests

Examples:
feat(schema): Add metadata extraction from Oracle
feat(ai): Integrate Groq API for Text-to-SQL
fix(vector): Handle NULL values in flattening
docs(api): Add API documentation
```

## Testing Guidelines

### Backend Tests

- Unit tests for **domain services**
- Integration tests for **API endpoints**
- Test naming: `MethodName_StateUnderTest_ExpectedResult`

```java
@Test
void extractTables_WithValidConnection_ReturnsTableList() {
    // Arrange
    when(oracleDataSource.getConnection()).thenReturn(mockConnection);
    
    // Act
    List<Table> tables = schemaExtractor.extractTables();
    
    // Assert
    assertNotNull(tables);
    assertFalse(tables.isEmpty());
}
```

### Frontend Tests

- Use **Jest** + **React Testing Library**
- Test user interactions, not implementation
- Mock API calls

```typescript
test('submitting query shows loading state', async () => {
  render(<ChatWindow />);
  
  fireEvent.change(screen.getByRole('textbox'), {
    target: { value: 'Find employees' }
  });
  
  expect(screen.getByText('Loading...')).toBeInTheDocument();
});
```

## Security Guidelines

- Never commit secrets (API keys, passwords) to git
- Use environment variables for sensitive data
- Validate and sanitize all user inputs
- SQL validation: **whitelist only SELECT queries** for Text-to-SQL
- Use **BCrypt** for password hashing
- Implement **JWT** with expiration

## Important Notes

- AI uses hybrid fallback: **Groq → Ollama → Gemini**
- Vector embedding uses **BGE-base** via Ollama
- Schema extraction queries: **ALL_TABLES**, **ALL_TAB_COLUMNS**, **ALL_CONSTRAINTS**
- Flattening logic converts DB rows to text documents for embedding
- Follow **DDD** with 4 Bounded Contexts
