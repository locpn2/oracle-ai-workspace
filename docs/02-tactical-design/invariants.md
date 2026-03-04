# Invariants - Phase 2: Tactical Design

## 1. Overview

Document này liệt kê các **Invariant** (quy tắc nghiệp vụ bắt buộc phải đúng mọi lúc) cho từng Bounded Context. Invariants phải được enforce trực tiếp trong Domain layer.

---

## 2. Schema Context Invariants

### 2.1 SchemaMetadata Aggregate

| # | Invariant | Description | Enforcement Location |
|---|-----------|-------------|---------------------|
| S1 | **Table name unique** | Tên table phải unique trong schema | `SchemaMetadata.addTable()` |
| S2 | **Column exists before reference** | FK reference phải đến column tồn tại | `ForeignKey` constructor |
| S3 | **PK columns exist** | PK columns phải là columns của table | `PrimaryKey` constructor |
| S4 | **At least one table** | Schema không được empty | `SchemaMetadata` factory |

### 2.2 Table Entity

| # | Invariant | Description | Enforcement Location |
|---|-----------|-------------|---------------------|
| S5 | **Column name unique** | Tên column unique trong table | `Table.addColumn()` |
| S6 | **FK source columns exist** | FK source phải là columns của table | `ForeignKey` validation |
| S7 | **PK non-empty** | PK phải có ít nhất 1 column | `PrimaryKey` constructor |

---

## 3. Chat Context Invariants

### 3.1 SQL Validation (Critical Security Invariant)

```java
// ═══════════════════════════════════════════════════════════════════
// INVARIANT: SQL must be SELECT-only for security
// ═══════════════════════════════════════════════════════════════════

public class SQLValidator {
    
    // Whitelist of allowed SQL starting patterns
    private static final Set<String> ALLOWED_PREFIXES = Set.of(
        "SELECT",
        "WITH"
    );
    
    // Forbidden keywords that indicate dangerous operations
    private static final Set<String> FORBIDDEN_KEYWORDS = Set.of(
        "DROP", "DELETE", "INSERT", "UPDATE", "CREATE", "ALTER",
        "TRUNCATE", "EXEC", "EXECUTE", "GRANT", "REVOKE",
        "COMMIT", "ROLLBACK", "CALL"
    );
    
    public ValidatedSQL validate(String sql) {
        // Rule 1: Must start with allowed prefix
        String trimmed = sql.trim();
        String upper = trimmed.toUpperCase();
        
        boolean allowedPrefix = ALLOWED_PREFIXES.stream()
            .anyMatch(upper::startsWith);
            
        if (!allowedPrefix) {
            throw new SQLValidationException(
                "SQL must start with: SELECT or WITH");
        }
        
        // Rule 2: No forbidden keywords
        for (String keyword : FORBIDDEN_KEYWORDS) {
            Pattern pattern = Pattern.compile(
                "\\b" + keyword + "\\b", 
                Pattern.CASE_INSENSITIVE
            );
            if (pattern.matcher(upper).find()) {
                throw new SQLValidationException(
                    "Forbidden keyword in SQL: " + keyword);
            }
        }
        
        // Rule 3: No UNION with dangerous queries
        if (upper.contains("UNION")) {
            String[] parts = upper.split("UNION");
            for (int i = 1; i < parts.length; i++) {
                String part = parts[i].trim();
                if (!part.startsWith("SELECT")) {
                    throw new SQLValidationException(
                        "UNION must be followed by SELECT only");
                }
            }
        }
        
        // Rule 4: Max result rows limit
        if (upper.contains("LIMIT")) {
            Pattern limitPattern = Pattern.compile(
                "LIMIT\\s+(\\d+)", Pattern.CASE_INSENSITIVE
            );
            Matcher m = limitPattern.matcher(upper);
            if (m.find()) {
                int limit = Integer.parseInt(m.group(1));
                if (limit > 10000) {
                    throw new SQLValidationException(
                        "LIMIT cannot exceed 10000 rows }
        }
        
");
                }
                   // Extract referenced tables and columns
        Set<TableName> tables = extractReferencedTables(sql);
        Set<ColumnName> columns = extractReferencedColumns(sql);
        
        return new ValidatedSQL(sql, SQLType.SELECT, tables, columns);
    }
}
```

### 3.2 ChatSession Aggregate

| # | Invariant | Description | Enforcement Location |
|---|-----------|-------------|---------------------|
| C1 | **Session owner** | Chỉ owner mới add được message | `ChatSession.addMessage()` |
| C2 | **Valid status transition** | ACTIVE → CLOSED/EXPIRED | `ChatSession.close()` |
| C3 | **Message timestamp** | Messages phải theo thứ tự thời gian | `ChatMessage` constructor |
| C4 | **Max history** | Session max 100 messages | `ChatSession.addMessage()` |

---

## 4. Vector Context Invariants

### 4.1 EmbeddingJob State Machine

```java
// ═══════════════════════════════════════════════════════════════════
// INVARIANT: Valid state transitions for EmbeddingJob
// ═══════════════════════════════════════════════════════════════════

public class EmbeddingJob {
    
    // Valid state transitions map
    private static final Map<JobStatus, Set<JobStatus>> VALID_TRANSITIONS = Map.of(
        JobStatus.PENDING,   Set.of(JobStatus.PROCESSING, JobStatus.CANCELLED),
        JobStatus.PROCESSING, Set.of(JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED),
        JobStatus.COMPLETED,  Set.of(),
        JobStatus.FAILED,    Set.of(JobStatus.PENDING),  // Allow retry
        JobStatus.CANCELLED,  Set.of(JobStatus.PENDING)  // Allow retry
    );
    
    public void start() {
        // INVARIANT: Can only start from PENDING
        if (this.status != JobStatus.PENDING) {
            throw new IllegalStateException(
                "Cannot start job in status: " + this.status + 
                ". Only PENDING jobs can be started.");
        }
        this.status = JobStatus.PROCESSING;
    }
    
    public void complete() {
        // INVARIANT: All rows must be processed before completion
        if (this.status != JobStatus.PROCESSING) {
            throw new IllegalStateException(
                "Cannot complete job not in PROCESSING status");
        }
        if (this.processedRows < this.totalRows) {
            throw new IllegalStateException(
                "Cannot complete: " + processedRows + "/" + totalRows + 
                " rows processed");
        }
        this.status = JobStatus.COMPLETED;
        this.completedAt = Instant.now();
    }
    
    public void fail(ErrorReason reason) {
        // INVARIANT: Failure reason must be provided
        if (reason == null) {
            throw new IllegalArgumentException("Failure reason required");
        }
        this.status = JobStatus.FAILED;
        this.failureReason = reason;
    }
    
    public void retry() {
        // INVARIANT: Can only retry FAILED or CANCELLED jobs
        if (this.status != JobStatus.FAILED && 
            this.status != JobStatus.CANCELLED) {
            throw new IllegalStateException(
                "Can only retry FAILED or CANCELLED jobs");
        }
        this.status = JobStatus.PENDING;
        this.processedRows = 0;
    }
}
```

### 4.2 Vector Entry Rules

| # | Invariant | Description | Enforcement Location |
|---|-----------|-------------|---------------------|
| V1 | **Valid embedding dimension** | Vector phải có đúng 768 dimensions | `VectorEntry` constructor |
| V2 | **Non-empty document** | Document text không được empty` constructor |
| V3 | **Score | `VectorEntry range** | Similarity score phải trong [-1, 1] | `VectorEntry` factory |

---

## 5. Auth Context Invariants

### 5.1 User Password Policy

```java
// ═══════════════════════════════════════════════════════════════════
// INVARIANT: Password strength requirements
// ═══════════════════════════════════════════════════════════════════

public record HashedPassword {
    
    public static HashedPassword fromPlain(String plain) {
        // Rule 1: Minimum length
        if (plain == null || plain.length() < 8) {
            throw new ValidationException(
                "Password must be at least 8 characters");
        }
        
        // Rule 2: Contains uppercase
        if (!plain.matches(".*[A-Z].*")) {
            throw new ValidationException(
                "Password must contain at least one uppercase letter");
        }
        
        // Rule 3: Contains lowercase
        if (!plain.matches(".*[a-z].*")) {
            throw new ValidationException(
                "Password must contain at least one lowercase letter");
        }
        
        // Rule 4: Contains digit
        if (!plain.matches(".*\\d.**")) {
            throw new ValidationException(
                "Password must contain at least one digit");
        }
        
        // Rule 5: No common passwords
        if (COMMON_PASSWORDS.contains(plain.toLowerCase())) {
            throw new ValidationException(
                "Password is too common, choose a stronger one");
        }
        
        return new HashedPassword(BCrypt.hashpw(plain, BCrypt.gensalt()));
    }
    
    private static final Set<String> COMMON_PASSWORDS = Set.of(
        "password", "12345678", "qwerty", "admin", "letmein",
        "welcome", "monkey", "1234567890"
    );
}
```

### 5.2 User Entity Invariants

| # | Invariant | Description | Enforcement Location |
|---|-----------|-------------|---------------------|
| A1 | **Unique username** | Username phải unique | `User` constructor validation |
| A2 | **Unique email** | Email phải unique | `User` constructor validation |
| A3 | **At least one role** | User phải có ít nhất 1 role | `User` constructor |
| A4 | **Valid role combination** | VIEWER không thể có WRITE permissions | `User.assignRole()` |

### 5.3 Connection Pool Invariants

| # | Invariant | Description | Enforcement Location |
|---|-----------|-------------|---------------------|
| A5 | **Max pool size** | Pool size tối đa 20 connections | `ConnectionPoolConfig` |
| A6 | **Connection timeout** | Timeout tối thiểu 5s | `ConnectionPoolConfig` |

---

## 6. Cross-Context Invariants

### 6.1 Identity References

| # | Invariant | Description | Enforcement |
|---|-----------|-------------|-------------|
| X1 | **Valid UUID** | All IDs phải là valid UUID | Constructor validation |
| X2 | **Non-null references** | Không ID nào được null | Constructor |
| X3 | **Cross-context validation** | UserId phải tồn tại trong Auth | Repository check |

---

## 7. Testing Invariants

Mỗi invariant cần có unit test:

```java
class SQLValidatorTest {
    
    @Test
    void validate_SelectQuery_ReturnsValidatedSQL() {
        String sql = "SELECT * FROM employees WHERE salary > 5000";
        ValidatedSQL result = validator.validate(sql);
        
        assertTrue(result.isValid());
        assertEquals(SQLType.SELECT, result.type());
    }
    
    @Test
    void validate_InsertQuery_ThrowsException() {
        String sql = "INSERT INTO employees VALUES (1, 'John')";
        
        assertThrows(SQLValidationException.class, 
            () -> validator.validate(sql));
    }
    
    @Test
    void validate_DropTable_ThrowsException() {
        String sql = "DROP TABLE employees";
        
        SQLValidationException ex = assertThrows(
            SQLValidationException.class,
            () -> validator.validate(sql)
        );
        assertTrue(ex.getMessage().contains("DROP"));
    }
}
```

---

## 8. Summary

| Context | Key Invariants | Priority |
|---------|---------------|----------|
| **Schema** | Table uniqueness, FK validity | HIGH |
| **Chat** | SQL SELECT-only (SECURITY) | CRITICAL |
| **Vector** | State machine transitions | HIGH |
| **Auth** | Password policy, role validation | HIGH |

**Nguyên tắc:**
- Invariants được enforce **TRỰC TIẾP** trong Domain layer
- Không để Application Service validate business rules
- Mọi state change phải qua domain methods
- Unit tests bắt buộc cho mỗi invariant
