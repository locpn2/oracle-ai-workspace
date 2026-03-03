# Application Layer - Triển khai Application Services

## Mục tiêu
Implement Application Services, Use Cases, và DTOs.

## Input → Output
- **Input:** Domain layer, Use Cases từ SPEC
- **Output:** Application services code

## Parallel Triggers
- Phụ thuộc `03_implementation/02_domain.md`

## Quality Gates
- [ ] Business logic trong Domain, không trong Application
- [ ] DTOs tách biệt với Domain objects
- [ ] Use cases có single responsibility

## Key Questions
- Use case orchestration logic?
- Transaction boundaries?
- Error handling strategy?

---

## Workflow

### Bước 1: DTOs Definition
- Request DTOs
- Response DTOs

### Bước 2: Use Cases Implementation
```java
@Service
@RequiredArgsConstructor
public class [UseCaseName]UseCase {
    private final [Repository] repository;
    
    public Output execute(Input input) {
        // 1. Validate input
        // 2. Call domain
        // 3. Return output
    }
}
```

### Bước 3: Application Service
- Orchestrate use cases
- Handle transactions
- Publish domain events

---

## Output Format

```markdown
# Application Layer - [Context Name]

## 1. Request DTOs
### [Name]Request.java
```java
// content
```

## 2. Response DTOs
### [Name]Response.java
```java
// content
```

## 3. Use Cases
### [UseCaseName]UseCase.java
```java
// Invariant: [from tactical design]
```

## 4. Application Service
### [ServiceName]Service.java
```java
// content
```
```
