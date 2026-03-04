# AGENTS.md

## Project Overview

Oracle DB Visualization & RDBMS-to-Vector Converter - Extract Oracle DB schema for visualization (D3.js ERD) and convert data to Vector DB with AI Text-to-SQL.

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

## Build Commands

```bash
# Backend - Build
cd backend && mvn clean package

# Backend - Run dev
cd backend && mvn spring-boot:run

# Backend - Run all tests
cd backend && mvn test

# Backend - Run single test class
cd backend && mvn test -Dtest=SchemaApplicationServiceTest

# Backend - Run single test method
cd backend && mvn test -Dtest=SchemaApplicationServiceTest#testExtractTables

# Backend - Skip tests
cd backend && mvn clean package -DskipTests
```

## Architecture

### DDD Bounded Contexts (4)

```
com.oracleai.workspace/
├── schema/      # Schema extraction, ERD generation
├── chat/        # AI chat, Text-to-SQL
├── vector/      # Embedding, semantic search
└── auth/        # Authentication, user management
```

### Hexagonal Structure (per context)

```
context/
├── domain/entity/           # Aggregate roots
├── domain/valueobject/     # Value objects
├── application/port/in/    # Use case interfaces
├── application/port/out/   # Repository interfaces
├── application/service/    # Application services
├── api/                    # REST controllers
└── infrastructure/         # Adapters, repositories
```

## Code Style - Backend (Java)

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Classes | PascalCase | `Table`, `SchemaService` |
| Methods | camelCase | `extractTables()` |
| Variables | camelCase | `tableName` |
| Constants | UPPER_SNAKE | `MAX_BATCH_SIZE` |
| Packages | lowercase | `com.oracleai.workspace.schema` |
| DTOs | suffix DTO | `TableDTO` |
| Value Objects | immutable records | `TableName` |
| Controllers | suffix Controller | `SchemaController` |
| Use Cases | suffix UseCase | `ExtractSchemaUseCase` |

### Formatting Rules

- **4 spaces** indentation, no tabs
- **120 chars** max line length
- Opening brace on same line: `if (condition) {`
- Use **Builder pattern** for entities
- **Immutable** value objects (final class/fields, no setters)

### Imports Order

```java
// java.* → javax.* → org.springframework.* → com.oracleai.workspace.*
import java.util.List;
import javax.persistence.*;
import org.springframework.beans.factory.annotation.*;
import com.oracleai.workspace.schema.domain.entity.Table;
```

### Entity Example

```java
public final class Table {
    private final TableName name;
    private final List<Column> columns;

    private Table(Builder builder) {
        this.name = builder.name;
        this.columns = List.copyOf(builder.columns);
    }

    public TableName getName() { return name; }

    public static Builder builder() { return new Builder(); }

    public static class Builder {
        private TableName name;
        public Builder name(TableName n) { this.name = n; return this; }
        public Table build() { return new Table(this); }
    }
}
```

### Value Object Example

```java
public record TableName(String value) {
    public TableName {
        if (value == null || value.isBlank())
            throw new IllegalArgumentException("TableName cannot be blank");
    }
}
```

### Error Handling

- Custom exceptions for business logic
- `@ControllerAdvice` for global handling
- HTTP status codes: 200, 201, 400, 401, 404, 500

### Repository Pattern

```java
// Port: application/port/out
public interface SchemaRepository {
    List<Table> findAll();
    Optional<Table> findByName(TableName name);
}
```

## API Endpoints

| Context | Endpoint | Method | Description |
|---------|----------|--------|-------------|
| Schema | `/api/schema/tables` | GET | List tables |
| Schema | `/api/schema/tables/{name}` | GET | Table details |
| Schema | `/api/schema/erd` | GET | ERD JSON |
| Chat | `/api/chat/query` | POST | Text-to-SQL |
| Vector | `/api/vector/embed-table` | POST | Embed rows |
| Vector | `/api/vector/search` | GET | Semantic search |
| Auth | `/api/auth/login` | POST | Login |

## Response Format

```json
{ "success": true, "data": { ... }, "message": "Optional" }
```

## Security

- Never commit secrets - use env vars
- Validate/sanitize user inputs
- SQL: whitelist only SELECT queries
- Use BCrypt for passwords, JWT with expiration

## Testing

```
MethodName_StateUnderTest_ExpectedResult
```

```java
@Test
void extractTables_WithValidConnection_ReturnsTableList() {
    when(oracleDataSource.getConnection()).thenReturn(mockConn);
    List<Table> tables = service.extractTables();
    assertNotNull(tables);
}
```

## Git Commit Convention

```
<type>(<scope>): <description>
Types: feat, fix, refactor, docs, chore, test
```
