# Domain Implementation - Triển khai Domain Layer

## Mục tiêu
Implement Entities, Value Objects, Aggregates theo Tactical Design.

## Input → Output
- **Input:** Tactical Design output
- **Output:** Domain layer code

## Parallel Triggers
- Phụ thuộc `03_implementation/01_setup.md`
- Có thể chạy song song với `03_application.md`

## Quality Gates
- [ ] Invariants được enforce trong code
- [ ] Value Objects là immutable
- [ ] Domain events phát sinh đúng

## Key Questions
- Invariant violations có throw exception?
- Factory methods hay constructors?
- Domain events implemented how?

---

## Workflow

### Bước 1: Value Objects Implementation
```java
public record ColumnName(String value) {
    public ColumnName {
        if (value == null || value.isBlank())
            throw new IllegalArgumentException("...");
    }
}
```

### Bước 2: Entities Implementation
- Identity fields
- Business methods
- Invariant enforcement

### Bước 3: Aggregate Root Implementation
- State management
- Command methods
- Domain events publishing

---

## Output Format

```markdown
# Domain Implementation - [Context Name]

## 1. Value Objects
### [VOName].java
```java
// [file content]
```

## 2. Entities
### [EntityName].java
```java
// [file content]
```

## 3. Aggregate Root
### [AggregateName].java
```java
// [file content]
// Invariant: [description]
// Domain Event: [event name]
```

## 4. Domain Events
```java
public record [EventName]([params]) {}
```

## 5. Repository Interface
```java
public interface [RepositoryName] {
    // signatures
}
```
```
