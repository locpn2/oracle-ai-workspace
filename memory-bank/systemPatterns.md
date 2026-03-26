# System Patterns - VecBase

## Kiến trúc tổng quan

### High-Level Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (React)                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   ERD    │  │   AI     │  │  Vector  │  │  Schema  │   │
│  │ Viewer   │  │  Query   │  │ Manager  │  │ Browser  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     API Gateway (Nginx)                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Backend (Spring Boot)                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                   Application Layer                    │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐   │  │
│  │  │ Schema   │  │   AI     │  │     Vector       │   │  │
│  │  │ Service  │  │ Service  │  │    Service        │   │  │
│  │  └──────────┘  └──────────┘  └──────────────────┘   │  │
│  └──────────────────────────────────────────────────────┘  │
│                              │                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                   Domain Layer                         │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐   │  │
│  │  │ Database │  │  Query   │  │    Vector        │   │  │
│  │  │  Schema  │  │  Result  │  │   Collection     │   │  │
│  │  └──────────┘  └──────────┘  └──────────────────┘   │  │
│  └──────────────────────────────────────────────────────┘  │
│                              │                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                Infrastructure Layer                    │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐   │  │
│  │  │  Oracle  │  │   LLM    │  │    PgVector      │   │  │
│  │  │ Adapter  │  │ Adapter  │  │     Adapter      │   │  │
│  │  └──────────┘  └──────────┘  └──────────────────┘   │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│    Oracle    │    │   OpenAI     │    │  PostgreSQL  │
│   Database   │    │     API      │    │  + pgvector  │
└──────────────┘    └──────────────┘    └──────────────┘
```

## Design Patterns

### 1. Hexagonal Architecture (Ports & Adapters)
**Mục đích**: Tách biệt domain logic khỏi infrastructure

```
┌─────────────────────────────────────────┐
│              Domain Core                 │
│  ┌─────────────────────────────────┐   │
│  │         Entities                 │   │
│  │  - DatabaseSchema                │   │
│  │  - Table                         │   │
│  │  - Column                        │   │
│  │  - VectorCollection              │   │
│  │  - QueryResult                   │   │
│  └─────────────────────────────────┘   │
│  ┌─────────────────────────────────┐   │
│  │         Ports (Interfaces)       │   │
│  │  - SchemaRepository              │   │
│  │  - VectorRepository              │   │
│  │  - AIService                     │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
┌───────────────┐      ┌───────────────┐
│   Adapters    │      │   Adapters    │
│  - Oracle     │      │  - PgVector   │
│  - OpenAI     │      │  - REST API   │
└───────────────┘      └───────────────┘
```

### 2. Repository Pattern
**Mục đích**: Abstract data access layer

```java
// Port (Domain)
public interface SchemaRepository {
    DatabaseSchema findByConnection(ConnectionConfig config);
    List<Table> findTablesBySchema(String schemaName);
}

// Adapter (Infrastructure)
@Repository
public class OracleSchemaRepository implements SchemaRepository {
    @Override
    public DatabaseSchema findByConnection(ConnectionConfig config) {
        // Oracle-specific implementation
    }
}
```

### 3. Strategy Pattern
**Mục đích**: Support multiple vector DB backends

```java
public interface VectorizationStrategy {
    VectorCollection convert(DatabaseSchema schema);
    void save(VectorCollection collection);
}

public class PgVectorStrategy implements VectorizationStrategy { }
public class RedisVectorStrategy implements VectorizationStrategy { }
```

### 4. Builder Pattern
**Mục đích**: Construct complex objects step by step

```java
DatabaseSchema schema = DatabaseSchema.builder()
    .name("HR_SCHEMA")
    .tables(tables)
    .relationships(relationships)
    .metadata(metadata)
    .build();
```

### 5. Observer Pattern
**Mục đích**: Track conversion progress

```java
public interface ConversionProgressObserver {
    void onProgress(ConversionProgressEvent event);
    void onComplete(ConversionCompleteEvent event);
    void onError(ConversionErrorEvent event);
}
```

## Bounded Contexts

### 1. Visualization Context
**Responsibility**: ERD generation and schema browsing

```
┌─────────────────────────────────────┐
│       Visualization Context          │
│  ┌─────────────────────────────┐   │
│  │         Entities             │   │
│  │  - ERDDiagram                │   │
│  │  - DiagramNode               │   │
│  │  - DiagramEdge               │   │
│  │  - LayoutConfig              │   │
│  └─────────────────────────────┘   │
│  ┌─────────────────────────────┐   │
│  │         Services             │   │
│  │  - ERDGenerationService      │   │
│  │  - LayoutService             │   │
│  │  - ExportService             │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

### 2. AI Context
**Responsibility**: Natural language query processing

```
┌─────────────────────────────────────┐
│           AI Context                 │
│  ┌─────────────────────────────┐   │
│  │         Entities             │   │
│  │  - NaturalLanguageQuery      │   │
│  │  - GeneratedSQL              │   │
│  │  - QueryResult               │   │
│  │  - QueryHistory              │   │
│  └─────────────────────────────┘   │
│  ┌─────────────────────────────┐   │
│  │         Services             │   │
│  │  - TextToSQLService          │   │
│  │  - QueryExecutionService     │   │
│  │  - ResultFormattingService   │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

### 3. Conversion Context
**Responsibility**: RDBMS to Vector DB conversion

```
┌─────────────────────────────────────┐
│        Conversion Context            │
│  ┌─────────────────────────────┐   │
│  │         Entities             │   │
│  │  - ConversionJob             │   │
│  │  - MappingRule               │   │
│  │  - VectorCollection          │   │
│  │  - Embedding                 │   │
│  └─────────────────────────────┘   │
│  ┌─────────────────────────────┐   │
│  │         Services             │   │
│  │  - SchemaMappingService      │   │
│  │  - EmbeddingService          │   │
│  │  - VectorStorageService      │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

## Integration Patterns

### API Design
- **REST API** for CRUD operations
- **WebSocket** for real-time updates (conversion progress)
- **GraphQL** (future) for flexible queries

### Error Handling
```java
@ControllerAdvice
public class GlobalExceptionHandler {
    
    @ExceptionHandler(DatabaseConnectionException.class)
    public ResponseEntity<ErrorResponse> handleDatabaseError() { }
    
    @ExceptionHandler(AIServiceException.class)
    public ResponseEntity<ErrorResponse> handleAIError() { }
}
```

### Caching Strategy
- **L1 Cache**: In-memory (Caffeine) for schema metadata
- **L2 Cache**: Redis for query results
- **TTL**: 1 hour for schema, 15 minutes for queries

## Critical Implementation Paths

### 1. Schema Discovery Flow
```
User Request → SchemaService → OracleAdapter → Database
                    ↓
              Cache Schema
                    ↓
              Generate ERD → Return to Frontend
```

### 2. AI Query Flow
```
Natural Language → TextToSQLService → LLM Adapter → OpenAI
                        ↓
                  Generated SQL
                        ↓
              QueryExecutionService → Oracle
                        ↓
                  Format Results → Return to User
```

### 3. Vector Conversion Flow
```
Schema Selection → ConversionService → SchemaMappingService
                        ↓
                  Mapping Rules
                        ↓
              EmbeddingService → Generate Embeddings
                        ↓
              VectorStorageService → PgVector
                        ↓
                  Update Progress → Notify User