# Implementation Plan - Full Stack DDD

## Overview

This plan covers the complete implementation of all 4 Bounded Contexts (Auth, Schema, Chat, Vector) with full layer stack (Domain → Application → Infrastructure → API).

**Configuration:**
- Authentication: JWT
- AI Fallback: Groq → Ollama → Gemini (full chain)
- Connection Pool: Per-user (dedicated pool for each user)
- Embedding: Async processing with Spring @Async

---

## 1. Current Status

| Context | Domain (VO + Entity) | Application | Infrastructure | API |
|---------|---------------------|------------|----------------|-----|
| **Auth** | ✅ Done | ❌ | ❌ | ❌ |
| **Schema** | ✅ Partial | ✅ Partial | ❌ | ❌ |
| **Chat** | ✅ Done | ❌ | ❌ | ❌ |
| **Vector** | ✅ Done | ❌ | ❌ | ❌ |

---

## 2. Implementation Phases

### Phase 0: Infrastructure & Setup (NEW)
### Phase 1: Auth Context
### Phase 2: Schema Context
### Phase 3: Chat Context
### Phase 4: Vector Context

---

## Phase 0: Infrastructure & Setup

**Objective:** Set up Spring Boot project structure, dependencies, and configuration.

### Tasks:

| # | Task | File(s) | Status |
|---|------|---------|--------|
| 0.1 | Create Maven pom.xml with dependencies | `backend/pom.xml` | [ ] |
| 0.2 | Create application.yml configuration | `backend/src/main/resources/application.yml` | [ ] |
| 0.3 | Create application-dev.yml | `backend/src/main/resources/application-dev.yml` | [ ] |
| 0.4 | Create application-prod.yml | `backend/src/main/resources/application-prod.yml` | [ ] |
| 0.5 | Create main Application class | `backend/src/main/java/com/oracleai/workspace/OracleAiWorkspaceApplication.java` | [ ] |
| 0.6 | Create shared exceptions | `backend/src/main/java/com/oracleai/workspace/shared/exception/*.java` | [ ] |
| 0.7 | Create shared DTOs | `backend/src/main/java/com/oracleai/workspace/shared/dto/*.java` | [ ] |
| 0.8 | Create global exception handler | `backend/src/main/java/com/oracleai/workspace/shared/config/GlobalExceptionHandler.java` | [ ] |
| 0.9 | Create CORS config | `backend/src/main/java/com/oracleai/workspace/shared/config/CorsConfig.java` | [ ] |

#### 0.1 pom.xml Dependencies

```xml
<!-- Spring Boot Starters -->
- spring-boot-starter-web
- spring-boot-starter-data-jpa
- spring-boot-starter-security
- spring-boot-starter-validation
- spring-boot-starter-aop

<!-- Spring AI -->
- spring-ai-bom
- spring-ai-openai-spring-boot-starter (for Groq/Gemini)

<!-- Database -->
- ojdbc11 (Oracle)
- postgresql (PostgreSQL)
- pgvector (Vector support)

<!-- JWT -->
- jjwt-api, jjwt-impl, jjwt-jackson

<!-- Utilities -->
- lombok
- jackson-databind-nullable
- commons-lang3

<!-- Test -->
- spring-boot-starter-test
- h2-database (test)
```

---

## Phase 1: Auth Context

**Objective:** Implement user authentication with JWT, per-user connection pooling.

### 1.1 Domain Layer

| # | Task | File(s) | Status |
|---|------|---------|--------|
| 1.1.1 | Create UserId value object | `auth/domain/valueobject/UserId.java` | [ ] |
| 1.1.2 | Create ConnectionId value object | `auth/domain/valueobject/ConnectionId.java` | [ ] |
| 1.1.3 | Create DbConnection entity | `auth/domain/entity/DbConnection.java` | [ ] |
| 1.1.4 | Create UserRepository interface | `auth/domain/repository/UserRepository.java` | [ ] |

### 1.2 Application Layer

| # | Task | File(s) | Status |
|---|------|---------|--------|
| 1.2.1 | Create AuthUseCase interface | `auth/application/port/in/AuthUseCase.java` | [ ] |
| 1.2.2 | Create LoginRequest DTO | `auth/application/dto/LoginRequest.java` | [ ] |
| 1.2.3 | Create RegisterRequest DTO | `auth/application/dto/RegisterRequest.java` | [ ] |
| 1.2.4 | Create AuthResponse DTO | `auth/application/dto/AuthResponse.java` | [ ] |
| 1.2.5 | Create AuthApplicationService | `auth/application/service/AuthApplicationService.java` | [ ] |

### 1.3 Infrastructure Layer

| # | Task | File(s) | Status |
|---|------|---------|--------|
| 1.3.1 | Create User JPA entity | `auth/infrastructure/persistence/UserEntity.java` | [ ] |
| 1.3.2 | Create UserRepositoryImpl | `auth/infrastructure/persistence/UserRepositoryImpl.java` | [ ] |
| 1.3.3 | Create JwtUtil | `auth/infrastructure/security/JwtUtil.java` | [ ] |
| 1.3.4 | Create JwtAuthenticationFilter | `auth/infrastructure/security/JwtAuthenticationFilter.java` | [ ] |
| 1.3.5 | Create SecurityConfig | `auth/infrastructure/security/SecurityConfig.java` | [ ] |
| 1.3.6 | Create PerUserConnectionPool | `auth/infrastructure/pool/PerUserConnectionPool.java` | [ ] |

### 1.4 API Layer

| # | Task | File(s) | Status |
|---|------|---------|--------|
| 1.4.1 | Create AuthController | `auth/api/AuthController.java` | [ ] |

### Invariants (from invariants.md)

- **A1**: Username unique (validate in UserRepository)
- **A2**: Email unique (validate in UserRepository)
- **A3**: At least one role (constructor validation)
- Password policy: min 8 chars, uppercase, lowercase, digit (in HashedPassword.fromPlain())

---

## Phase 2: Schema Context

**Objective:** Extract Oracle DB metadata, generate ERD JSON for D3.js.

### 2.1 Domain Layer

| # | Task | File(s) | Status |
|---|------|---------|--------|
| 2.1.1 | Create SchemaId value object | `schema/domain/valueobject/SchemaId.java` | [ ] |
| 2.1.2 | Create SchemaVersion value object | `schema/domain/valueobject/SchemaVersion.java` | [ ] |
| 2.1.3 | Create PrimaryKey value object | `schema/domain/valueobject/PrimaryKey.java` | [ ] |
| 2.1.4 | Create ForeignKey value object | `schema/domain/valueobject/ForeignKey.java` | [ ] |
| 2.1.5 | Create ConstraintName value object | `schema/domain/valueobject/ConstraintName.java` | [ ] |
| 2.1.6 | Create TableRepository interface | `schema/domain/repository/TableRepository.java` | [ ] |

### 2.2 Application Layer

| # | Task | File(s) | Status |
|---|------|---------|--------|
| 2.2.1 | Create TableDTO | `schema/application/dto/TableDTO.java` | [ ] |
| 2.2.2 | Create ColumnDTO | `schema/application/dto/ColumnDTO.java` | [ ] |
| 2.2.3 | Create ERDResponse | `schema/application/dto/ERDResponse.java` | [ ] |
| 2.2.4 | Create TableMetadataService | `schema/application/service/TableMetadataService.java` | [ ] |

### 2.3 Infrastructure Layer

| # | Task | File(s) | Status |
|---|------|---------|--------|
| 2.3.1 | Create OracleSchemaExtractor | `schema/infrastructure/oracle/OracleSchemaExtractor.java` | [ ] |
| 2.3.2 | Create TableRepositoryImpl | `schema/infrastructure/persistence/TableRepositoryImpl.java` | [ ] |

### 2.4 API Layer

| # | Task | File(s) | Status |
|---|------|---------|--------|
| 2.4.1 | Create SchemaController | `schema/api/SchemaController.java` | [ ] |

### Requirements Coverage (requirement.md)

- **Req 1.1**: GET `/api/schema/tables` - List all tables
- **Req 1.2**: GET `/api/schema/tables/{name}` - Table details
- **Req 1.3**: GET `/api/schema/columns/{table}` - Columns of table
- **Req 1.4**: GET `/api/schema/relationships` - FK relationships
- **Req 1.5**: GET `/api/schema/erd` - Full ERD JSON

### Invariants (from invariants.md)

- **S1**: Table name unique in SchemaMetadata
- **S2**: FK reference to existing column
- **S5**: Column name unique in Table

---

## Phase 3: Chat Context

**Objective:** Text-to-SQL with AI, SQL validation (SELECT-only), fallback chain.

### 3.1 Domain Layer

| # | Task | File(s) | Status |
|---|------|---------|--------|
| 3.1.1 | Create SessionId value object | `chat/domain/valueobject/SessionId.java` | [ ] |
| 3.1.2 | Create MessageId value object | `chat/domain/valueobject/MessageId.java` | [ ] |
| 3.1.3 | Create ChatRepository interface | `chat/domain/repository/ChatRepository.java` | [ ] |

### 3.2 Application Layer

| # | Task | File(s) | Status |
|---|------|---------|--------|
| 3.2.1 | Create QueryUseCase interface | `chat/application/port/in/QueryUseCase.java` | [ ] |
| 3.2.2 | Create QueryRequest DTO | `chat/application/dto/QueryRequest.java` | [ ] |
| 3.2.3 | Create QueryResponse DTO | `chat/application/dto/QueryResponse.java` | [ ] |
| 3.2.4 | **Create SQLValidator (CRITICAL)** | `chat/application/service/SQLValidator.java` | [ ] |
| 3.2.5 | Create TextToSQLService | `chat/application/service/TextToSQLService.java` | [ ] |
| 3.2.6 | Create AIProvider enum | `chat/application/service/AIProvider.java` | [ ] |
| 3.2.7 | Create ChatApplicationService | `chat/application/service/ChatApplicationService.java` | [ ] |

### 3.3 Infrastructure Layer

| # | Task | File(s) | Status |
|---|------|---------|--------|
| 3.3.1 | Create GroqClient | `chat/infrastructure/ai/GroqClient.java` | [ ] |
| 3.3.2 | Create OllamaClient | `chat/infrastructure/ai/OllamaClient.java` | [ ] |
| 3.3.3 | Create GeminiClient | `chat/infrastructure/ai/GeminiClient.java` | [ ] |
| 3.3.4 | Create OracleQueryExecutor | `chat/infrastructure/oracle/OracleQueryExecutor.java` | [ ] |
| 3.3.5 | Create ChatRepositoryImpl | `chat/infrastructure/persistence/ChatRepositoryImpl.java` | [ ] |

### 3.4 API Layer

| # | Task | File(s) | Status |
|---|------|---------|--------|
| 3.4.1 | Create ChatController | `chat/api/ChatController.java` | [ ] |

### Requirements Coverage (requirement.md)

- **Req 3.1**: POST `/api/chat/query` - Natural language to SQL
- **Req 3.2**: GET `/api/chat/history` - Chat history
- **Req 3.3**: GET `/api/chat/history/{sessionId}` - Session history

### Invariants (CRITICAL from invariants.md)

- **C-SQL**: SQL must be SELECT-only (security - whitelist validation)
- **C1**: Session owner only add message
- **C2**: Valid status transition (ACTIVE → CLOSED/EXPIRED)
- **C4**: Max 100 messages per session

---

## Phase 4: Vector Context

**Objective:** Embed Oracle rows to pgvector, semantic search.

### 4.1 Domain Layer

| # | Task | File(s) | Status |
|---|------|---------|--------|
| 4.1.1 | Create JobId value object | `vector/domain/valueobject/JobId.java` | [ ] |
| 4.1.2 | Create BatchId value object | `vector/domain/valueobject/BatchId.java` | [ ] |
| 4.1.3 | Create RowId value object | `vector/domain/valueobject/RowId.java` | [ ] |
| 4.1.4 | Create VectorRepository interface | `vector/domain/repository/VectorRepository.java` | [ ] |

### 4.2 Application Layer

| # | Task | File(s) | Status |
|---|------|---------|--------|
| 4.2.1 | Create EmbeddingUseCase interface | `vector/application/port/in/EmbeddingUseCase.java` | [ ] |
| 4.2.2 | Create EmbedTableRequest DTO | `vector/application/dto/EmbedTableRequest.java` | [ ] |
| 4.2.3 | Create SearchRequest DTO | `vector/application/dto/SearchRequest.java` | [ ] |
| 4.2.4 | Create SearchResponse DTO | `vector/application/dto/SearchResponse.java` | [ ] |
| 4.2.5 | Create FlatteningService | `vector/application/service/FlatteningService.java` | [ ] |
| 4.2.6 | Create EmbeddingService | `vector/application/service/EmbeddingService.java` | [ ] |
| 4.2.7 | Create VectorSearchService | `vector/application/service/VectorSearchService.java` | [ ] |
| 4.2.8 | Create VectorApplicationService | `vector/application/service/VectorApplicationService.java` | [ ] |

### 4.3 Infrastructure Layer

| # | Task | File(s) | Status |
|---|------|---------|--------|
| 4.3.1 | Create OracleDataReader | `vector/infrastructure/oracle/OracleDataReader.java` | [ ] |
| 4.3.2 | Create OllamaEmbeddingClient | `vector/infrastructure/ai/OllamaEmbeddingClient.java` | [ ] |
| 4.3.3 | Create VectorRepositoryImpl | `vector/infrastructure/pgvector/VectorRepositoryImpl.java` | [ ] |
| 4.3.4 | Create EmbeddingJobExecutor (Async) | `vector/infrastructure/executor/EmbeddingJobExecutor.java` | [ ] |

### 4.4 API Layer

| # | Task | File(s) | Status |
|---|------|---------|--------|
| 4.4.1 | Create VectorController | `vector/api/VectorController.java` | [ ] |

### Requirements Coverage (requirement.md)

- **Req 4.1**: POST `/api/vector/embed-table` - Embed entire table
- **Req 4.2**: POST `/api/vector/embed-rows` - Embed specific rows
- **Req 4.3**: GET `/api/vector/search` - Semantic search
- **Req 4.4**: GET `/api/vector/status` - Embedding status

### Invariants (from invariants.md)

- **V1**: Valid embedding dimension (768)
- **V2**: Non-empty document
- **V3**: Similarity score range [-1, 1]
- Job state machine: PENDING → PROCESSING → COMPLETED/FAILED

---

## 3. Dependency Graph

```
Phase 0: Infrastructure
    └── pom.xml, application.yml, shared exceptions

Phase 1: Auth (Foundation)
    └── Phase 0
    
Phase 2: Schema
    └── Phase 0, Phase 1 (UserId reference)

Phase 3: Chat
    └── Phase 0, Phase 1, Phase 2 (schema for AI prompt)

Phase 4: Vector
    └── Phase 0, Phase 1, Phase 2 (table metadata)
```

---

## 4. Checklist Coverage

### Security Checklist (requirement.md)

| Item | Implementation |
|------|----------------|
| JWT token with expiration | JwtUtil (24h default) |
| SQL SELECT-only whitelist | SQLValidator (CRITICAL) |
| Password BCrypt hashing | HashedPassword (exists) |
| CORS configuration | CorsConfig |
| Rate limiting | To be added (Spring Bucket4j) |

### Performance Checklist

| Item | Implementation |
|------|----------------|
| Batch processing 1000 rows | EmbeddingConfig default |
| Connection pooling | HikariCP + PerUserConnectionPool |
| Vector index (ivfflat) | VectorRepositoryImpl SQL |
| Async embedding | Spring @Async + EmbeddingJobExecutor |

### Data Quality Checklist

| Item | Implementation |
|------|----------------|
| Handle NULL in flattening | FlatteningService |
| Handle special characters | FlatteningService sanitization |
| Handle BLOB/CLOB | FlatteningService skip/convert |

---

## 5. Implementation Order

1. **Phase 0**: Infrastructure & Setup
2. **Phase 1**: Auth Context (Foundation - required by all)
3. **Phase 2**: Schema Context (Core domain)
4. **Phase 3**: Chat Context (AI integration)
5. **Phase 4**: Vector Context (Semantic search)

---

## 6. Notes

- All domain entities and value objects already exist in codebase
- Focus on Application, Infrastructure, and API layers
- SQLValidator is CRITICAL for security - must enforce SELECT-only
- Per-user connection pool requires careful resource management
- Async embedding should use Spring @Async with thread pool executor

---

**Created**: 2026-03-06
**Status**: Pending User Approval
