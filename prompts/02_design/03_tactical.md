# Tactical Design - Thiết kế Chiến thuật

## Mục tiêu
Chi tiết hóa Domain Model với Aggregates, Entities, Value Objects.

## Input → Output
- **Input:** Strategic design output
- **Output:** Domain Model chi tiết

## Parallel Triggers
- Phụ thuộc `02_design/02_strategic.md`

## Quality Gates
- [ ] Mỗi aggregate có clear invariant
- [ ] Identity và value objects đã phân biệt
- [ ] Domain events đã identified

## Key Questions
- Aggregate root của mỗi context?
- Invariants cần enforce?
- Domain events phát sinh khi nào?

---

## Workflow

### Bước 1: Aggregate Design
Cho mỗi Bounded Context:
- Xác định Aggregate Root
- Xác định Entities (có identity)
- Xác định Value Objects (immutable)

### Bước 2: Invariant Definition
Mỗi aggregate cần:
- State transitions
- Business rules
- Validation logic

### Bước 3: Domain Events
Xác định events phát sinh từ state changes

---

## Output Format

```markdown
# Tactical Design - [Context Name]

## 1. Aggregates
### [AggregateName] (Aggregate Root)
```java
public class [AggregateName] {
    private final [IdType] id;
    private final [ValueObject] ...;
    
    // Domain methods
    public void [action]() {
        // Invariant enforcement
    }
}
```

## 2. Entities
| Entity | Identity | Attributes |
|--------|----------|------------|
| ... | ... | ... |

## 3. Value Objects
| VO | Attributes | Purpose |
|----|------------|---------|
| ... | ... | ... |

## 4. Invariants
| Aggregate | Invariant | Enforcement |
|-----------|-----------|-------------|
| ... | ... | ... |

## 5. Domain Events
| Event | Payload | Trigger |
|-------|---------|---------|
| ... | ... | ... |
```
