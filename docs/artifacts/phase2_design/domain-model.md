# Tactical Design - Domain Model

---

## Context 1: Authentication

### 1. Aggregates

#### User (Aggregate Root)
```java
public class User {
    private final UserId id;
    private final Username username;
    private final EncryptedPassword password;
    private final UserRole role;
    private final CreatedAt createdAt;
    
    public void changePassword(String newPassword) {
        // Validate password strength
        // Encrypt and update
    }
    
    public boolean canAccess(String resource) {
        return role.hasPermission(resource);
    }
}
```

### 2. Entities
| Entity | Identity | Attributes |
|--------|----------|------------|
| User | UserId (UUID) | username, password, role, createdAt |
| Session | SessionId (UUID) | userId, token, expiresAt |

### 3. Value Objects
| VO | Attributes | Purpose |
|----|------------|---------|
| Username | String (3-50 chars) | User login name |
| EncryptedPassword | String (BCrypt) | Secure password storage |
| UserRole | Enum (ADMIN, USER, VIEWER) | Access control |
| JWT | String | Authentication token |

### 4. Invariants
| Aggregate | Invariant | Enforcement |
|-----------|-----------|-------------|
| User | Username must be unique | Database unique constraint |
| User | Password min 8 chars | Validation in changePassword() |
| Session | Token expires after 24h | Token expiration check |

### 5. Domain Events
| Event | Payload | Trigger |
|-------|---------|---------|
| UserRegistered | username, role | POST /api/auth/register |
| UserLoggedIn | userId, token | POST /api/auth/login |
| PasswordChanged | userId | User.changePassword() |

---

## Context 2: Database Connection

### 1. Aggregates

#### DatabaseConnection (Aggregate Root)
```java
public class DatabaseConnection {
    private final ConnectionId id;
    private final ConnectionConfig config;
    private final ConnectionStatus status;
    private final CreatedAt createdAt;
    
    public void connect() {
        // Validate config
        // Establish connection
        // Update status
    }
    
    public void disconnect() {
        // Close connection
        // Update status
    }
}
```

### 2. Entities
| Entity | Identity | Attributes |
|--------|----------|------------|
| DatabaseConnection | ConnectionId | host, port, service, username, encryptedPassword, status |
| Schema | SchemaId (String) | connectionId, name |

### 3. Value Objects
| VO | Attributes | Purpose |
|----|------------|---------|
| ConnectionConfig | host, port, service, username, password | Database connection details |
| ConnectionStatus | Enum (CONNECTED, DISCONNECTED, ERROR) | Connection state |
| ConnectionString | String | JDBC URL format |

### 4. Invariants
| Aggregate | Invariant | Enforcement |
|-----------|-----------|-------------|
| DatabaseConnection | Password encrypted at rest | AES-256 encryption |
| DatabaseConnection | Only one active connection per user | Connection pool management |

### 5. Domain Events
| Event | Payload | Trigger |
|-------|---------|---------|
| DatabaseConnected | connectionId | connect() success |
| ConnectionFailed | connectionId, error | connect() failure |

---

## Context 3: Schema (from Database Connection)

### 1. Aggregates

#### Schema (Aggregate Root)
```java
public class Schema {
    private final SchemaId id;
    private final ConnectionId connectionId;
    private final List<Table> tables;
    private final List<Relationship> relationships;
    private final ExtractedAt extractedAt;
    
    public Table findTable(String tableName) {
        return tables.stream()
            .filter(t -> t.getName().equals(tableName))
            .findFirst()
            .orElseThrow(() -> new TableNotFoundException(tableName));
    }
}
```

### 2. Entities
| Entity | Identity | Attributes |
|--------|----------|------------|
| Table | TableId | schemaId, name, columns, primaryKey |
| Column | ColumnId | name, dataType, nullable, defaultValue |
| PrimaryKey | PKId | tableId, columnIds |
| ForeignKey | FKId | sourceTable, sourceColumn, targetTable, targetColumn |
| Index | IndexId | tableId, columns, unique |

### 3. Value Objects
| VO | Attributes | Purpose |
|----|------------|---------|
| TableName | String | Name of table |
| ColumnName | String | Name of column |
| DataType | OracleDataType | VARCHAR2, NUMBER, DATE, etc. |
| Relationship | source→target | FK relationship |

### 4. Invariants
| Aggregate | Invariant | Enforcement |
|-----------|-----------|-------------|
| Schema | All FK reference existing PK | Validation on extraction |
| Table | Unique name within schema | Database constraint |

### 5. Domain Events
| Event | Payload | Trigger |
|-------|---------|---------|
| SchemaExtracted | connectionId, tableCount | JDBC metadata extraction |
| TableDiscovered | tableName, columnCount | Metadata scan |

---

## Context 4: ERD Visualization

### 1. Aggregates

#### ERDDiagram (Aggregate Root)
```java
public class ERDDiagram {
    private final DiagramId id;
    private final SchemaId schemaId;
    private final List<Node> nodes;
    private final List<Edge> edges;
    private final LayoutConfig layout;
    
    public void addNode(Table table) {
        nodes.add(Node.fromTable(table));
    }
    
    public void addEdge(Relationship rel) {
        edges.add(Edge.fromRelationship(rel));
    }
    
    public void autoLayout() {
        // Apply layout algorithm
    }
}
```

### 2. Entities
| Entity | Identity | Attributes |
|--------|----------|------------|
| Node | NodeId | tableId, position (x, y), label |
| Edge | EdgeId | sourceNodeId, targetNodeId, label |

### 3. Value Objects
| VO | Attributes | Purpose |
|----|------------|---------|
| Position | x: int, y: int | Node coordinates |
| LayoutConfig | algorithm: String | auto-layout settings |
| DiagramExport | format: PNG/SVG | Export configuration |

### 4. Invariants
| Aggregate | Invariant | Enforcement |
|-----------|-----------|-------------|
| ERDDiagram | No duplicate nodes | Check before add |
| ERDDiagram | Edge references valid nodes | Validate node existence |

---

## Context 5: AI Query

### 1. Aggregates

#### Query (Aggregate Root)
```java
public class Query {
    private final QueryId id;
    private final UserId userId;
    private final NaturalLanguageQuestion question;
    private final GeneratedSql sql;
    private final QueryStatus status;
    private final QueryResult result;
    
    public void generateSQL(Schema schema, OllamaService ollama) {
        // Build prompt with schema context
        // Call Ollama
        // Validate generated SQL
        // Update sql and status
    }
    
    public void execute(OracleDB db) {
        // Execute SQL
        // Store results
        // Update status
    }
}
```

### 2. Entities
| Entity | Identity | Attributes |
|--------|----------|------------|
| Query | QueryId | userId, question, sql, status, createdAt |
| QueryResult | ResultId | columns, rows, rowCount |

### 3. Value Objects
| VO | Attributes | Purpose |
|----|------------|---------|
| NaturalLanguageQuestion | String | User's question in plain language |
| GeneratedSql | String | SQL generated by AI |
| QueryStatus | Enum (PENDING, GENERATING, EXECUTING, COMPLETED, FAILED) | Query state |

### 4. Invariants
| Aggregate | Invariant | Enforcement |
|-----------|-----------|-------------|
| Query | SQL must be SELECT only | Security check before execute |
| Query | Question must not be empty | Validation |

### 5. Domain Events
| Event | Payload | Trigger |
|-------|---------|---------|
| SQLGenerated | queryId, sql | Ollama returns SQL |
| QueryExecuted | queryId, rowCount | SQL execution success |
| QueryFailed | queryId, error | SQL execution failure |

---

## Context 6: Data Grouping

### 1. Aggregates

#### DataGroup (Aggregate Root)
```java
public class DataGroup {
    private final GroupId id;
    private final UserId ownerId;
    private final GroupName name;
    private final List<TableId> tables;
    private final CreatedAt createdAt;
    
    public void addTable(TableId tableId) {
        if (tables.contains(tableId)) {
            throw new TableAlreadyInGroupException();
        }
        tables.add(tableId);
    }
    
    public void removeTable(TableId tableId) {
        tables.remove(tableId);
    }
}
```

### 2. Entities
| Entity | Identity | Attributes |
|--------|----------|------------|
| DataGroup | GroupId | ownerId, name, description, tables, createdAt |

### 3. Value Objects
| VO | Attributes | Purpose |
|----|------------|---------|
| GroupName | String (1-100 chars) | Group identifier |

### 4. Invariants
| Aggregate | Invariant | Enforcement |
|-----------|-----------|-------------|
| DataGroup | Unique name per user | Database unique constraint |
| DataGroup | Table belongs to only one group per user | Check before add |

---

## Context 7: Vector Sync

### 1. Aggregates

#### SyncJob (Aggregate Root)
```java
public class SyncJob {
    private final JobId id;
    private final UserId userId;
    private final ConnectionId connectionId;
    private final SyncConfig config;
    private final SyncStatus status;
    private final SyncProgress progress;
    private final StartedAt startedAt;
    private final CompletedAt completedAt;
    
    public void startFullSync(OracleDB db, OllamaService ollama, ChromaDB chroma) {
        status = SyncStatus.RUNNING;
        progress = new SyncProgress(0, totalRecords);
        
        List<Record> records = db.extractAllData(config.getTableNames());
        for (Record record : records) {
            String text = config.toTextRepresentation(record);
            float[] embedding = ollama.embed(text);
            chroma.upsert(config.getCollectionName(), record.getId(), embedding, text);
            progress.increment();
        }
        
        status = SyncStatus.COMPLETED;
    }
    
    public void startIncrementalSync(OracleDB db, OllamaService ollama, ChromaDB chroma) {
        // Similar but only sync changed records
    }
}
```

### 2. Entities
| Entity | Identity | Attributes |
|--------|----------|------------|
| SyncJob | JobId | userId, connectionId, config, status, progress, startedAt |
| SyncConfig | ConfigId | tableNames, columnMappings, collectionName |

### 3. Value Objects
| VO | Attributes | Purpose |
|----|------------|---------|
| SyncConfig | tables, columns, collection | Sync configuration |
| SyncStatus | Enum (PENDING, RUNNING, COMPLETED, FAILED) | Job state |
| SyncProgress | current, total | Progress tracking |
| ColumnMapping | sourceColumn, textTemplate | How to generate text from row |

### 4. Invariants
| Aggregate | Invariant | Enforcement |
|-----------|-----------|-------------|
| SyncJob | Only one running job per user | Job queue management |
| SyncJob | Config must have at least one table | Validation |

### 5. Domain Events
| Event | Payload | Trigger |
|-------|---------|---------|
| SyncStarted | jobId | startFullSync() called |
| DataSynced | jobId, recordCount | Batch synced |
| SyncCompleted | jobId, totalRecords | Sync finished |
| SyncFailed | jobId, error | Sync error |

---

## Context 8: Semantic Search

### 1. Aggregates

#### VectorSearch (Aggregate Root)
```java
public class VectorSearch {
    private final SearchId id;
    private final UserId userId;
    private final String query;
    private final SearchResult results;
    
    public void search(String queryText, OllamaService ollama, ChromaDB chroma) {
        float[] embedding = ollama.embed(queryText);
        results = chroma.similaritySearch(embedding, topK);
    }
}
```

### 2. Entities
| Entity | Identity | Attributes |
|--------|----------|------------|
| SearchResult | ResultId | queryId, results, scores |

### 3. Value Objects
| VO | Attributes | Purpose |
|----|------------|---------|
| SearchQuery | String | Search text |
| VectorResult | id, text, score | Single result |
| SimilarityScore | double (0-1) | Relevance score |

---

## Summary: All Domain Events

| Event | Context | Payload |
|-------|---------|---------|
| UserRegistered | Authentication | username, role |
| UserLoggedIn | Authentication | userId, token |
| PasswordChanged | Authentication | userId |
| DatabaseConnected | Database Connection | connectionId |
| ConnectionFailed | Database Connection | connectionId, error |
| SchemaExtracted | Schema | connectionId, tableCount |
| TableDiscovered | Schema | tableName, columnCount |
| ERDGenerated | ERD | diagramId |
| SQLGenerated | AI Query | queryId, sql |
| QueryExecuted | AI Query | queryId, rowCount |
| QueryFailed | AI Query | queryId, error |
| GroupCreated | Data Grouping | groupId |
| TableAssignedToGroup | Data Grouping | groupId, tableId |
| SyncStarted | Vector Sync | jobId |
| DataSynced | Vector Sync | jobId, recordCount |
| SyncCompleted | Vector Sync | jobId |
| SyncFailed | Vector Sync | jobId, error |
