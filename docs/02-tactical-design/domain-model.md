# Domain Model - Phase 2: Tactical Design

## 1. Overview

Document này định nghĩa chi tiết **Entities**, **Value Objects**, và **Aggregates** cho từng Bounded Context theo Clean Architecture.

---

## 2. Schema Context

### 2.1 Aggregate: SchemaMetadata (Aggregate Root)

```java
// Aggregate Root - có identity và là entry point cho tất cả operations
public class SchemaMetadata {
    private final SchemaId id;              // Identity
    private final UserId ownerId;           // Reference to Auth Context
    private final List<Table> tables;        // Child entities
    private final Instant extractedAt;      // Timestamp
    private final SchemaVersion version;    // Value Object
    
    // Domain methods - business logic BÊN TRONG aggregate
    public void addTable(Table table) { ... }
    public Optional<Table> getTable(TableName name) { ... }
    public List<Relationship> getAllRelationships() { ... }
}
```

### 2.2 Entity: Table

```java
// Entity - có identity (tableName) nhưng phụ thuộc Aggregate Root
public class Table {
    private final TableName name;           // Identity
    private final List<Column> columns;     // Value Objects
    private final PrimaryKey primaryKey;   // Value Object
    private final List<ForeignKey> foreignKeys;
    private final TableType type;          // Value Object (VIEW, TABLE, etc.)
    
    // Domain logic
    public boolean hasColumn(ColumnName name) { ... }
    public Optional<ForeignKey> findForeignKeyTo(TableName target) { ... }
}
```

### 2.3 Value Objects

```java
// Value Object - immutable, không có identity
public record Column(
    ColumnName name,
    DataType dataType,
    boolean nullable,
    int position,
    String defaultValue
) {
    // No setters - immutable
}

// Value Object cho PK
public record PrimaryKey(
    List<ColumnName> columns,
    ConstraintName name
) {}

// Value Object cho FK
public record ForeignKey(
    ConstraintName name,
    List<ColumnName> sourceColumns,
    TableName targetTable,
    List<ColumnName> targetColumns,
    DeleteRule deleteRule  // CASCADE, SET NULL, etc.
) {}

// Value Object cho data type
public enum DataType {
    VARCHAR2, NUMBER, DATE, TIMESTAMP, 
    BLOB, CLOB, RAW, ROWID, INTEGER, FLOAT, DOUBLE
}

// Value Object cho schema version
public record SchemaVersion(int major, int minor) implements Comparable<SchemaVersion> {
    public SchemaMetadata increment() { ... }
}

// Value Object cho table type
public enum TableType {
    TABLE, VIEW, MATERIALIZED_VIEW, SYNONYM
}

// Value Object cho delete rule
public enum DeleteRule {
    NO_ACTION, CASCADE, SET_NULL, SET_DEFAULT, RESTRICT
}
```

---

## 3. Chat Context

### 3.1 Aggregate: ChatSession (Aggregate Root)

```java
public class ChatSession {
    private final SessionId id;             // Identity
    private final UserId userId;            // Reference to Auth
    private final SchemaId schemaId;        // Reference to Schema
    private final List<ChatMessage> messages;
    private final SessionStatus status;
    private final Instant createdAt;
    private final Instant lastActivityAt;
    
    // Domain methods
    public void addUserMessage(String content) { ... }
    public void addAssistantMessage(String content, String sql) { ... }
    public List<ChatMessage> getRecentMessages(int count) { ... }
    public void close() { ... }
}
```

### 3.2 Entity: ChatMessage

```java
public class ChatMessage {
    private final MessageId id;             // Identity
    private final MessageRole role;         // Value Object
    private final String content;
    private final String sql;               // Optional - chỉ assistant messages
    private final Instant timestamp;
    private final ExecutionResult result;   // Optional
    
    public boolean hasSQL() { return sql != null; }
    public boolean isSuccessful() { return result != null && result.isSuccess(); }
}
```

### 3.3 Value Objects

```java
// Value Object cho message role
public enum MessageRole {
    USER, SYSTEM, ASSISTANT
}

// Value Object cho session status
public enum SessionStatus {
    ACTIVE, CLOSED, EXPIRED
}

// Value Object cho SQL generation result
public record ExecutionResult(
    boolean success,
    int rowCount,
    List<String> columns,
    List<Map<String, Object>> data,
    String errorMessage
) {
    public static ExecutionResult failure(String message) { ... }
}

// Value Object cho validated SQL
public record ValidatedSQL(
    String sql,
    SQLType type,                    // SELECT, etc.
    Set<TableName> referencedTables,
    Set<ColumnName> referencedColumns
) {}

// Value Object cho SQL type
public enum SQLType {
    SELECT, SELECT_INTO, WITH
}
```

---

## 4. Vector Context

### 4.1 Aggregate: EmbeddingJob (Aggregate Root)

```java
public class EmbeddingJob {
    private final JobId id;                // Identity
    private final UserId userId;
    private final TableName sourceTable;
    private JobStatus status;
    private long totalRows;
    private long processedRows;
    private final List<EmbeddingBatch> batches;
    private final EmbeddingConfig config;
    private final Instant createdAt;
    private Instant completedAt;
    private ErrorReason failureReason;
    
    // Domain methods - enforce state transitions
    public void start() {
        if (status != JobStatus.PENDING) 
            throw new IllegalStateException("Can only start PENDING job");
        this.status = JobStatus.PROCESSING;
    }
    
    public void completeBatch(BatchId batchId, List<VectorEntry> vectors) {
        // Business logic: update batch, check if all done
    }
    
    public void fail(ErrorReason reason) {
        this.status = JobStatus.FAILED;
        this.failureReason = reason;
    }
}
```

### 4.2 Entity: EmbeddingBatch

```java
public class EmbeddingBatch {
    private final BatchId id;              // Identity
    private final int batchNumber;
    private final long startRow;
    private final long endRow;
    private BatchStatus status;
    private List<VectorEntry> vectors;
    
    public boolean isComplete() { return status == BatchStatus.COMPLETED; }
}
```

### 4.3 Value Objects

```java
// Value Object cho job status
public enum JobStatus {
    PENDING, PROCESSING, COMPLETED, FAILED, CANCELLED
}

// Value Object cho batch status  
public enum BatchStatus {
    QUEUED, PROCESSING, COMPLETED, FAILED
}

// Value Object cho vector entry
public record VectorEntry(
    RowId rowId,              // Original Oracle ROWID
    String document,          // Flattened text
    float[] embedding,        // 768-dim vector
    double similarityScore   // Computed after search
) {}

// Value Object cho embedding configuration
public record EmbeddingConfig(
    EmbeddingModel model,    // BGE_BASE, etc.
    int batchSize,
    int maxRetries,
    Duration timeout
) {
    public static EmbeddingConfig defaultConfig() {
        return new EmbeddingConfig(EmbeddingModel.BGE_BASE, 1000, 3, Duration.ofMinutes(5));
    }
}

// Value Object cho embedding model
public enum EmbeddingModel {
    BGE_BASE("bge-base"),
    SQLCODER_7B("sqlcoder-7b"),
    NOMIC_EMBED("nomic-embed-text");
    
    private final String modelName;
}

// Value Object cho search result
public record SearchResult(
    VectorEntry entry,
    double similarityScore,
    String highlightedText
) {}

// Value Object cho error reason
public record ErrorReason(
    String code,
    String message,
    Throwable cause
) {}
```

---

## 5. Auth Context

### 5.1 Aggregate: User (Aggregate Root)

```java
public class User {
    private final UserId id;               // Identity
    private final Username username;      // Value Object
    private final HashedPassword password; // Value Object
    private final Email email;             // Value Object
    private final Set<Role> roles;
    private UserStatus status;
    private final Instant createdAt;
    private Instant lastLoginAt;
    
    // Domain methods
    public void changePassword(CurrentPassword current, NewPassword newPwd) {
        if (!this.password.matches(current.value()))
            throw new InvalidPasswordException();
        this.password = newPwd.hash();
    }
    
    public void assignRole(Role role) { 
        this.roles.add(role); 
    }
    
    public boolean hasPermission(Permission perm) { ... }
    
    public void lock() {
        this.status = UserStatus.LOCKED;
    }
}
```

### 5.2 Entity: DbConnection

```java
public class DbConnection {
    private final ConnectionId id;         // Identity
    private final UserId userId;
    private final ConnectionString connStr;
    private final ConnectionPoolConfig poolConfig;
    private ConnectionStatus status;
    private final Instant createdAt;
    
    public void activate() {
        this.status = ConnectionStatus.ACTIVE;
    }
    
    public void deactivate() {
        this.status = ConnectionStatus.INACTIVE;
    }
}
```

### 5.3 Value Objects

```java
// Value Object cho username
public record Username(String value) {
    public Username {
        if (value == null || value.length() < 3)
            throw new ValidationException("Username must be at least 3 characters");
        if (!value.matches("^[a-zA-Z0-9_]+$"))
            throw new ValidationException("Username can only contain alphanumeric and underscore");
    }
}

// Value Object cho email
public record Email(String value) {
    public Email {
        if (value == null || !value.matches("^[A-Za-z0-9+_.-]+@(.+)$"))
            throw new ValidationException("Invalid email format");
    }
}

// Value Object cho hashed password
public record HashedPassword(String value) {
    public static HashedPassword fromPlain(String plain) { 
        // BCrypt hashing
        return new HashedPassword(BCrypt.hashpw(plain, BCrypt.gensalt()));
    }
    
    public boolean matches(String plain) {
        return BCrypt.checkpw(plain, this.value);
    }
}

// Value Object cho roles
public enum Role {
    ADMIN, USER, VIEWER
}

// Value Object cho permissions
public enum Permission {
    SCHEMA_READ, SCHEMA_WRITE,
    CHAT_QUERY, CHAT_HISTORY,
    VECTOR_EMBED, VECTOR_SEARCH,
    USER_MANAGE
}

// Value Object cho user status
public enum UserStatus {
    ACTIVE, SUSPENDED, LOCKED
}

// Value Object cho connection status
public enum ConnectionStatus {
    ACTIVE, INACTIVE, EXPIRED
}

// Value Object cho connection string
public record ConnectionString(String jdbcUrl, String username, String password) {
    public static ConnectionString parse(String raw) {
        // Parse JDBC URL format
    }
}

// Value Object cho connection pool config
public record ConnectionPoolConfig(
    int minIdle,
    int maxPoolSize,
    long connectionTimeout,
    long idleTimeout
) {
    public static ConnectionPoolConfig defaults() {
        return new ConnectionPoolConfig(1, 10, 30000, 600000);
    }
}
```

---

## 6. Identity References (Cross-Context)

Theo DDD nguyên tắc, các Aggregates chỉ tham chiếu nhau qua ID:

```java
// Reference types - chỉ là ID, không chứa business logic
public record SchemaId(UUID value) {}
public record UserId(UUID value) {}
public record SessionId(UUID value) {}
public record JobId(UUID value) {}
public record TableName(String value) {}
public record ColumnName(String value) {}
public record RowId(String value) {}
public record MessageId(UUID value) {}
public record BatchId(UUID value) {}
public record ConnectionId(UUID value) {}
public record ConstraintName(String value) {}
```

---

## 7. Domain Events

Các sự kiện được phát ra sau khi state thay đổi:

```java
// Schema Context Events
public record SchemaExtracted(SchemaId schemaId, int tableCount) {}
public record TableAdded(SchemaId schemaId, TableName tableName) {}

// Chat Context Events  
public record QueryReceived(SessionId sessionId, String query) {}
public record SQLGenerated(SessionId sessionId, String sql, AIProvider provider) {}
public record SQLValidated(SessionId sessionId, ValidatedSQL sql) {}
public record SQLExecuted(SessionId sessionId, int rowCount) {}
public record FallbackTriggered(SessionId sessionId, AIProvider from, AIProvider to) {}

// Vector Context Events
public record EmbeddingJobStarted(JobId jobId, TableName tableName) {}
public record BatchCompleted(JobId jobId, BatchId batchId, int vectorCount) {}
public record EmbeddingJobCompleted(JobId jobId, long totalVectors) {}
public record EmbeddingJobFailed(JobId jobId, ErrorReason reason) {}

// Auth Context Events
public record UserRegistered(UserId userId, Username username) {}
public record UserAuthenticated(UserId userId) {}
public record PasswordChanged(UserId userId) {}
public record UserLocked(UserId userId) {}

// AI Provider value object
public enum AIProvider {
    GROQ, OLLAMA, GEMINI
}
```

---

## 8. Summary

| Context | Aggregate Root | Entity | Value Objects |
|---------|---------------|--------|---------------|
| **Schema** | SchemaMetadata | Table | Column, ForeignKey, PrimaryKey, DataType, SchemaVersion |
| **Chat** | ChatSession | ChatMessage | MessageRole, SessionStatus, ValidatedSQL, ExecutionResult |
| **Vector** | EmbeddingJob | EmbeddingBatch | JobStatus, BatchStatus, VectorEntry, EmbeddingConfig, SearchResult |
| **Auth** | User | DbConnection | Username, Email, HashedPassword, Role, Permission |

**Nguyên tắc áp dụng:**
- ✅ **Rich Domain Model** - Logic nghiệp vụ trong Entities/Aggregates
- ✅ **Primitive Obsession** - Dùng Value Objects thay primitives  
- ✅ **Identity Reference** - Tham chiếu qua ID không import Entities
- ✅ **Immutability** - Value Objects là immutable records
- ✅ **Encapsulation** - State changes qua domain methods, enforce invariants
